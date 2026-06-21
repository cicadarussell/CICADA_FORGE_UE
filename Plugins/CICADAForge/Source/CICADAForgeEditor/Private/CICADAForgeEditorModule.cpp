#include "CICADAForgeEditorModule.h"

#include "CICADAForgeStatusModel.h"

#include "Framework/Docking/TabManager.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformProcess.h"
#include "Input/Reply.h"
#include "Logging/LogMacros.h"
#include "Math/Vector.h"
#include "Misc/DateTime.h"
#include "Misc/FileHelper.h"
#include "Misc/Guid.h"
#include "Misc/Paths.h"
#include "Templates/SharedPointer.h"
#include "ToolMenus.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SScrollBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SWidget.h"
#include "Widgets/Text/STextBlock.h"

DEFINE_LOG_CATEGORY_STATIC(LogCICADAForgeEditor, Log, All);

#define LOCTEXT_NAMESPACE "FCICADAForgeEditorModule"

const FName FCICADAForgeEditorModule::ForgeTabName(TEXT("CICADAForgeMainTab"));

namespace CICADAForgeEditorUI
{
    struct FBoxSketch
    {
        float WidthMm = 80.0f;
        float DepthMm = 40.0f;
        float HeightMm = 12.0f;
        bool bHasSketch = false;
        bool bHasExtrude = false;
        bool bValidated = false;
        bool bBuildVolumePassed = false;
    };

    struct FForgeState
    {
        int32 TotalEvents = 0;
        int32 StlExports = 0;
        int32 ManifestExports = 0;
        int32 ReceiptsWritten = 0;

        FString LastAction = TEXT("none");
        FString LastDiagnostic = TEXT("No diagnostics run yet.");
        FString LastStlPath = TEXT("none");
        FString LastManifestPath = TEXT("none");
        FString LastReceiptPath = TEXT("none");
        FString BackendInspector = TEXT("Backend Inspector:\nReady for sketch box -> STL workflow.\nDirect printer send remains locked.");

        FBoxSketch Sketch;
        TArray<FString> FeatureOps;
        TArray<FString> Events;
    };

    struct FForgeLiveContext
    {
        FString SessionId;
        FString SessionStarted;
        FForgeState State;

        TSharedPtr<STextBlock> SelectedAction;
        TSharedPtr<STextBlock> SessionMetadata;
        TSharedPtr<STextBlock> SketchStatus;
        TSharedPtr<STextBlock> ExportStatus;
        TSharedPtr<STextBlock> PrinterStatus;
        TSharedPtr<STextBlock> BackendHealth;
        TSharedPtr<STextBlock> BackendInspector;
        TSharedPtr<STextBlock> EventLog;
        TSharedPtr<STextBlock> Diagnostics;
    };

    static FString EscapeJson(const FString& In)
    {
        FString Out = In;
        Out.ReplaceInline(TEXT("\\"), TEXT("\\\\"));
        Out.ReplaceInline(TEXT("\""), TEXT("\\\""));
        Out.ReplaceInline(TEXT("\r"), TEXT("\\r"));
        Out.ReplaceInline(TEXT("\n"), TEXT("\\n"));
        return Out;
    }

    static FString BoolWord(const bool bValue)
    {
        return bValue ? TEXT("yes") : TEXT("no");
    }

    static void AddEvent(const TSharedRef<FForgeLiveContext>& Ctx, const FString& Line)
    {
        Ctx->State.TotalEvents += 1;
        Ctx->State.Events.Insert(Line, 0);

        while (Ctx->State.Events.Num() > 14)
        {
            Ctx->State.Events.RemoveAt(Ctx->State.Events.Num() - 1);
        }
    }

    static void SetPreset(
        const TSharedRef<FForgeLiveContext>& Ctx,
        const float WidthMm,
        const float DepthMm,
        const float HeightMm,
        const FString& PresetName
    )
    {
        Ctx->State.Sketch.WidthMm = WidthMm;
        Ctx->State.Sketch.DepthMm = DepthMm;
        Ctx->State.Sketch.HeightMm = HeightMm;
        Ctx->State.Sketch.bHasSketch = true;
        Ctx->State.Sketch.bHasExtrude = true;
        Ctx->State.Sketch.bValidated = false;
        Ctx->State.Sketch.bBuildVolumePassed = false;
        Ctx->State.FeatureOps.Empty();
        Ctx->State.FeatureOps.Add(FString::Printf(TEXT("PRESET %s"), *PresetName));
        Ctx->State.FeatureOps.Add(FString::Printf(TEXT("SKETCH_RECT width=%.2fmm depth=%.2fmm plane=XY"), WidthMm, DepthMm));
        Ctx->State.FeatureOps.Add(FString::Printf(TEXT("EXTRUDE height=%.2fmm operation=new_body"), HeightMm));
        Ctx->State.LastAction = PresetName;
        Ctx->State.LastDiagnostic = TEXT("Preset sketch box created in memory.");
        Ctx->State.BackendInspector = FString::Printf(
            TEXT("Backend Inspector:\nPreset: %s\nSketch/extrude state: READY\nSTL exporter: ready\nDirect printer send: locked"),
            *PresetName
        );

        AddEvent(Ctx, FString::Printf(TEXT("PRESET: %s %.2f x %.2f x %.2f mm"), *PresetName, WidthMm, DepthMm, HeightMm));
    }

