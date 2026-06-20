#pragma once

#include "Modules/ModuleManager.h"
#include "Templates/SharedPointer.h"

class SDockTab;
class FSpawnTabArgs;

class FCICADAForgeEditorModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

private:
    void RegisterMenus();
    TSharedRef<SDockTab> SpawnForgeTab(const FSpawnTabArgs& Args);

private:
    static const FName ForgeTabName;
};
