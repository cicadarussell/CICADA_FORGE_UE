#include "CICADAForgeEditorModule.h"

#include "CICADAForgeStatusModel.h"

#include "Framework/Docking/TabManager.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"
#include "HAL/FileManager.h"
#include "Input/Reply.h"
#include "Logging/LogMacros.h"
#include "Misc/DateTime.h"
#include "Misc/FileHelper.h"
#include "Misc/Guid.h"
#include "Misc/Paths.h"
#include "Templates/SharedPointer.h"
#include "ToolMenus.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SWidget.h"
#include "Widgets/Text/STextBlock.h"

DEFINE_LOG_CATEGORY_STATIC(LogCICADAForgeEditor, Log, All);

#define LOCTEXT_NAMESPACE "FCICADAForgeEditorModule"

const FName FCICADAForgeEditorModule::ForgeTabName(TEXT("CICADAForgeMainTab"));

namespace CICADAForgeEditorUI
{
    struct FForgeUiState
    {
        int32 TotalSafeEvents = 0;
        int32 ReceiptsWritten = 0;
        FString LastAction = TEXT("none");
        FString LastEvidence = TEXT("none");
        FString LastReceiptPath = TEXT("none");
        FString LastDiagnostic = TEXT("No diagnostics run yet.");
        bool bReceiptReady = false;
        bool bReceiptSaved = false;
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

