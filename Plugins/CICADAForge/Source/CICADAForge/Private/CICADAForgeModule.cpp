#include "CICADAForgeModule.h"

#include "Logging/LogMacros.h"

DEFINE_LOG_CATEGORY_STATIC(LogCICADAForge, Log, All);

#define LOCTEXT_NAMESPACE "FCICADAForgeModule"

void FCICADAForgeModule::StartupModule()
{
    UE_LOG(LogCICADAForge, Display, TEXT("CICADA Forge module started."));
}

void FCICADAForgeModule::ShutdownModule()
{
    UE_LOG(LogCICADAForge, Display, TEXT("CICADA Forge module shut down."));
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FCICADAForgeModule, CICADAForge)
