#pragma once

#include "CoreMinimal.h"

struct FCICADAForgeProjectState
{
    FString ProjectName;
    FString RepoPath;
    FString CurrentPhase;
    FString EvidenceState;
    FString CadSidecarState;
    FString MachineBridgeState;
    FString LastRunState;
    bool bMachineCommandsLocked = true;

    static FCICADAForgeProjectState MakeDefault();
    static FCICADAForgeProjectState LoadFromConfig();
};
