#pragma once

#include "CoreMinimal.h"
#include "CICADAForgeProjectState.h"

struct FCICADAForgePanelCard
{
    FText Title;
    FText Body;
};

struct FCICADAForgeStatusModel
{
    FString ProjectName;
    FText PhaseLabel;
    FText LeftRailTitle;
    FText WorkspaceTitle;
    FText StatusTitle;
    FText BottomLog;

    TArray<FText> ProjectActions;
    TArray<FCICADAForgePanelCard> WorkspaceCards;
    TArray<FCICADAForgePanelCard> StatusCards;

    static FCICADAForgeStatusModel MakeFromProjectState(const FCICADAForgeProjectState& ProjectState);
    static FCICADAForgeStatusModel MakePhase002DDefault();
};
