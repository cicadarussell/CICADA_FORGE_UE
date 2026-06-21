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
            TEXT("LOG: Phase 003I CAD sidecar contract and exact-geometry boundary are live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "CadContractCardTitle", "CAD Sidecar Contract"),
        NSLOCTEXT("CICADAForgeStatusModel", "CadContractCardBody", "Phase 003I defines the exact-geometry boundary: JSON part schema, mechanical examples, validation, reports, and optional CadQuery/FreeCAD STEP export if an engine exists.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "NoFakeStepCardTitle", "No Fake STEP Rule"),
        NSLOCTEXT("CICADAForgeStatusModel", "NoFakeStepCardBody", "If no exact CAD engine is detected, the sidecar writes a blocked export report instead of pretending triangles are STEP. Astonishingly, honesty is cheaper than haunted manufacturing.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Automation Boundary"),
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardBody", "Allowed: validate part intent, generate reports, optional local STEP/STL export. Blocked: serial ports, G-code streaming, printer/CNC/pick-and-place commands.")
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
                ? TEXT("Machine commands are locked. CAD sidecar is local/export-only.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
