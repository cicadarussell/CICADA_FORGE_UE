#include "CICADAForgeStatusModel.h"

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakeFromProjectState(const FCICADAForgeProjectState& ProjectState)
{
    FCICADAForgeStatusModel Model;

    Model.ProjectName = ProjectState.ProjectName;
    Model.PhaseLabel = FText::FromString(ProjectState.CurrentPhase);

    Model.LeftRailTitle = NSLOCTEXT("CICADAForgeStatusModel", "LeftRailTitle", "PROJECT");
    Model.WorkspaceTitle = NSLOCTEXT("CICADAForgeStatusModel", "WorkspaceTitle", "FORGE WORKSPACE");
    Model.StatusTitle = NSLOCTEXT("CICADAForgeStatusModel", "StatusTitle", "STATUS");

    Model.BottomLog = FText::FromString(
        FString::Printf(
            TEXT("LOG: Phase 003G headless forge control tower is live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "HeadlessCardTitle", "Headless Control Tower"),
        NSLOCTEXT("CICADAForgeStatusModel", "HeadlessCardBody", "Phase 003G adds a no-Unreal master CLI for doctor/full-check/demo/report/inventory. The software can now prove the STL pipeline without opening the editor every time.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "DebugCardTitle", "Debugging Tools"),
        NSLOCTEXT("CICADAForgeStatusModel", "DebugCardBody", "New tools check repo state, file presence, Python tooling, artifacts, manifests, STL quality, reports, slicer discovery, and machine-safety locks.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Automation Boundary"),
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardBody", "Allowed: headless STL generation, quality reports, manifests, inventory, local HTML dashboard. Blocked: serial ports, G-code streaming, direct printer send.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "ProjectStateCardTitle", "Project State"),
        FText::FromString(FString::Printf(TEXT("Repo: %s\nPhase source: Config/CICADAForgeState.ini"), *ProjectState.RepoPath))
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
        NSLOCTEXT("CICADAForgeStatusModel", "BoundaryCardTitle", "Safety Boundary"),
        FText::FromString(
            ProjectState.bMachineCommandsLocked
                ? TEXT("Machine commands are locked. Headless diagnostics are allowed; printer automation is not.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