    static FString BuildSketchText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        FString Text = FString::Printf(
            TEXT("Sketch Box Model:\nSketch: %s\nExtrude: %s\nValidated: %s\nBuild volume checked: %s\nWidth: %.2f mm\nDepth: %.2f mm\nHeight: %.2f mm\nOps: %d\n\nFeature operations:"),
            *BoolWord(Ctx->State.Sketch.bHasSketch),
            *BoolWord(Ctx->State.Sketch.bHasExtrude),
            *BoolWord(Ctx->State.Sketch.bValidated),
            *BoolWord(Ctx->State.Sketch.bBuildVolumePassed),
            Ctx->State.Sketch.WidthMm,
            Ctx->State.Sketch.DepthMm,
            Ctx->State.Sketch.HeightMm,
            Ctx->State.FeatureOps.Num()
        );

        if (Ctx->State.FeatureOps.Num() == 0)
        {
            Text += TEXT("\nNo feature operations yet.");
            return Text;
        }

        for (int32 Index = 0; Index < Ctx->State.FeatureOps.Num(); ++Index)
        {
            Text += FString::Printf(TEXT("\n%d. %s"), Index + 1, *Ctx->State.FeatureOps[Index]);
        }

        return Text;
    }

    static FString BuildExportText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return FString::Printf(
            TEXT("Export State:\nSTL exports: %d\nPrint manifests: %d\nReceipts: %d\nLast STL: %s\nLast manifest: %s\nLast receipt: %s"),
            Ctx->State.StlExports,
            Ctx->State.ManifestExports,
            Ctx->State.ReceiptsWritten,
            *Ctx->State.LastStlPath,
            *Ctx->State.LastManifestPath,
            *Ctx->State.LastReceiptPath
        );
    }

    static FString BuildPrinterText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return FString::Printf(
            TEXT("Printer Handoff:\nDirect printer send: LOCKED\nG-code streaming: LOCKED\nSerial ports: NOT TOUCHED\nManifest exports: %d\nManual path: open STL in slicer, inspect, slice, print manually."),
            Ctx->State.ManifestExports
        );
    }

    static FString BuildBackendHealthText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return FString::Printf(
            TEXT("Backend Health:\nUI: alive\nSketch model: %s\nSTL exporter: %s\nDefault app/slicer launch: available\nCAD/STEP sidecar: NOT BUILT\nPrinter bridge: LOCKED\nLast diagnostic: %s"),
            Ctx->State.Sketch.bHasExtrude ? TEXT("ready") : TEXT("waiting"),
            Ctx->State.StlExports > 0 ? TEXT("produced STL") : TEXT("ready"),
            *Ctx->State.LastDiagnostic
        );
    }

    static FString BuildSessionText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return FString::Printf(
            TEXT("Session ID: %s\nStarted: %s\nEvents: %d\nSTL exports: %d\nManifests: %d\nLast action: %s"),
            *Ctx->SessionId,
            *Ctx->SessionStarted,
            Ctx->State.TotalEvents,
            Ctx->State.StlExports,
            Ctx->State.ManifestExports,
            *Ctx->State.LastAction
        );
    }

    static FString BuildEventLogText(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        FString Text = TEXT("Event Log:");

        if (Ctx->State.Events.Num() == 0)
        {
            Text += TEXT("\nWaiting for sketch/export/print-handoff events.");
            return Text;
        }

        for (int32 Index = 0; Index < Ctx->State.Events.Num(); ++Index)
        {
            Text += FString::Printf(TEXT("\n%d. %s"), Index + 1, *Ctx->State.Events[Index]);
        }

        return Text;
    }

    static void RefreshPanels(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        if (Ctx->SelectedAction.IsValid())
        {
            Ctx->SelectedAction->SetText(FText::FromString(FString::Printf(TEXT("Selected action: %s"), *Ctx->State.LastAction)));
        }
        if (Ctx->SessionMetadata.IsValid())
        {
            Ctx->SessionMetadata->SetText(FText::FromString(BuildSessionText(Ctx)));
        }
        if (Ctx->SketchStatus.IsValid())
        {
            Ctx->SketchStatus->SetText(FText::FromString(BuildSketchText(Ctx)));
        }
        if (Ctx->ExportStatus.IsValid())
        {
            Ctx->ExportStatus->SetText(FText::FromString(BuildExportText(Ctx)));
        }
        if (Ctx->PrinterStatus.IsValid())
        {
            Ctx->PrinterStatus->SetText(FText::FromString(BuildPrinterText(Ctx)));
        }
        if (Ctx->BackendHealth.IsValid())
        {
            Ctx->BackendHealth->SetText(FText::FromString(BuildBackendHealthText(Ctx)));
        }
        if (Ctx->BackendInspector.IsValid())
        {
            Ctx->BackendInspector->SetText(FText::FromString(Ctx->State.BackendInspector));
        }
        if (Ctx->EventLog.IsValid())
        {
            Ctx->EventLog->SetText(FText::FromString(BuildEventLogText(Ctx)));
        }
        if (Ctx->Diagnostics.IsValid())
        {
            Ctx->Diagnostics->SetText(FText::FromString(FString::Printf(TEXT("Diagnostics:\n%s"), *Ctx->State.LastDiagnostic)));
        }
    }

    static void AppendTriangle(FString& Stl, const FVector& A, const FVector& B, const FVector& C)
    {
        Stl += TEXT("  facet normal 0 0 0\n");
        Stl += TEXT("    outer loop\n");
        Stl += FString::Printf(TEXT("      vertex %.6f %.6f %.6f\n"), A.X, A.Y, A.Z);
        Stl += FString::Printf(TEXT("      vertex %.6f %.6f %.6f\n"), B.X, B.Y, B.Z);
        Stl += FString::Printf(TEXT("      vertex %.6f %.6f %.6f\n"), C.X, C.Y, C.Z);
        Stl += TEXT("    endloop\n");
        Stl += TEXT("  endfacet\n");
    }

    static FString BuildBoxStl(const FBoxSketch& Sketch)
    {
        const float W = Sketch.WidthMm;
        const float D = Sketch.DepthMm;
        const float H = Sketch.HeightMm;

        const FVector V000(0.0f, 0.0f, 0.0f);
        const FVector V100(W, 0.0f, 0.0f);
        const FVector V110(W, D, 0.0f);
        const FVector V010(0.0f, D, 0.0f);

        const FVector V001(0.0f, 0.0f, H);
        const FVector V101(W, 0.0f, H);
        const FVector V111(W, D, H);
        const FVector V011(0.0f, D, H);

        FString Stl = TEXT("solid CICADA_Sketch_Box\n");

        AppendTriangle(Stl, V000, V110, V100);
        AppendTriangle(Stl, V000, V010, V110);

        AppendTriangle(Stl, V001, V101, V111);
        AppendTriangle(Stl, V001, V111, V011);

        AppendTriangle(Stl, V000, V100, V101);
        AppendTriangle(Stl, V000, V101, V001);

        AppendTriangle(Stl, V010, V011, V111);
        AppendTriangle(Stl, V010, V111, V110);

        AppendTriangle(Stl, V000, V001, V011);
        AppendTriangle(Stl, V000, V011, V010);

        AppendTriangle(Stl, V100, V110, V111);
        AppendTriangle(Stl, V100, V111, V101);

        Stl += TEXT("endsolid CICADA_Sketch_Box\n");
        return Stl;
    }

    static FString BuildPrintManifestJson(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        FString Json;
        Json += TEXT("{\n");
        Json += TEXT("  \"project\": \"CICADA_FORGE_UE\",\n");
        Json += TEXT("  \"phase\": \"003C\",\n");
        Json += FString::Printf(TEXT("  \"session_id\": \"%s\",\n"), *EscapeJson(Ctx->SessionId));
        Json += TEXT("  \"job_type\": \"manual_3d_print_handoff\",\n");
        Json += TEXT("  \"direct_printer_send\": false,\n");
        Json += TEXT("  \"gcode_streaming\": false,\n");
        Json += TEXT("  \"machine_bridge\": \"LOCKED\",\n");
        Json += FString::Printf(TEXT("  \"stl_path\": \"%s\",\n"), *EscapeJson(Ctx->State.LastStlPath));
        Json += TEXT("  \"suggested_slicer_settings\": {\n");
        Json += TEXT("    \"layer_height_mm\": 0.20,\n");
        Json += TEXT("    \"walls\": 3,\n");
        Json += TEXT("    \"infill_percent\": 15,\n");
        Json += TEXT("    \"supports\": \"off for simple box\"\n");
        Json += TEXT("  },\n");
        Json += TEXT("  \"manual_next_step\": \"Open STL in slicer, inspect model, choose material/profile, slice manually, then print manually.\",\n");
        Json += TEXT("  \"box_mm\": {\n");
        Json += FString::Printf(TEXT("    \"width\": %.3f,\n"), Ctx->State.Sketch.WidthMm);
        Json += FString::Printf(TEXT("    \"depth\": %.3f,\n"), Ctx->State.Sketch.DepthMm);
        Json += FString::Printf(TEXT("    \"height\": %.3f\n"), Ctx->State.Sketch.HeightMm);
        Json += TEXT("  }\n");
        Json += TEXT("}\n");
        return Json;
    }

    static FString BuildReceiptJson(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        FString Json;
        Json += TEXT("{\n");
        Json += TEXT("  \"project\": \"CICADA_FORGE_UE\",\n");
        Json += TEXT("  \"phase\": \"003C\",\n");
        Json += FString::Printf(TEXT("  \"session_id\": \"%s\",\n"), *EscapeJson(Ctx->SessionId));
        Json += FString::Printf(TEXT("  \"events\": %d,\n"), Ctx->State.TotalEvents);
        Json += FString::Printf(TEXT("  \"last_action\": \"%s\",\n"), *EscapeJson(Ctx->State.LastAction));
        Json += FString::Printf(TEXT("  \"last_stl_path\": \"%s\",\n"), *EscapeJson(Ctx->State.LastStlPath));
        Json += FString::Printf(TEXT("  \"last_manifest_path\": \"%s\",\n"), *EscapeJson(Ctx->State.LastManifestPath));
        Json += TEXT("  \"direct_printer_send\": false,\n");
        Json += TEXT("  \"machine_bridge\": \"LOCKED\",\n");
        Json += TEXT("  \"cad_sidecar\": \"NOT_BUILT\",\n");
        Json += TEXT("  \"scope\": \"STL export and manual slicer handoff only; no direct printer command\"\n");
        Json += TEXT("}\n");
        return Json;
    }

    static TSharedRef<SWidget> MakeScroll(const TSharedRef<SWidget>& Inner)
    {
        return SNew(SScrollBox)
            + SScrollBox::Slot()
            [
                Inner
            ];
    }

    static TSharedRef<SWidget> MakeLiveCard(const FText& Title, const TSharedRef<STextBlock>& Body)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)
                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock).Text(Title).AutoWrapText(true)
                ]
                + SVerticalBox::Slot().AutoHeight()
                [
                    Body
                ]
            ];
    }

    static TSharedRef<SWidget> MakeCard(const FText& Title, const FText& Body)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)
                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock).Text(Title).AutoWrapText(true)
                ]
                + SVerticalBox::Slot().AutoHeight()
                [
                    SNew(STextBlock).Text(Body).AutoWrapText(true)
                ]
            ];
    }

    static TSharedRef<SWidget> MakePresetButton(
        const FText& Label,
        const float W,
        const float D,
        const float H,
        const FString PresetName,
        const TSharedRef<FForgeLiveContext>& Ctx
    )
    {
        return SNew(SButton)
            .Text(Label)
            .OnClicked_Lambda([W, D, H, PresetName, Ctx]()
            {
                SetPreset(Ctx, W, D, H, PresetName);
                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge sketch preset: %s"), *PresetName);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeValidateButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "ValidateSketch", "[check] Validate sketch + printer fit"))
            .OnClicked_Lambda([Ctx]()
            {
                const bool bGeometryValid = Ctx->State.Sketch.bHasSketch
                    && Ctx->State.Sketch.bHasExtrude
                    && Ctx->State.Sketch.WidthMm > 0.0f
                    && Ctx->State.Sketch.DepthMm > 0.0f
                    && Ctx->State.Sketch.HeightMm > 0.0f;

                const bool bFitsGenericPrinter = Ctx->State.Sketch.WidthMm <= 220.0f
                    && Ctx->State.Sketch.DepthMm <= 220.0f
                    && Ctx->State.Sketch.HeightMm <= 250.0f;

                Ctx->State.Sketch.bValidated = bGeometryValid;
                Ctx->State.Sketch.bBuildVolumePassed = bFitsGenericPrinter;
                Ctx->State.LastAction = TEXT("Validate sketch + printer fit");
                Ctx->State.LastDiagnostic = bGeometryValid && bFitsGenericPrinter
                    ? TEXT("PASS: geometry valid and fits generic 220 x 220 x 250 mm printer volume.")
                    : TEXT("FAIL/WARN: geometry missing or does not fit generic printer volume.");
                Ctx->State.BackendInspector = bGeometryValid
                    ? TEXT("Backend Inspector:\nValidation backend: WORKING\nGeometry: positive dimensions\nPrinter volume check: generic 220x220x250\nDirect printer send: locked")
                    : TEXT("Backend Inspector:\nValidation failed.\nCreate/select a preset box first.");

                AddEvent(Ctx, bGeometryValid && bFitsGenericPrinter ? TEXT("VALIDATION: sketch box PASS") : TEXT("VALIDATION: sketch box FAIL/WARN"));
                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge sketch/printer validation: %s"), (bGeometryValid && bFitsGenericPrinter) ? TEXT("PASS") : TEXT("FAIL_OR_WARN"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeExportStlButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "ExportStl", "[export] Generate STL"))
            .OnClicked_Lambda([Ctx]()
            {
                if (!(Ctx->State.Sketch.bHasSketch && Ctx->State.Sketch.bHasExtrude))
                {
                    Ctx->State.LastDiagnostic = TEXT("STL export blocked: choose/create a sketch box preset first.");
                    Ctx->State.BackendInspector = TEXT("Backend Inspector:\nSTL export blocked.\nReason: no sketch/extrude model.");
                    AddEvent(Ctx, TEXT("STL: export blocked -> no sketch box"));
                    RefreshPanels(Ctx);
                    return FReply::Handled();
                }

                const FString StlDir = FPaths::ProjectSavedDir() / TEXT("CICADAForge/STL");
                IFileManager::Get().MakeDirectory(*StlDir, true);

                const FString Stamp = FDateTime::Now().ToString(TEXT("%Y%m%d_%H%M%S"));
                const FString StlPath = StlDir / FString::Printf(
                    TEXT("CICADA_Box_%.0fx%.0fx%.0f_%s.stl"),
                    Ctx->State.Sketch.WidthMm,
                    Ctx->State.Sketch.DepthMm,
                    Ctx->State.Sketch.HeightMm,
                    *Stamp
                );

                const bool bSaved = FFileHelper::SaveStringToFile(BuildBoxStl(Ctx->State.Sketch), *StlPath);

                if (bSaved)
                {
                    Ctx->State.StlExports += 1;
                    Ctx->State.LastStlPath = StlPath;
                    Ctx->State.LastAction = TEXT("Generate STL");
                    Ctx->State.LastDiagnostic = TEXT("ASCII STL generated locally. Open in slicer and inspect before printing.");
                    Ctx->State.BackendInspector = FString::Printf(
                        TEXT("Backend Inspector:\nSTL exporter: WORKING\nFile: %s\nTriangles: 12\nDirect printer send: locked"),
                        *StlPath
                    );
                    AddEvent(Ctx, FString::Printf(TEXT("STL: generated -> %s"), *StlPath));
                }
                else
                {
                    Ctx->State.LastDiagnostic = TEXT("STL save failed. Check Saved folder permissions.");
                    Ctx->State.BackendInspector = TEXT("Backend Inspector:\nSTL exporter: SAVE FAILED");
                    AddEvent(Ctx, TEXT("STL: save failed"));
                }

                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge STL export: %s"), bSaved ? *StlPath : TEXT("FAILED"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeManifestButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "PrintManifest", "[printer] Save manual print handoff manifest"))
            .OnClicked_Lambda([Ctx]()
            {
                if (Ctx->State.LastStlPath.Equals(TEXT("none")))
                {
                    Ctx->State.LastDiagnostic = TEXT("Print handoff blocked: generate an STL first.");
                    Ctx->State.BackendInspector = TEXT("Backend Inspector:\nManifest blocked.\nReason: no STL yet.");
                    AddEvent(Ctx, TEXT("PRINTER: manifest blocked -> no STL"));
                    RefreshPanels(Ctx);
                    return FReply::Handled();
                }

                const FString ManifestDir = FPaths::ProjectSavedDir() / TEXT("CICADAForge/PrintHandoff");
                IFileManager::Get().MakeDirectory(*ManifestDir, true);

                const FString Stamp = FDateTime::Now().ToString(TEXT("%Y%m%d_%H%M%S"));
                const FString ManifestPath = ManifestDir / FString::Printf(TEXT("CICADA_PrintHandoff_%s.json"), *Stamp);

                const bool bSaved = FFileHelper::SaveStringToFile(BuildPrintManifestJson(Ctx), *ManifestPath);

                if (bSaved)
                {
                    Ctx->State.ManifestExports += 1;
                    Ctx->State.LastManifestPath = ManifestPath;
                    Ctx->State.LastAction = TEXT("Save manual print handoff manifest");
                    Ctx->State.LastDiagnostic = TEXT("Manual print handoff manifest saved. Direct printer send remains locked.");
                    Ctx->State.BackendInspector = FString::Printf(
                        TEXT("Backend Inspector:\nPrint handoff: WORKING\nManifest: %s\nSuggested settings written\nDirect printer send: LOCKED"),
                        *ManifestPath
                    );
                    AddEvent(Ctx, FString::Printf(TEXT("PRINTER: manifest saved -> %s"), *ManifestPath));
                }
                else
                {
                    Ctx->State.LastDiagnostic = TEXT("Print handoff manifest save failed.");
                    AddEvent(Ctx, TEXT("PRINTER: manifest save failed"));
                }

                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge print handoff manifest: %s"), bSaved ? *ManifestPath : TEXT("FAILED"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeOpenStlFolderButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "OpenStlFolder", "[folder] Open STL output folder"))
            .OnClicked_Lambda([Ctx]()
            {
                const FString StlDir = FPaths::ProjectSavedDir() / TEXT("CICADAForge/STL");
                IFileManager::Get().MakeDirectory(*StlDir, true);
                FPlatformProcess::ExploreFolder(*StlDir);

                Ctx->State.LastAction = TEXT("Open STL output folder");
                Ctx->State.LastDiagnostic = TEXT("STL output folder opened.");
                Ctx->State.BackendInspector = FString::Printf(TEXT("Backend Inspector:\nOpened STL folder:\n%s"), *StlDir);

                AddEvent(Ctx, TEXT("FOLDER: opened STL output folder"));
                RefreshPanels(Ctx);

                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeOpenLatestStlButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "OpenLatestStl", "[slicer] Open latest STL in default app"))
            .OnClicked_Lambda([Ctx]()
            {
                if (Ctx->State.LastStlPath.Equals(TEXT("none")))
                {
                    Ctx->State.LastDiagnostic = TEXT("Open STL blocked: generate an STL first.");
                    Ctx->State.BackendInspector = TEXT("Backend Inspector:\nDefault app launch blocked.\nReason: no STL generated yet.");
                    AddEvent(Ctx, TEXT("SLICER: open blocked -> no STL"));
                    RefreshPanels(Ctx);
                    return FReply::Handled();
                }

                FPlatformProcess::LaunchFileInDefaultExternalApplication(*Ctx->State.LastStlPath);

                Ctx->State.LastAction = TEXT("Open latest STL in default app");
                Ctx->State.LastDiagnostic = TEXT("Requested Windows open latest STL in default app/slicer. Inspect before printing.");
                Ctx->State.BackendInspector = FString::Printf(
                    TEXT("Backend Inspector:\nDefault app launch requested for:\n%s\nDirect printer send: still locked"),
                    *Ctx->State.LastStlPath
                );

                AddEvent(Ctx, TEXT("SLICER: requested default app open for latest STL"));
                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge opened latest STL via default app: %s"), *Ctx->State.LastStlPath);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeSaveReceiptButton(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "SaveReceipt", "[receipt] Save export receipt JSON"))
            .OnClicked_Lambda([Ctx]()
            {
                const FString ReceiptDir = FPaths::ProjectSavedDir() / TEXT("CICADAForge/Receipts");
                IFileManager::Get().MakeDirectory(*ReceiptDir, true);

                const FString Stamp = FDateTime::Now().ToString(TEXT("%Y%m%d_%H%M%S"));
                const FString ReceiptPath = ReceiptDir / FString::Printf(TEXT("CICADA_STL_PrintReady_Receipt_%s.json"), *Stamp);

                const bool bSaved = FFileHelper::SaveStringToFile(BuildReceiptJson(Ctx), *ReceiptPath);

                if (bSaved)
                {
                    Ctx->State.ReceiptsWritten += 1;
                    Ctx->State.LastReceiptPath = ReceiptPath;
                    Ctx->State.LastAction = TEXT("Save export receipt JSON");
                    Ctx->State.LastDiagnostic = TEXT("Export receipt saved locally.");
                    AddEvent(Ctx, FString::Printf(TEXT("RECEIPT: saved -> %s"), *ReceiptPath));
                }
                else
                {
                    Ctx->State.LastDiagnostic = TEXT("Receipt save failed.");
                    AddEvent(Ctx, TEXT("RECEIPT: save failed"));
                }

                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge export receipt save: %s"), bSaved ? *ReceiptPath : TEXT("FAILED"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeDebugButton(const FText& Label, const FString Diagnostic, const FString Inspector, const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(Label)
            .OnClicked_Lambda([Diagnostic, Inspector, Ctx]()
            {
                Ctx->State.LastAction = Label.ToString();
                Ctx->State.LastDiagnostic = Diagnostic;
                Ctx->State.BackendInspector = Inspector;

                AddEvent(Ctx, FString::Printf(TEXT("DEBUG: %s"), *Label.ToString()));
                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge debug check: %s"), *Diagnostic);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeProjectButton(const FText& Label, const FString ActionName, const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SButton)
            .Text(Label)
            .OnClicked_Lambda([ActionName, Ctx]()
            {
                Ctx->State.LastAction = ActionName;
                Ctx->State.LastDiagnostic = TEXT("Project UI stub clicked. No export triggered.");
                Ctx->State.BackendInspector = FString::Printf(TEXT("Backend Inspector:\nProject action: %s\nBackend: UI stub\nMachine bridge: locked"), *ActionName);

                AddEvent(Ctx, FString::Printf(TEXT("ACTION: %s -> UI stub"), *ActionName));
                RefreshPanels(Ctx);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge safe action stub clicked: %s"), *ActionName);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeWorkflowControls(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 8)
                [
                    SNew(STextBlock).Text(NSLOCTEXT("CICADAForgeEditorUI", "WorkflowTitle", "Print-Ready Sketch Box Workflow")).AutoWrapText(true)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakePresetButton(NSLOCTEXT("CICADAForgeEditorUI", "PresetSmallTest", "[preset] 20 x 20 x 10 mm test block"), 20.0f, 20.0f, 10.0f, TEXT("20 x 20 x 10 mm test block"), Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakePresetButton(NSLOCTEXT("CICADAForgeEditorUI", "PresetThinPlate", "[preset] 80 x 40 x 4 mm thin plate"), 80.0f, 40.0f, 4.0f, TEXT("80 x 40 x 4 mm thin plate"), Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakePresetButton(NSLOCTEXT("CICADAForgeEditorUI", "PresetBox", "[preset] 80 x 40 x 12 mm box"), 80.0f, 40.0f, 12.0f, TEXT("80 x 40 x 12 mm box"), Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 6, 0, 6)
                [
                    MakeValidateButton(Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeExportStlButton(Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeManifestButton(Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeOpenLatestStlButton(Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeOpenStlFolderButton(Ctx)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 0)
                [
                    MakeSaveReceiptButton(Ctx)
                ]
            ];
    }

    static TSharedRef<SWidget> MakeDebugControls(const TSharedRef<FForgeLiveContext>& Ctx)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 8)
                [
                    SNew(STextBlock).Text(NSLOCTEXT("CICADAForgeEditorUI", "DebugTitle", "Backend Debug Controls")).AutoWrapText(true)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeDebugButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "DebugMap", "[debug] Show backend map"),
                        TEXT("Backend map inspected."),
                        TEXT("Backend Inspector:\nUI shell: WORKING\nPreset sketch model: WORKING\nSTL exporter: WORKING\nDefault app/slicer launch: WORKING / Windows association\nPrint handoff manifest: WORKING\nDirect printer send: LOCKED\nCAD/STEP sidecar: NOT BUILT"),
                        Ctx
                    )
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                [
                    MakeDebugButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "DebugPrinterBoundary", "[debug] Show printer safety boundary"),
                        TEXT("Printer safety boundary inspected."),
                        TEXT("Backend Inspector:\nAllowed: STL export, default app open, handoff manifest.\nBlocked: G-code generation, serial ports, direct print button, machine bridge.\nManual step: inspect STL in slicer, slice manually, print manually."),
                        Ctx
                    )
                ]
            ];
    }

    static TSharedRef<SWidget> MakeCardList(const TArray<FCICADAForgePanelCard>& Cards)
    {
        TSharedRef<SVerticalBox> Box = SNew(SVerticalBox);

        for (const FCICADAForgePanelCard& Card : Cards)
        {
            Box->AddSlot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeCard(Card.Title, Card.Body)
            ];
        }

        return Box;
    }

    static TSharedRef<SWidget> MakeLeftRail(const FCICADAForgeStatusModel& Model, const TSharedRef<FForgeLiveContext>& Ctx)
    {
        TSharedRef<SVerticalBox> Inner =
            SNew(SVerticalBox)

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                SNew(STextBlock).Text(Model.LeftRailTitle).AutoWrapText(true)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
            [
                SNew(STextBlock).Text(FText::FromString(Model.ProjectName)).AutoWrapText(true)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 16)
            [
                SNew(STextBlock).Text(Model.PhaseLabel).AutoWrapText(true)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
            [
                MakeProjectButton(NSLOCTEXT("CICADAForgeEditorUI", "ActionNew", "[stub] New design"), TEXT("New design"), Ctx)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
            [
                MakeProjectButton(NSLOCTEXT("CICADAForgeEditorUI", "ActionGraph", "[stub] Open feature graph"), TEXT("Open feature graph"), Ctx)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 12, 0, 0)
            [
                SNew(SBorder).Padding(8)[Ctx->SelectedAction.ToSharedRef()]
            ];

        return SNew(SBorder).Padding(10)[MakeScroll(Inner)];
    }

    static TSharedRef<SWidget> MakeCentreWorkspace(const FCICADAForgeStatusModel& Model, const TSharedRef<FForgeLiveContext>& Ctx)
    {
        TSharedRef<SVerticalBox> Inner =
            SNew(SVerticalBox)

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
            [
                SNew(STextBlock).Text(Model.WorkspaceTitle).AutoWrapText(true)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeWorkflowControls(Ctx)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "SketchState", "Sketch / Feature State"), Ctx->SketchStatus.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "ExportState", "Export State"), Ctx->ExportStatus.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeDebugControls(Ctx)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "BackendInspector", "Backend Inspector"), Ctx->BackendInspector.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight()
            [
                MakeCardList(Model.WorkspaceCards)
            ];

        return SNew(SBorder).Padding(12)[MakeScroll(Inner)];
    }

    static TSharedRef<SWidget> MakeRightRail(const FCICADAForgeStatusModel& Model, const TSharedRef<FForgeLiveContext>& Ctx)
    {
        TSharedRef<SVerticalBox> Inner =
            SNew(SVerticalBox)

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                SNew(STextBlock).Text(Model.StatusTitle).AutoWrapText(true)
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "BackendHealth", "Backend Health"), Ctx->BackendHealth.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "PrinterStatus", "Printer Handoff State"), Ctx->PrinterStatus.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "Session", "Session Metadata"), Ctx->SessionMetadata.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "Events", "Event Log"), Ctx->EventLog.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 10)
            [
                MakeLiveCard(NSLOCTEXT("CICADAForgeEditorUI", "Diagnostics", "Diagnostics"), Ctx->Diagnostics.ToSharedRef())
            ]

            + SVerticalBox::Slot().AutoHeight()
            [
                MakeCardList(Model.StatusCards)
            ];

        return SNew(SBorder).Padding(10)[MakeScroll(Inner)];
    }

    static TSharedRef<SWidget> MakeBottomLog(const FCICADAForgeStatusModel& Model)
    {
        return SNew(SBorder)
            .Padding(8)
            [
                SNew(STextBlock).Text(Model.BottomLog).AutoWrapText(true)
            ];
    }
}

void FCICADAForgeEditorModule::StartupModule()
{
    FGlobalTabmanager::Get()->RegisterNomadTabSpawner(
        ForgeTabName,
        FOnSpawnTab::CreateRaw(this, &FCICADAForgeEditorModule::SpawnForgeTab)
    )
    .SetDisplayName(LOCTEXT("CICADAForgeTabTitle", "CICADA Forge"))
    .SetTooltipText(LOCTEXT("CICADAForgeTabTooltip", "Open the CICADA Forge workspace shell."))
    .SetMenuType(ETabSpawnerMenuType::Hidden);

    UToolMenus::RegisterStartupCallback(
        FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FCICADAForgeEditorModule::RegisterMenus)
    );

    UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge Editor module started."));
}

void FCICADAForgeEditorModule::ShutdownModule()
{
    if (UToolMenus::IsToolMenuUIEnabled())
    {
        UToolMenus::UnRegisterStartupCallback(this);
        UToolMenus::UnregisterOwner(this);
    }

    FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(ForgeTabName);

    UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge Editor module shut down."));
}

void FCICADAForgeEditorModule::RegisterMenus()
{
    FToolMenuOwnerScoped OwnerScoped(this);

    UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
    FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");

    Section.AddMenuEntry(
        "OpenCICADAForgeWorkspace",
        LOCTEXT("OpenCICADAForgeWorkspaceLabel", "CICADA Forge"),
        LOCTEXT("OpenCICADAForgeWorkspaceTooltip", "Open the CICADA Forge workspace shell."),
        FSlateIcon(),
        FUIAction(FExecuteAction::CreateLambda([]()
        {
            FGlobalTabmanager::Get()->TryInvokeTab(FCICADAForgeEditorModule::ForgeTabName);
        }))
    );
}

TSharedRef<SDockTab> FCICADAForgeEditorModule::SpawnForgeTab(const FSpawnTabArgs& Args)
{
    const FCICADAForgeStatusModel Model = FCICADAForgeStatusModel::MakePhase002DDefault();

    TSharedRef<CICADAForgeEditorUI::FForgeLiveContext> Ctx =
        MakeShared<CICADAForgeEditorUI::FForgeLiveContext>();

    Ctx->SessionId = FGuid::NewGuid().ToString(EGuidFormats::DigitsWithHyphens);
    Ctx->SessionStarted = FDateTime::Now().ToString(TEXT("%Y-%m-%d %H:%M:%S"));

    Ctx->SelectedAction = SNew(STextBlock).Text(NSLOCTEXT("CICADAForgeEditorUI", "InitialSelected", "Selected action: none")).AutoWrapText(true);
    Ctx->SessionMetadata = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildSessionText(Ctx))).AutoWrapText(true);
    Ctx->SketchStatus = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildSketchText(Ctx))).AutoWrapText(true);
    Ctx->ExportStatus = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildExportText(Ctx))).AutoWrapText(true);
    Ctx->PrinterStatus = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildPrinterText(Ctx))).AutoWrapText(true);
    Ctx->BackendHealth = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildBackendHealthText(Ctx))).AutoWrapText(true);
    Ctx->BackendInspector = SNew(STextBlock).Text(FText::FromString(Ctx->State.BackendInspector)).AutoWrapText(true);
    Ctx->EventLog = SNew(STextBlock).Text(FText::FromString(CICADAForgeEditorUI::BuildEventLogText(Ctx))).AutoWrapText(true);
    Ctx->Diagnostics = SNew(STextBlock).Text(FText::FromString(FString::Printf(TEXT("Diagnostics:\n%s"), *Ctx->State.LastDiagnostic))).AutoWrapText(true);

    return SNew(SDockTab)
        .TabRole(ETabRole::NomadTab)
        [
            SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 8)
                [
                    SNew(STextBlock).Text(LOCTEXT("ForgeTitle", "CICADA FORGE")).AutoWrapText(true)
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
                [
                    SNew(STextBlock).Text(Model.PhaseLabel).AutoWrapText(true)
                ]

                + SVerticalBox::Slot().FillHeight(1.0f)
                [
                    SNew(SHorizontalBox)

                    + SHorizontalBox::Slot()
                    .FillWidth(0.22f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeLeftRail(Model, Ctx)
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.52f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeCentreWorkspace(Model, Ctx)
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.26f)
                    [
                        CICADAForgeEditorUI::MakeRightRail(Model, Ctx)
                    ]
                ]

                + SVerticalBox::Slot().AutoHeight().Padding(0, 8, 0, 0)
                [
                    CICADAForgeEditorUI::MakeBottomLog(Model)
                ]
            ]
        ];
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FCICADAForgeEditorModule, CICADAForgeEditor)
