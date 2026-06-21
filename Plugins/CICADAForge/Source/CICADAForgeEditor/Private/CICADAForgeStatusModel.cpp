#include "CICADAForgeStatusModel.h"

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakeFromProjectState(const FCICADAForgeProjectState& ProjectState)
{
    FCICADAForgeStatusModel Model;

    Model.ProjectName = ProjectState.ProjectName;
    Model.PhaseLabel = FText::FromString(ProjectState.CurrentPhase);

    Model.LeftRailTitle = NSLOCTEXT(
        "CICADAForgeStatusModel",
        "LeftRailTitle",
        "PROJECT"
    );

    Model.WorkspaceTitle = NSLOCTEXT(
        "CICADAForgeStatusModel",
        "WorkspaceTitle",
        "FORGE WORKSPACE"
    );

    Model.StatusTitle = NSLOCTEXT(
        "CICADAForgeStatusModel",
        "StatusTitle",
        "STATUS"
    );

    Model.BottomLog = FText::FromString(
        FString::Printf(
            TEXT("LOG: Phase 002I session metadata panel is live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "GraphCardTitle", "Feature Graph Placeholder"),
        NSLOCTEXT("CICADAForgeStatusModel", "GraphCardBody", "Future home of parametric design intent: dimensions, primitives, operations, constraints, validation state, and export receipts.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "PreviewCardTitle", "Preview Placeholder"),
        NSLOCTEXT("CICADAForgeStatusModel", "PreviewCardBody", "Unreal viewport/preview integration comes later. Manufacturing truth will still come from the feature graph and CAD sidecar, not raw editor mesh vibes.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "GateCardTitle", "Current Gate"),
        NSLOCTEXT("CICADAForgeStatusModel", "GateCardBody", "Gate: prove session metadata updates during the local Forge run. No persistence, CAD export, sidecar calls, or machine control in this phase.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "ProjectStateCardTitle", "Project State"),
        FText::FromString(
            FString::Printf(
                TEXT("Repo: %s\nPhase source: Config/CICADAForgeState.ini"),
                *ProjectState.RepoPath
            )
        )
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "EvidenceCardTitle", "Evidence"),
        FText::FromString(ProjectState.EvidenceState)
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SidecarCardTitle", "CAD Sidecar"),
        FText::FromString(ProjectState.CadSidecarState)
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "MachineCardTitle", "Machine Bridge"),
        FText::FromString(ProjectState.MachineBridgeState)
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Safety Boundary"),
        FText::FromString(
            ProjectState.bMachineCommandsLocked
                ? TEXT("Machine commands are locked. Future machine actions require dry run, preview, explicit approval, and logs.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
