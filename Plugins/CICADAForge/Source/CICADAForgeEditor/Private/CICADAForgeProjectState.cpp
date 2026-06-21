#include "CICADAForgeProjectState.h"

#include "Misc/ConfigCacheIni.h"
#include "Misc/Paths.h"

FCICADAForgeProjectState FCICADAForgeProjectState::MakeDefault()
{
    FCICADAForgeProjectState State;

    State.ProjectName = TEXT("CICADA_FORGE_UE");
    State.RepoPath = TEXT("C:\\CICADA\\CICADA_APPS\\CICADA_FORGE_UE");
    State.CurrentPhase = TEXT("Phase 003I: CAD sidecar contract and exact-geometry boundary are alive");
    State.EvidenceState = TEXT("Headless STL/job/report/dashboard path is working; Phase 003I adds CAD sidecar contract, part schema, example mechanical parts, and STEP-readiness diagnostics");
    State.CadSidecarState = TEXT("CAD sidecar V0 contract built; CadQuery/FreeCAD engine optional and detected by doctor; no fake STEP if engine missing");
    State.MachineBridgeState = TEXT("Locked - exact-geometry sidecar is local/export-only; no printer/CNC/pick-place command path");
    State.LastRunState = TEXT("Project is on track: headless outputs, dashboard, and CAD truth boundary now exist");
    State.bMachineCommandsLocked = true;

    return State;
}

FCICADAForgeProjectState FCICADAForgeProjectState::LoadFromConfig()
{
    FCICADAForgeProjectState State = MakeDefault();

    const FString RawConfigPath = FPaths::ProjectConfigDir() / TEXT("CICADAForgeState.ini");
    const FString ConfigPath = FConfigCacheIni::NormalizeConfigIniPath(RawConfigPath);
    const TCHAR* Section = TEXT("CICADAForge.State");

    GConfig->GetString(Section, TEXT("ProjectName"), State.ProjectName, ConfigPath);
    GConfig->GetString(Section, TEXT("RepoPath"), State.RepoPath, ConfigPath);
    GConfig->GetString(Section, TEXT("CurrentPhase"), State.CurrentPhase, ConfigPath);
    GConfig->GetString(Section, TEXT("EvidenceState"), State.EvidenceState, ConfigPath);
    GConfig->GetString(Section, TEXT("CadSidecarState"), State.CadSidecarState, ConfigPath);
    GConfig->GetString(Section, TEXT("MachineBridgeState"), State.MachineBridgeState, ConfigPath);
    GConfig->GetString(Section, TEXT("LastRunState"), State.LastRunState, ConfigPath);
    GConfig->GetBool(Section, TEXT("bMachineCommandsLocked"), State.bMachineCommandsLocked, ConfigPath);

    return State;
}
