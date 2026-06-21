#include "CICADAForgeProjectState.h"

#include "Misc/ConfigCacheIni.h"
#include "Misc/Paths.h"

FCICADAForgeProjectState FCICADAForgeProjectState::MakeDefault()
{
    FCICADAForgeProjectState State;

    State.ProjectName = TEXT("CICADA_FORGE_UE");
    State.RepoPath = TEXT("C:\\CICADA\\CICADA_APPS\\CICADA_FORGE_UE");
    State.CurrentPhase = TEXT("Phase 002K: debug cockpit and receipt dry-run are alive");
    State.EvidenceState = TEXT("Phase 002J assumed locally working by user report; Phase 002K adds debug tooling and explicit receipt dry-run");
    State.CadSidecarState = TEXT("Offline - Phase 005 target");
    State.MachineBridgeState = TEXT("Locked - no physical machine commands in V0 shell");
    State.LastRunState = TEXT("Phase 002J UI changed and looked good; moving to larger focused debug cluster");
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
