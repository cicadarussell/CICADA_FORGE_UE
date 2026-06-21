#include "CICADAForgeProjectState.h"

#include "Misc/ConfigCacheIni.h"
#include "Misc/Paths.h"

FCICADAForgeProjectState FCICADAForgeProjectState::MakeDefault()
{
    FCICADAForgeProjectState State;

    State.ProjectName = TEXT("CICADA_FORGE_UE");
    State.RepoPath = TEXT("C:\\CICADA\\CICADA_APPS\\CICADA_FORGE_UE");
    State.CurrentPhase = TEXT("Phase 003J: CAD builder and PowerShell switch fix are alive");
    State.EvidenceState = TEXT("003I audit, cad-doctor, cad-validate, dashboard passed; Phase 003J fixes PowerShell switch forwarding and adds CAD part builders/full-check");
    State.CadSidecarState = TEXT("CAD sidecar V0 contract plus mechanical part builder; CadQuery/FreeCAD still optional and detected by doctor; no fake STEP if engine missing");
    State.MachineBridgeState = TEXT("Locked - CAD builder writes intent/reports/optional exports only; no printer/CNC/pick-place command path");
    State.LastRunState = TEXT("Project is on track: PowerShell wrapper bug fixed and CAD builder path added");
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