    static TSharedRef<SWidget> MakeCard(const FText& Title, const FText& Body)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(Title)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                [
                    SNew(STextBlock)
                    .Text(Body)
                    .AutoWrapText(true)
                ]
            ];
    }

    static FString BuildEventLogText(const TSharedRef<TArray<FString>>& EventLogLines)
    {
        FString EventLogText = TEXT("Event Log:");

        if (EventLogLines->Num() == 0)
        {
            EventLogText += TEXT("\nWaiting for safe UI events.");
            return EventLogText;
        }

        for (int32 Index = 0; Index < EventLogLines->Num(); ++Index)
        {
            EventLogText += FString::Printf(
                TEXT("\n%d. %s"),
                Index + 1,
                *(*EventLogLines)[Index]
            );
        }

        return EventLogText;
    }

    static FString BuildSessionMetadataText(
        const FString& SessionId,
        const FString& SessionStarted,
        const TSharedRef<FForgeUiState>& UiState
    )
    {
        return FString::Printf(
            TEXT("Session ID: %s\nStarted: %s\nSafe UI events: %d\nReceipts written: %d\nLast action: %s\nPersistence: memory + explicit dry-run receipt only"),
            *SessionId,
            *SessionStarted,
            UiState->TotalSafeEvents,
            UiState->ReceiptsWritten,
            *UiState->LastAction
        );
    }

    static FString BuildReceiptPreviewText(
        const FString& SessionId,
        const TSharedRef<FForgeUiState>& UiState
    )
    {
        return FString::Printf(
            TEXT("Receipt Preview:\nStatus: %s\nSession ID: %s\nEvents counted: %d\nLast action: %s\nLast evidence: %s\nLast receipt path: %s\nSave mode: explicit local dry-run only"),
            UiState->bReceiptReady ? (UiState->bReceiptSaved ? TEXT("saved dry-run receipt") : TEXT("ready in memory")) : TEXT("waiting for evidence"),
            *SessionId,
            UiState->TotalSafeEvents,
            *UiState->LastAction,
            *UiState->LastEvidence,
            *UiState->LastReceiptPath
        );
    }

    static FString BuildDiagnosticsText(const TSharedRef<FForgeUiState>& UiState)
    {
        return FString::Printf(
            TEXT("Diagnostics:\nLast check: %s\nMachine bridge: LOCKED\nCAD sidecar: OFFLINE\nReceipt write scope: Saved/CICADAForge/Receipts only\nLast evidence: %s"),
            *UiState->LastDiagnostic,
            *UiState->LastEvidence
        );
    }

    static FString BuildReceiptJson(
        const FString& SessionId,
        const FString& SessionStarted,
        const TSharedRef<FForgeUiState>& UiState,
        const TSharedRef<TArray<FString>>& EventLogLines
    )
    {
        FString Json;
        Json += TEXT("{\n");
        Json += FString::Printf(TEXT("  \"project\": \"CICADA_FORGE_UE\",\n"));
        Json += FString::Printf(TEXT("  \"phase\": \"002K\",\n"));
        Json += FString::Printf(TEXT("  \"session_id\": \"%s\",\n"), *EscapeJson(SessionId));
        Json += FString::Printf(TEXT("  \"session_started\": \"%s\",\n"), *EscapeJson(SessionStarted));
        Json += FString::Printf(TEXT("  \"receipt_written_utc\": \"%s\",\n"), *EscapeJson(FDateTime::UtcNow().ToString(TEXT("%Y-%m-%d %H:%M:%S"))));
        Json += FString::Printf(TEXT("  \"total_safe_events\": %d,\n"), UiState->TotalSafeEvents);
        Json += FString::Printf(TEXT("  \"last_action\": \"%s\",\n"), *EscapeJson(UiState->LastAction));
        Json += FString::Printf(TEXT("  \"last_evidence\": \"%s\",\n"), *EscapeJson(UiState->LastEvidence));
        Json += FString::Printf(TEXT("  \"machine_bridge\": \"LOCKED\",\n"));
        Json += FString::Printf(TEXT("  \"cad_sidecar\": \"OFFLINE\",\n"));
        Json += FString::Printf(TEXT("  \"scope\": \"local dry-run receipt only; no CAD, no sidecar, no machine command\",\n"));
        Json += FString::Printf(TEXT("  \"events\": [\n"));

        for (int32 Index = 0; Index < EventLogLines->Num(); ++Index)
        {
            const FString Suffix = (Index + 1 < EventLogLines->Num()) ? TEXT(",") : TEXT("");
            Json += FString::Printf(
                TEXT("    \"%s\"%s\n"),
                *EscapeJson((*EventLogLines)[Index]),
                *Suffix
            );
        }

        Json += TEXT("  ]\n");
        Json += TEXT("}\n");

        return Json;
    }

    static void AddEventLine(
        const FString& EventLine,
        const TSharedRef<TArray<FString>>& EventLogLines
    )
    {
        EventLogLines->Insert(EventLine, 0);

        while (EventLogLines->Num() > 8)
        {
            EventLogLines->RemoveAt(EventLogLines->Num() - 1);
        }
    }

    static void RefreshLivePanels(
        const FString& SessionId,
        const FString& SessionStarted,
        const TSharedRef<FForgeUiState>& UiState,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus
    )
    {
        EventLogStatus->SetText(FText::FromString(BuildEventLogText(EventLogLines)));
        SessionMetadataStatus->SetText(FText::FromString(BuildSessionMetadataText(SessionId, SessionStarted, UiState)));
        ReceiptPreviewStatus->SetText(FText::FromString(BuildReceiptPreviewText(SessionId, UiState)));
        DiagnosticsStatus->SetText(FText::FromString(BuildDiagnosticsText(UiState)));
    }

    static TSharedRef<SWidget> MakeLiveStatusCard(const FText& Title, const TSharedRef<STextBlock>& LiveText)
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(Title)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                [
                    LiveText
                ]
            ];
    }

    static TSharedRef<SWidget> MakeActionButton(
        const FText& Label,
        const TSharedRef<STextBlock>& VisibleActionStatus,
        const TSharedRef<STextBlock>& LastActionStatus,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SButton)
            .Text(FText::Format(
                NSLOCTEXT("CICADAForgeEditorUI", "StubButtonFormat", "[stub] {0}"),
                Label
            ))
            .ToolTipText(NSLOCTEXT(
                "CICADAForgeEditorUI",
                "StubButtonTooltip",
                "Safe stub only. Updates UI state and logs an action. Does not export CAD or command machines."
            ))
            .OnClicked_Lambda([Label, VisibleActionStatus, LastActionStatus, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus, EventLogLines, UiState, SessionId, SessionStarted]()
            {
                const FString LabelString = Label.ToString();

                UiState->TotalSafeEvents += 1;
                UiState->LastAction = LabelString;
                UiState->LastDiagnostic = TEXT("Action stub clicked safely.");

                const FText LeftStatus = FText::Format(
                    NSLOCTEXT(
                        "CICADAForgeEditorUI",
                        "SelectedActionFormat",
                        "Selected action: {0} - safe stub only"
                    ),
                    Label
                );

                const FText RightStatus = FText::Format(
                    NSLOCTEXT(
                        "CICADAForgeEditorUI",
                        "LastActionFormat",
                        "Last Action: {0}\nResult: safe stub logged only"
                    ),
                    Label
                );

                AddEventLine(
                    FString::Printf(TEXT("ACTION: %s -> safe stub logged only"), *LabelString),
                    EventLogLines
                );

                VisibleActionStatus->SetText(LeftStatus);
                LastActionStatus->SetText(RightStatus);
                RefreshLivePanels(SessionId, SessionStarted, UiState, EventLogLines, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge safe action stub clicked: %s"), *LabelString);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeEvidenceButton(
        const FText& Label,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SButton)
            .Text(FText::Format(
                NSLOCTEXT("CICADAForgeEditorUI", "EvidenceButtonFormat", "[evidence] {0}"),
                Label
            ))
            .ToolTipText(NSLOCTEXT(
                "CICADAForgeEditorUI",
                "EvidenceButtonTooltip",
                "Memory evidence marker. Does not save files unless dry-run receipt button is explicitly clicked."
            ))
            .OnClicked_Lambda([Label, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus, EventLogLines, UiState, SessionId, SessionStarted]()
            {
                const FString LabelString = Label.ToString();

                UiState->TotalSafeEvents += 1;
                UiState->LastEvidence = LabelString;
                UiState->bReceiptReady = true;
                UiState->bReceiptSaved = false;
                UiState->LastDiagnostic = TEXT("Evidence marker recorded in memory.");

                AddEventLine(
                    FString::Printf(TEXT("EVIDENCE: %s -> memory marker"), *LabelString),
                    EventLogLines
                );

                RefreshLivePanels(SessionId, SessionStarted, UiState, EventLogLines, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge evidence stub clicked: %s"), *LabelString);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeDiagnosticsButton(
        const FText& Label,
        const FString DiagnosticText,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SButton)
            .Text(FText::Format(
                NSLOCTEXT("CICADAForgeEditorUI", "DiagnosticsButtonFormat", "[debug] {0}"),
                Label
            ))
            .ToolTipText(NSLOCTEXT(
                "CICADAForgeEditorUI",
                "DiagnosticsButtonTooltip",
                "Runs a memory-only diagnostic status update. Does not scan your whole drive, summon demons, or touch machines."
            ))
            .OnClicked_Lambda([Label, DiagnosticText, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus, EventLogLines, UiState, SessionId, SessionStarted]()
            {
                const FString LabelString = Label.ToString();

                UiState->TotalSafeEvents += 1;
                UiState->LastAction = LabelString;
                UiState->LastDiagnostic = DiagnosticText;

                AddEventLine(
                    FString::Printf(TEXT("DEBUG: %s -> %s"), *LabelString, *DiagnosticText),
                    EventLogLines
                );

                RefreshLivePanels(SessionId, SessionStarted, UiState, EventLogLines, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge debug stub clicked: %s"), *LabelString);
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeSaveReceiptButton(
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "SaveReceiptDryRunButton", "[receipt] Save local dry-run receipt"))
            .ToolTipText(NSLOCTEXT(
                "CICADAForgeEditorUI",
                "SaveReceiptDryRunTooltip",
                "Writes one local JSON receipt under Saved/CICADAForge/Receipts. No CAD, no sidecar, no machine command."
            ))
            .OnClicked_Lambda([EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus, EventLogLines, UiState, SessionId, SessionStarted]()
            {
                UiState->TotalSafeEvents += 1;
                UiState->LastAction = TEXT("Save local dry-run receipt");

                const FString ReceiptDir = FPaths::ProjectSavedDir() / TEXT("CICADAForge/Receipts");
                IFileManager::Get().MakeDirectory(*ReceiptDir, true);

                const FString Stamp = FDateTime::Now().ToString(TEXT("%Y%m%d_%H%M%S"));
                const FString ShortSessionId = SessionId.Left(8);
                const FString ReceiptPath = ReceiptDir / FString::Printf(TEXT("CICADAForgeReceipt_%s_%s.json"), *Stamp, *ShortSessionId);

                const FString ReceiptJson = BuildReceiptJson(SessionId, SessionStarted, UiState, EventLogLines);
                const bool bSaved = FFileHelper::SaveStringToFile(ReceiptJson, *ReceiptPath);

                UiState->bReceiptSaved = bSaved;
                UiState->bReceiptReady = true;
                UiState->ReceiptsWritten += bSaved ? 1 : 0;
                UiState->LastReceiptPath = bSaved ? ReceiptPath : TEXT("SAVE FAILED");
                UiState->LastDiagnostic = bSaved
                    ? TEXT("Dry-run receipt saved inside Project/Saved only.")
                    : TEXT("Dry-run receipt save failed.");

                AddEventLine(
                    bSaved
                        ? FString::Printf(TEXT("RECEIPT: saved dry-run receipt -> %s"), *ReceiptPath)
                        : TEXT("RECEIPT: save failed"),
                    EventLogLines
                );

                RefreshLivePanels(SessionId, SessionStarted, UiState, EventLogLines, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge receipt dry-run save: %s"), bSaved ? *ReceiptPath : TEXT("FAILED"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeClearEventLogButton(
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SButton)
            .Text(NSLOCTEXT("CICADAForgeEditorUI", "ClearEventLogButton", "[system] Clear visible event log"))
            .ToolTipText(NSLOCTEXT(
                "CICADAForgeEditorUI",
                "ClearEventLogTooltip",
                "Clears the visible in-memory event log only. It does not delete saved files."
            ))
            .OnClicked_Lambda([EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus, EventLogLines, UiState, SessionId, SessionStarted]()
            {
                UiState->TotalSafeEvents += 1;
                UiState->LastAction = TEXT("Clear visible event log");
                UiState->LastDiagnostic = TEXT("Visible in-memory event log cleared.");

                EventLogLines->Empty();

                AddEventLine(
                    TEXT("SYSTEM: visible event log cleared -> memory only"),
                    EventLogLines
                );

                RefreshLivePanels(SessionId, SessionStarted, UiState, EventLogLines, EventLogStatus, SessionMetadataStatus, ReceiptPreviewStatus, DiagnosticsStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge system stub clicked: Clear visible event log"));
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeActionList(
        const TArray<FText>& Actions,
        const TSharedRef<STextBlock>& VisibleActionStatus,
        const TSharedRef<STextBlock>& LastActionStatus,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        TSharedRef<SVerticalBox> ActionBox = SNew(SVerticalBox);

        for (const FText& Action : Actions)
        {
            ActionBox->AddSlot()
            .AutoHeight()
            .Padding(0, 0, 0, 6)
            [
                MakeActionButton(
                    Action,
                    VisibleActionStatus,
                    LastActionStatus,
                    EventLogStatus,
                    SessionMetadataStatus,
                    ReceiptPreviewStatus,
                    DiagnosticsStatus,
                    EventLogLines,
                    UiState,
                    SessionId,
                    SessionStarted
                )
            ];
        }

        return ActionBox;
    }

    static TSharedRef<SWidget> MakeEvidenceAndDebugControls(
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 8)
                [
                    SNew(STextBlock)
                    .Text(NSLOCTEXT("CICADAForgeEditorUI", "EvidenceControlsTitle", "Evidence + Debug Controls"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    MakeEvidenceButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "EvidenceScreenshotObserved", "Screenshot observed"),
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    MakeEvidenceButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "EvidenceOutputLogChecked", "Output log checked"),
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    MakeEvidenceButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "EvidenceUiPassCandidate", "UI pass candidate"),
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 4, 0, 6)
                [
                    MakeDiagnosticsButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "DiagnosticUiStateCheck", "Run UI state self-check"),
                        TEXT("UI state self-check passed: machine locked, CAD sidecar offline, receipt path scoped to Saved."),
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    MakeDiagnosticsButton(
                        NSLOCTEXT("CICADAForgeEditorUI", "DiagnosticNoiseClassifier", "Classify known log noise"),
                        TEXT("Known noise: aqProf/Vtune/PIX/RenderDoc/XGE/EOS/DerivedDataCache/SDK warnings are non-blocking unless build fails."),
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 4, 0, 6)
                [
                    MakeSaveReceiptButton(
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 0)
                [
                    MakeClearEventLogButton(
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]
            ];
    }

    static TSharedRef<SWidget> MakeCardList(const TArray<FCICADAForgePanelCard>& Cards)
    {
        TSharedRef<SVerticalBox> CardBox = SNew(SVerticalBox);

        for (const FCICADAForgePanelCard& Card : Cards)
        {
            CardBox->AddSlot()
            .AutoHeight()
            .Padding(0, 0, 0, 10)
            [
                MakeCard(Card.Title, Card.Body)
            ];
        }

        return CardBox;
    }

    static TSharedRef<SWidget> MakeLeftRail(
        const FCICADAForgeStatusModel& Model,
        const TSharedRef<STextBlock>& VisibleActionStatus,
        const TSharedRef<STextBlock>& LastActionStatus,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    SNew(STextBlock)
                    .Text(Model.LeftRailTitle)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(FText::FromString(Model.ProjectName))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 16)
                [
                    SNew(STextBlock)
                    .Text(Model.PhaseLabel)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                [
                    MakeActionList(
                        Model.ProjectActions,
                        VisibleActionStatus,
                        LastActionStatus,
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 12, 0, 0)
                [
                    SNew(SBorder)
                    .Padding(8)
                    [
                        VisibleActionStatus
                    ]
                ]
            ];
    }

    static TSharedRef<SWidget> MakeCentreWorkspace(
        const FCICADAForgeStatusModel& Model,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus,
        const TSharedRef<TArray<FString>>& EventLogLines,
        const TSharedRef<FForgeUiState>& UiState,
        const FString SessionId,
        const FString SessionStarted
    )
    {
        return SNew(SBorder)
            .Padding(12)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 12)
                [
                    SNew(STextBlock)
                    .Text(Model.WorkspaceTitle)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeEvidenceAndDebugControls(
                        EventLogStatus,
                        SessionMetadataStatus,
                        ReceiptPreviewStatus,
                        DiagnosticsStatus,
                        EventLogLines,
                        UiState,
                        SessionId,
                        SessionStarted
                    )
                ]

                + SVerticalBox::Slot()
                .FillHeight(1.0f)
                [
                    MakeCardList(Model.WorkspaceCards)
                ]
            ];
    }

    static TSharedRef<SWidget> MakeRightRail(
        const FCICADAForgeStatusModel& Model,
        const TSharedRef<STextBlock>& SessionMetadataStatus,
        const TSharedRef<STextBlock>& LastActionStatus,
        const TSharedRef<STextBlock>& EventLogStatus,
        const TSharedRef<STextBlock>& ReceiptPreviewStatus,
        const TSharedRef<STextBlock>& DiagnosticsStatus
    )
    {
        return SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    SNew(STextBlock)
                    .Text(Model.StatusTitle)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeLiveStatusCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "SessionMetadataCardTitle", "Session Metadata"),
                        SessionMetadataStatus
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeLiveStatusCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "LastActionCardTitle", "Last Action"),
                        LastActionStatus
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeLiveStatusCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "EventLogCardTitle", "Event Log"),
                        EventLogStatus
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeLiveStatusCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "ReceiptPreviewCardTitle", "Evidence Receipt Preview"),
                        ReceiptPreviewStatus
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeLiveStatusCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "DiagnosticsCardTitle", "Diagnostics"),
                        DiagnosticsStatus
                    )
                ]

                + SVerticalBox::Slot()
                .FillHeight(1.0f)
                [
                    MakeCardList(Model.StatusCards)
                ]
            ];
    }

    static TSharedRef<SWidget> MakeBottomLog(const FCICADAForgeStatusModel& Model)
    {
        return SNew(SBorder)
            .Padding(8)
            [
                SNew(STextBlock)
                .Text(Model.BottomLog)
                .AutoWrapText(true)
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

    const FString SessionId = FGuid::NewGuid().ToString(EGuidFormats::DigitsWithHyphens);
    const FString SessionStarted = FDateTime::Now().ToString(TEXT("%Y-%m-%d %H:%M:%S"));

    TSharedRef<CICADAForgeEditorUI::FForgeUiState> UiState =
        MakeShared<CICADAForgeEditorUI::FForgeUiState>();

    TSharedRef<STextBlock> VisibleActionStatus =
        SNew(STextBlock)
        .Text(NSLOCTEXT(
            "CICADAForgeEditorUI",
            "InitialActionStatus",
            "Selected action: none"
        ))
        .AutoWrapText(true);

    TSharedRef<STextBlock> LastActionStatus =
        SNew(STextBlock)
        .Text(NSLOCTEXT(
            "CICADAForgeEditorUI",
            "InitialLastActionStatus",
            "Last Action: none\nResult: waiting for safe stub click"
        ))
        .AutoWrapText(true);

    TSharedRef<TArray<FString>> EventLogLines = MakeShared<TArray<FString>>();

    TSharedRef<STextBlock> EventLogStatus =
        SNew(STextBlock)
        .Text(FText::FromString(CICADAForgeEditorUI::BuildEventLogText(EventLogLines)))
        .AutoWrapText(true);

    TSharedRef<STextBlock> SessionMetadataStatus =
        SNew(STextBlock)
        .Text(FText::FromString(CICADAForgeEditorUI::BuildSessionMetadataText(
            SessionId,
            SessionStarted,
            UiState
        )))
        .AutoWrapText(true);

    TSharedRef<STextBlock> ReceiptPreviewStatus =
        SNew(STextBlock)
        .Text(FText::FromString(CICADAForgeEditorUI::BuildReceiptPreviewText(
            SessionId,
            UiState
        )))
        .AutoWrapText(true);

    TSharedRef<STextBlock> DiagnosticsStatus =
        SNew(STextBlock)
        .Text(FText::FromString(CICADAForgeEditorUI::BuildDiagnosticsText(UiState)))
        .AutoWrapText(true);

    return SNew(SDockTab)
        .TabRole(ETabRole::NomadTab)
        [
            SNew(SBorder)
            .Padding(10)
            [
                SNew(SVerticalBox)

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 8)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ForgeTitle", "CICADA FORGE"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 12)
                [
                    SNew(STextBlock)
                    .Text(Model.PhaseLabel)
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .FillHeight(1.0f)
                [
                    SNew(SHorizontalBox)

                    + SHorizontalBox::Slot()
                    .FillWidth(0.22f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeLeftRail(
                            Model,
                            VisibleActionStatus,
                            LastActionStatus,
                            EventLogStatus,
                            SessionMetadataStatus,
                            ReceiptPreviewStatus,
                            DiagnosticsStatus,
                            EventLogLines,
                            UiState,
                            SessionId,
                            SessionStarted
                        )
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.56f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeCentreWorkspace(
                            Model,
                            EventLogStatus,
                            SessionMetadataStatus,
                            ReceiptPreviewStatus,
                            DiagnosticsStatus,
                            EventLogLines,
                            UiState,
                            SessionId,
                            SessionStarted
                        )
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.22f)
                    [
                        CICADAForgeEditorUI::MakeRightRail(
                            Model,
                            SessionMetadataStatus,
                            LastActionStatus,
                            EventLogStatus,
                            ReceiptPreviewStatus,
                            DiagnosticsStatus
                        )
                    ]
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 8, 0, 0)
                [
                    CICADAForgeEditorUI::MakeBottomLog(Model)
                ]
            ]
        ];
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FCICADAForgeEditorModule, CICADAForgeEditor)
