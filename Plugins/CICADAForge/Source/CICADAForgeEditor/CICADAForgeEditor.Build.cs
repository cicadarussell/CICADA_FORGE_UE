using UnrealBuildTool;

public class CICADAForgeEditor : ModuleRules
{
    public CICADAForgeEditor(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(
            new string[]
            {
                "Core",
                "CoreUObject",
                "Engine",
                "CICADAForge"
            }
        );

        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
                "Slate",
                "SlateCore",
                "ToolMenus",
                "UnrealEd",
                "LevelEditor",
                "Projects"
            }
        );
    }
}
