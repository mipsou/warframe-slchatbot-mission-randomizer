
	Warframe Random Mission script
		by Rickie26k

requested by the awesome esp4him found at https://www.twitch.tv/esp4him

To install the script: 
	Start Streamlabs Chatbot
	Make sure you're connected
	Hit your scripts tab (requires connection)
	Right-click and open scripts folder
	Extract the WRM folder into your scripts folder

Don't forget to hit Save Settings when you have changed
	a setting. This button press is what updates the random
	selection list.

Weights are a way to increase the occurence of the
	weighted mission type. The baseline mission count,
	including assassinations and archwing are 205, and
	with special missions between 230-240.

	Example: We got 235 total missions with everything
	enabled. If we increase relic weight to 20, the
	(in this example) 5 fissure missions will be added
	20 times each to the random roll list.
	This brings up the chance for a fissure mission
	from 2% chance to 30%.


If the script has a hiccup and settings seems to
	misbehave or not take, delete the generated files
	WRMConfig.js & WRMConfig.json and reload your
	scripts.

Any other problems arise, feel free to post an issue on
	github.

Credits:
	Thanks to Zerro0713, maker of Ankhbot/SLCB RPG
		for nicely readable code I could learn
		from. And use some things to get started.
	http://www.twitch.tv/Zerro0713

	Thanks to the people who worked and works on
		warframe-worldstate-parser and 
		warframe-worldstate-data. Helped me make
		a lot more sense of how to parse
		worldState.php in a sensical manner.
	https://github.com/WFCD/warframe-worldstate-parser
	https://github.com/WFCD/warframe-worldstate-data
	

Changelog:

	Update 0.9.1.0:
	Updated json loading so the files are only read once
	instead of once or even twice for each mission in
	certain cases.
	Gave this readme a little touch up.

	Initial release 0.9.0.1:
	See "First Pass" in feature list


Features:

First Pass
-Toggle Special missions X
-Toggle mission Zones X
-Toggle mission Types X
-Hot reloading and recreate random list
	On save settings X
	On command request -
-Fetch data every X minutes ( defaults to 200 seconds ) X

Future thoughts:
-Settings changer commands
-Alert when any type of mission is about to rotate
-Level capping?
-Progress mode (track the casters progress)
-Event support
-Warframe info cmds
-Weapon info cmds
-News link cmds