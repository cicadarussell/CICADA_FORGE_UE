#include "CICADAForgeEditorModule.h"

#include "CICADAForgeStatusModel.h"

#include "Framework/Docking/TabManager.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"
#include "Input/Reply.h"
#include "Logging/LogMacros.h"
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

    static TSharedRef<SWidget> MakeActionButton(
        const FText& Label,
        const TSharedRef<STextBlock>& VisibleActionStatus,
        const TSharedRef<STextBlock>& LastActionStatus
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
                "Safe stub only. This updates visible action state, logs an action, and does not modify files, export CAD, or command machines."
            ))
            .OnClicked_Lambda([Label, VisibleActionStatus, LastActionStatus]()
            {
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

                VisibleActionStatus->SetText(LeftStatus);
                LastActionStatus->SetText(RightStatus);

                UE_LOG(LogCICADAForgeEditor, Display, TEXT("CICADA Forge safe action stub clicked: %s"), *Label.ToString());
                return FReply::Handled();
            });
    }

    static TSharedRef<SWidget> MakeActionList(
        const TArray<FText>& Actions,
        const TSharedRef<STextBlock>& VisibleActionStatus,
        const TSharedRef<STextBlock>& LastActionStatus
    )
    {
        TSharedRef<SVerticalBox> ActionBox = SNew(SVerticalBox);

        for (const FText& Action : Actions)
        {
            ActionBox->AddSlot()
            .AutoHeight()
            .Padding(0, 0, 0, 6)
            [
                MakeActionButton(Action, VisibleActionStatus, LastActionStatus)
            ];
        }

        return ActionBox;
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
        const TSharedRef<STextBlock>& LastActionStatus
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
                    MakeActionList(Model.ProjectActions, VisibleActionStatus, LastActionStatus)
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

    static TSharedRef<SWidget> MakeCentreWorkspace(const FCICADAForgeStatusModel& Model)
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
                .FillHeight(1.0f)
                [
                    MakeCardList(Model.WorkspaceCards)
                ]
            ];
    }

    static TSharedRef<SWidget> MakeRightRail(
        const FCICADAForgeStatusModel& Model,
        const TSharedRef<STextBlock>& LastActionStatus
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
                    MakeCard(
                        NSLOCTEXT("CICADAForgeEditorUI", "LastActionCardTitle", "Last Action"),
                        LastActionStatus->GetText()
                    )
                ]

                + SVerticalBox::Slot()
                .AutoHeight()
                .Padding(0, 0, 0, 10)
                [
                    SNew(SBorder)
                    .Padding(10)
                    [
                        LastActionStatus
                    ]
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
                        CICADAForgeEditorUI::MakeLeftRail(Model, VisibleActionStatus, LastActionStatus)
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.56f)
                    .Padding(0, 0, 8, 0)
                    [
                        CICADAForgeEditorUI::MakeCentreWorkspace(Model)
                    ]

                    + SHorizontalBox::Slot()
                    .FillWidth(0.22f)
                    [
                        CICADAForgeEditorUI::MakeRightRail(Model, LastActionStatus)
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
