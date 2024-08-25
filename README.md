### Team Tracker

**Team Tracker** offers an easy and efficient way to monitor XP, kill count, or progress in any skill, boss, or activity over time. The process is straightforward:

1. Create a Tracker: Set up a task with an objective and assigned team members.

Create a text file containing the names of your team members on a separate line. See `players.txt` for an example. This is a mandatory file when creating your tracker, using the `--players_file` flag.

Command: `python team_tracker.py <name of tracker> create --players_file <name of file with list of players> [--skill | --boss | --activity] <objective>`

Example: `python team_tracker.py myteam create --players_file ./players.txt --skill agility`

Example: `python team_tracker.py myteam create --players_file ./players.txt --activity "Clue Scrolls (hard)"`

2. Update the Tracker: Fetch data from the Hiscore database.

Command: `python team_tracker.py <name of tracker> update`

Example: `python team_tracker.py myteam update`

_NOTE_: Since data is being pulled from Hiscore DB, there is a chance that if a player has not retrieved the minimum high score xp/kc for an objective, the tracker would show that player's xp/kc as 0. Be sure to reach out to that team member if they have grinded xp/kc. 

3. View Progress: Generate a clear table showing each team member's current XP/KC and the change(delta) over time.

Command: `python team_tracker.py <name of tracker> print`

Example: `python team_tracker.py myteam print`

4. Remove the Tracker: Delete the tracker once it's no longer needed.

Command: `python team_tracker.py <name of tracker> destroy`

Example: `python team_tracker.py myteam destroy`

### Tasks and Objectives

--skill : attack,defence,strength,hitpoints,ranged,prayer,magic,cooking,woodcutting,fletching,fishing,firemaking,crafting,smithing,mining,herblore,agility,thieving,slayer,farming,runecrafting,hunter,construction

--boss : Abyssal Sire,Alchemical Hydra,Artio,Barrows Chests,Bryophyta,Callisto,Cal'varion,Cerberus,Chambers of Xeric,Chambers of Xeric: Challenge Mode,Chaos Elemental,Chaos Fanatic,Commander Zilyana,Corporeal Beast,Crazy Archaeologist,Dagannoth Prime,Dagannoth Rex,Dagannoth Supreme,Deranged Archaeologist,Duke Sucellus,General Graardor,Giant Mole,Grotesque Guardians,Hespori,Kalphite Queen,King Black Dragon,Kraken,Kree'Arra,K'ril Tsutsaroth,Lunar Chests,Mimic,Nex,Nightmare,Phosani's Nightmare,Obor,Phantom Muspah,Sarachnis,Scorpia,Scurrius,Skotizo,Sol Heredit,Spindel,Tempoross,The Gauntlet,The Corrupted Gauntlet,The Leviathan,The Whisperer,Theatre of Blood,Theatre of Blood: Hard Mode,Thermonuclear Smoke Devil,Tombs of Amascut,Tombs of Amascut: Expert Mode,TzKal-Zuk,TzTok-Jad,Vardorvis,Venenatis,Vet'ion,Vorkath,Wintertodt,Zalcano,Zulrah

--activity : League Points,Deadman Points,Bounty Hunter - Hunter,Bounty Hunter - Rogue,Bounty Hunter (Legacy) - Hunter,Bounty Hunter (Legacy) - Rogue,Clue Scrolls (all),Clue Scrolls (beginner),Clue Scrolls (easy),Clue Scrolls (medium),Clue Scrolls (hard),Clue Scrolls (elite),Clue Scrolls (master),LMS - Rank,PvP Arena - Rank,Soul Wars Zeal,Rifts closed,Colosseum Glory

