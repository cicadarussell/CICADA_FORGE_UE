#pragma once

#include "Modules/ModuleManager.h"

class FCICADAForgeModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
};
