#include "CICADAForgeStatusModel.h"

FCICADAForgeStatusModel FCICADAForgeStatusModel::MakePhase002CDefault()
{
    FCICADAForgeStatusModel Model;

    Model.ProjectName = TEXT("CICADA_FORGE_UE");

    Model.PhaseLabel = NSLOCTEXT(
        "CICADAForgeStatusModel",
        "Phase002CLabel",
        "Phase 002C: status model feeds the shell"
    );

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

    Model.BottomLog = NSLOCTEXT(
        "CICADAForgeStatusModel",
        "BottomLog",
        "LOG: Phase 002C status model loaded. Next target: persistent project state."
    );

    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionNewDesign", "[stub] New design"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionOpenGraph", "[stub] Open feature graph"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionRunValidation", "[stub] Run validation"));
    Model.ProjectActions.Add(NSLOCTEXT("CICADAForgeStatusModel", "ActionExportProof", "[stub] Export proof receipt"));

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
        NSLOCTEXT("CICADAForgeStatusModel", "GateCardBody", "Gate: prove the UI shell reads from one status model. No CAD export, no machine control, no sidecar calls in this phase.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "EvidenceCardTitle", "Evidence"),
        NSLOCTEXT("CICADAForgeStatusModel", "EvidenceCardBody", "Manual evidence logging active. Automated screenshots and receipts are later.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SidecarCardTitle", "CAD Sidecar"),
        NSLOCTEXT("CICADAForgeStatusModel", "SidecarCardBody", "Offline. Phase 005 target. No requests sent.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "MachineCardTitle", "Machine Bridge"),
        NSLOCTEXT("CICADAForgeStatusModel", "MachineCardBody", "Locked. No physical machine commands exist in V0 shell.")
    });

    Model.StatusCards.Add(FCICADAForgePanelCard{
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardTitle", "Safety Boundary"),
        NSLOCTEXT("CICADAForgeStatusModel", "SafetyCardBody", "All machine actions require future dry run, preview, explicit approval, and logs.")
    });

    return Model;
}
