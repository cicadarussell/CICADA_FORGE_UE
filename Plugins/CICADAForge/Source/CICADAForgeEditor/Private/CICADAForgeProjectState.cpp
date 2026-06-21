#include "CICADAForgeProjectState.h"

#include "Misc/ConfigCacheIni.h"
#include "Misc/Paths.h"

FCICADAForgeProjectState FCICADAForgeProjectState::MakeDefault()
{
    FCICADAForgeProjectState State;

    State.ProjectName = TEXT("CICADA_FORGE_UE");
    State.RepoPath = TEXT("C:\\CICADA\\CICADA_APPS\\CICADA_FORGE_UE");
    State.CurrentPhase = TEXT("Phase 003F: STL preview and quality gate are alive");
    State.EvidenceState = TEXT("Phase 002L is current on GitHub; Phase 003F is cumulative and adds mesh proof/reporting before any slicer or printer automation");
    State.CadSidecarState = TEXT("STL mesh exporter V0 plus STL analyzer/report pipeline; exact CAD/STEP sidecar still not built");
    State.MachineBridgeState = TEXT("Locked - local STL/manifest/report generation and manual slicer workflow only");
    State.LastRunState = TEXT("Project remains on track: editable box jobs -> STL -> mesh report -> manifest -> slicer/manual print");
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
