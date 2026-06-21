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
            TEXT("LOG: Phase 003H local artifact dashboard and control room are live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "DashboardCardTitle", "Local Dashboard"),
        NSLOCTEXT("CICADAForgeStatusModel", "DashboardCardBody", "Phase 003H adds a no-Unreal dashboard over artifacts: latest jobs, STLs, reports, manifests, receipts, run reports, safety state, and recommended next command.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "ControlRoomCardTitle", "Control Room"),
        NSLOCTEXT("CICADAForgeStatusModel", "ControlRoomCardBody", "The dashboard is generated from local files only. It does not call a printer, does not stream G-code, and does not pretend the CAD sidecar exists.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Automation Boundary"),
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardBody", "Allowed: dashboard generation, artifact inspection, headless full-check, STL reports. Blocked: serial ports, G-code streaming, direct printer send.")
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
                ? TEXT("Machine commands are locked. Dashboard diagnostics are allowed; printer automation is not.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
