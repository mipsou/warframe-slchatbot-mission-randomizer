
First version of mission list parsing complete.
	Still have some fields to add to Mission class
Then onto the randomizer

First Pass
-Fetch data every X minutes ( defaults to 5 )
-Toggle Special missions
-Toggle mission Zones
-Toggle mission Types
-Settings changer commands
-Hot reloading and recreate random list

Future thoughts:
-Alert when any type of mission is about to rotate
-Progress mode (track the casters progress)
-Event support
-Warframe info cmds
-Weapon info cmds
-News link cmds

API blocked:
-Nightmare missions
	Add to settings class and settingsOptions
	"togNightmare": {
        "type": "checkbox",
        "value": true,
        "label": "Toggle nightmare missions.",
        "tooltip": "Toggles all nightmaremissions.",
        "group": "Randomizer:Special Settings"
    },
	"nightmareWeight": {
        "type": "numberbox",
        "value": 1,
        "label": "Nightmare Mission Weighting",
        "tooltip": "",
        "group": "Randomizer:Special Settings"
    },
	
-Kuva farm missions
	Add to settings class and settingsOptions
	"togKuvafarm": {
        "type": "checkbox",
        "value": true,
        "label": "Toggle kuva farm missions.",
        "tooltip": "Toggles all kuva siphons and flood missions.",
        "group": "Randomizer:Special Settings"
    },
	"kuvafarmWeight": {
        "type": "numberbox",
        "value": 1,
        "label": "Kuva farm Mission Weighting",
        "tooltip": "",
        "group": "Randomizer:Special Settings"
    },

-Syndicate missions
	Add to settings class and settingsOptions
	"togSyndicate": {
        "type": "checkbox",
        "value": true,
        "label": "Toggle syndicate missions.",
        "tooltip": "Toggles all syndicate missions.",
        "group": "Randomizer:Special Settings"
    },
	"syndicateWeight": {
        "type": "numberbox",
        "value": 1,
        "label": "Syndicate Mission Weighting",
        "tooltip": "",
        "group": "Randomizer:Special Settings"
    },