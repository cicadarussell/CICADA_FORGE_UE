#include "CICADAForgeEditorModule.h"

#include "Framework/Docking/TabManager.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"
#include "Logging/LogMacros.h"
#include "ToolMenus.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SWidget.h"
#include "Widgets/Text/STextBlock.h"

DEFINE_LOG_CATEGORY_STATIC(LogCICADAForgeEditor, Log, All);

#define LOCTEXT_NAMESPACE "FCICADAForgeEditorModule"

const FName FCICADAForgeEditorModule::ForgeTabName(TEXT("CICADAForgeMainTab"));

namespace CICADAForgeEditorUI
{
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

    static TSharedRef<SWidget> MakeLeftRail()
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
                    .Text(LOCTEXT("LeftRailTitle", "PROJECT"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ProjectStatus", "CICADA_FORGE_UE"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 16)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ProjectPhase", "Phase 002B: structured shell"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ActionNewDesign", "[stub] New design"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ActionOpenGraph", "[stub] Open feature graph"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 6)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ActionRunValidation", "[stub] Run validation"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("ActionExportProof", "[stub] Export proof receipt"))
                    .AutoWrapText(true)
                ]
            ];
    }

    static TSharedRef<SWidget> MakeCentreWorkspace()
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
                    .Text(LOCTEXT("WorkspaceTitle", "FORGE WORKSPACE"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeCard(
                        LOCTEXT("GraphCardTitle", "Feature Graph Placeholder"),
                        LOCTEXT("GraphCardBody", "Future home of parametric design intent: dimensions, primitives, operations, constraints, validation state, and export receipts.")
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeCard(
                        LOCTEXT("ViewportCardTitle", "Preview Placeholder"),
                        LOCTEXT("ViewportCardBody", "Unreal viewport/preview integration comes later. Manufacturing truth will still come from the feature graph and CAD sidecar, not raw editor mesh vibes.")
                    )
                ]

                + SVerticalBox::Slot()
                .FillHeight(1.0f)
                [
                    MakeCard(
                        LOCTEXT("PhaseGateTitle", "Current Gate"),
                        LOCTEXT("PhaseGateBody", "Gate: prove structured shell loads. No CAD export, no machine control, no sidecar calls in this phase.")
                    )
                ]
            ];
    }

    static TSharedRef<SWidget> MakeRightRail()
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
                    .Text(LOCTEXT("RightRailTitle", "STATUS"))
                    .AutoWrapText(true)
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeCard(
                        LOCTEXT("EvidenceCardTitle", "Evidence"),
                        LOCTEXT("EvidenceCardBody", "Manual evidence logging active. Automated screenshots and receipts are later.")
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeCard(
                        LOCTEXT("SidecarCardTitle", "CAD Sidecar"),
                        LOCTEXT("SidecarCardBody", "Offline. Phase 005 target. No requests sent.")
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    MakeCard(
                        LOCTEXT("MachineCardTitle", "Machine Bridge"),
                        LOCTEXT("MachineCardBody", "Locked. No physical machine commands exist in V0 shell.")
                    )
                ]

                + SVerticalBox::Slot()
                .FillHeight(1.0f)
                [
                    MakeCard(
                        LOCTEXT("SafetyCardTitle", "Safety Boundary"),
                        LOCTEXT("SafetyCardBody", "All machine actions require future dry run, preview, explicit approval, and logs.")
                    )
                ]
            ];
    }

    static TSharedRef<SWidget> MakeBottomLog()
    {
        return SNew(SBorder)
            .Padding(8)
            [
                SNew(STextBlock)
                .Text(LOCTEXT("BottomLogText", "LOG: Phase 002B shell loaded. Next target: live status model and panel data source."))
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
                    .Text(LOCTEXT("ForgeSubtitle", "Phase 002B: structured cockpit shell is alive."))
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
                        CICADAForgeEditorUI::MakeLeftRail()
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.56f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeCentreWorkspace()
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.22f)
                    [
                        CICADAForgeEditorUI::MakeRightRail()
                    ]
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 8, 0, 0)
                [
                    CICADAForgeEditorUI::MakeBottomLog()
                ]
            ]
        ];
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FCICADAForgeEditorModule, CICADAForgeEditor)
