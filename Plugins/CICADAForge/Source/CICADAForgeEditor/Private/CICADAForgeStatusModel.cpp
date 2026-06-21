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
            TEXT("LOG: Phase 003J CAD builder and PowerShell switch fix are live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "CadBuilderCardTitle", "CAD Builder"),
        NSLOCTEXT("CICADAForgeStatusModel", "CadBuilderCardBody", "Phase 003J adds mechanical part builders for mounting plates, robot plates, and enclosure blanks. These create CAD intent JSON and feed the sidecar/report/dashboard.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SwitchFixCardTitle", "PowerShell Switch Fix"),
        NSLOCTEXT("CICADAForgeStatusModel", "SwitchFixCardBody", "The wrapper now forwards -OpenReport and -OpenDashboard as real switch parameters, not tragic little strings wearing switch costumes.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "NoFakeStepCardTitle", "No Fake STEP Rule"),
        NSLOCTEXT("CICADAForgeStatusModel", "NoFakeStepCardBody", "Exact STEP export still requires an exact CAD engine. If CadQuery is missing, the correct result is an honest blocked report.")
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
                ? TEXT("Machine commands are locked. CAD builder is local/export-only.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
