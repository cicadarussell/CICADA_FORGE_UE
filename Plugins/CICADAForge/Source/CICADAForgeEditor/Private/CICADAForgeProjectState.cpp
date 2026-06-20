#include "CICADAForgeProjectState.h"

#include "Misc/ConfigCacheIni.h"
#include "Misc/Paths.h"

FCICADAForgeProjectState FCICADAForgeProjectState::MakeDefault()
{
    FCICADAForgeProjectState State;

    State.ProjectName = TEXT("CICADA_FORGE_UE");
    State.RepoPath = TEXT("C:\\CICADA\\CICADA_APPS\\CICADA_FORGE_UE");
    State.CurrentPhase = TEXT("Phase 002D: persistent project state feeds the shell");
    State.EvidenceState = TEXT("Manual evidence logging active");
    State.CadSidecarState = TEXT("Offline - Phase 005 target");
    State.MachineBridgeState = TEXT("Locked - no physical machine commands in V0 shell");
    State.LastRunState = TEXT("Phase 002C passed by user screenshot");
    State.bMachineCommandsLocked = true;

    return State;
}

FCICADAForgeProjectState FCICADAForgeProjectState::LoadFromConfig()
{
    FCICADAForgeProjectState State = MakeDefault();

    const FString ConfigPath = FPaths::ProjectConfigDir() / TEXT("CICADAForgeState.ini");
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
