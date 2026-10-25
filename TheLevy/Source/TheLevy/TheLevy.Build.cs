// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class TheLevy : ModuleRules
{
	public TheLevy(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"TheLevy",
			"TheLevy/Variant_Platforming",
			"TheLevy/Variant_Platforming/Animation",
			"TheLevy/Variant_Combat",
			"TheLevy/Variant_Combat/AI",
			"TheLevy/Variant_Combat/Animation",
			"TheLevy/Variant_Combat/Gameplay",
			"TheLevy/Variant_Combat/Interfaces",
			"TheLevy/Variant_Combat/UI",
			"TheLevy/Variant_SideScrolling",
			"TheLevy/Variant_SideScrolling/AI",
			"TheLevy/Variant_SideScrolling/Gameplay",
			"TheLevy/Variant_SideScrolling/Interfaces",
			"TheLevy/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
