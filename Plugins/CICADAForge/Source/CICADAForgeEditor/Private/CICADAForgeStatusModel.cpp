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
            TEXT("LOG: Phase 003F STL preview and quality gate are live. Last run: %s"),
            *ProjectState.LastRunState
        )
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "Export proof receipt"));

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "StlProofCardTitle", "STL Proof Gate"),
        NSLOCTEXT("CICADAForgeStatusModel", "StlProofCardBody", "Phase 003F adds an STL analyzer, mesh quality gate, JSON stats, and HTML preview report. The goal is inspectable output before slicer automation.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "PreviewReportCardTitle", "Preview Report"),
        NSLOCTEXT("CICADAForgeStatusModel", "PreviewReportCardBody", "Reports include triangle count, vertex count, bounding box, dimensions, surface area, volume estimate, edge manifold check, and a simple SVG preview.")
    });

    Model.WorkspaceCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "PrinterSafetyCardTitle", "Printer Safety Boundary"),
        NSLOCTEXT("CICADAForgeStatusModel", "PrinterSafetyCardBody", "Allowed: STL analysis, preview reports, manual slicer handoff. Blocked: serial ports, G-code streaming, direct printer send.")
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
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Safety Boundary"),
        FText::FromString(
            ProjectState.bMachineCommandsLocked
                ? TEXT("Machine commands are locked. STL proof/reporting is allowed; printer automation is not.")
                : TEXT("WARNING: machine command lock is disabled.")
        )
    });

    return Model;
}

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002DDefault()
{
    return MakeFromProjectState(FCICADAForgeProjectState::LoadFromConfig());
}
