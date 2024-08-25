
import os
import json
import pathlib
from argparse import ArgumentParser, FileType
from util import SKILLS, BOSSES, ACTIVITIES, Hiscore

SKILL = "skill"
ACTIVITY = "activity"
BOSS = "boss"
TRACKER_FILE_PATH = lambda x: str(pathlib.Path(__file__).parent.absolute()) + "/trackers/%s.tracker" % (x)

def tracker_create_file(tracker_name, opt, value, players_hs):
    """
        boss: (name, kc, rank)
        skill: (name, level, xp, rank)
        activity: (name, score, rank)
        {
            name: "tracker_name",
            option: "Boss",
            value: "Zulrah",
            total_delta: 0,
            players: {
                // Boss example - kc
                player1: {
                    start: 1000,
                    current: 1000,
                    delta: 0
                }
                // Skill example - xp
                player1: {
                    start: 1000,
                    current: 1000,
                    delta: 0
                }
                // Activity example - kc/score
                {
                    start: 1000,
                    current: 1000,
                    delta: 0
                }
            }
        }
    """
    trkr_mdata = {
        "name": tracker_name,
        "option": opt,
        "value": value,
        "total_delta": 0,
        "players": {}
    }
    
    for player in players_hs:
        opt_data  = player.bosses.get(value).score if opt == BOSS \
                        else player.skills.get(value).xp if opt == SKILL \
                        else player.activities.get(value).score 
        trkr_mdata["players"][player.username] = {
            "start": opt_data if opt_data > 0 else 0,
            "current": opt_data if opt_data > 0 else 0,
            "delta": 0
        }
    
    with open(TRACKER_FILE_PATH(tracker_name), "w") as trkr_fp:
        trkr_fp.write(json.dumps(trkr_mdata, indent=4))


def tracker_file_exists(trkr_file):
    return os.path.isfile(trkr_file) and os.path.exists(trkr_file)


def can_create_tracker_file(tracker_name, overwrite):
    trkr_file = TRACKER_FILE_PATH(tracker_name)
    if tracker_file_exists(trkr_file):
        return overwrite
    return True


def tracker_create(tracker_name, players_fp, option, value, overwrite=False):
    if not can_create_tracker_file(tracker_name, overwrite):
        print(f"Unable to create tracker file: {tracker_name} already exists. Use flag '-o' to overwrite file")
        return
    
    players = sorted(players_fp.read().splitlines())
    players_hs = [Hiscore(player) for player in players]
    tracker_create_file(tracker_name, option, value, players_hs)


def tracker_update(tracker_name):
    trkr_file = TRACKER_FILE_PATH(tracker_name)
    if not tracker_file_exists(trkr_file):
        print(f"Tracker {tracker_name} does not exist")
        return
    
    with open(trkr_file, "r") as trkr_fp:
        trkr_mdata = json.loads(trkr_fp.read())
        
    option = trkr_mdata["option"]
    value = trkr_mdata["value"]
    trkr_mdata["total_delta"] = 0
    
    for player,player_mdata in trkr_mdata["players"].items():
        print("Updating", player)
        player_hs = Hiscore(player)
        start = player_mdata["start"]

        player_delta = 0
        new_current = 0
        if option == BOSS:
            new_current = player_hs.bosses.get(value).score
            player_delta = new_current - start
        elif option == SKILL:
            new_current = player_hs.skills.get(value).xp
            player_delta = new_current - start 
        elif option == ACTIVITY:
            new_current = player_hs.activities.get(value).score
            player_delta = new_current - start
        
        if player_delta < 0:
            player_delta = 0
        
        if new_current < 0:
            new_current = 0
        
        player_mdata["current"] = new_current
        player_mdata["delta"] = player_delta
        trkr_mdata["total_delta"] += player_delta

    with open(trkr_file, "w") as fp:
        fp.write(json.dumps(trkr_mdata, indent=4))


def tracker_destroy(tracker_name):
    trkr_file = TRACKER_FILE_PATH(tracker_name)
    if not tracker_file_exists(trkr_file):
        print(f"Tracker {tracker_name} does not exist")
    os.remove(trkr_file)

def tracker_print(tracker_name):
    trkr_file = TRACKER_FILE_PATH(tracker_name)
    if not os.path.exists(trkr_file) and not os.path.isfile(trkr_file):
        print(f"Tracker {tracker_name} does not exist")

    trkr_mdata = None
    with open(trkr_file, "r") as trkr_fp:
        trkr_mdata = json.loads(trkr_fp.read())

    print(f"Task:       {trkr_mdata['option']}")
    print(f"Objective:  {trkr_mdata['value']}")
    print()
    print("PLAYER           START      CURRENT    DELTA\n"
          "------------------------------------------------")

    for player,player_mdata in trkr_mdata["players"].items():
        start = player_mdata["start"]
        current = player_mdata["current"]
        delta = player_mdata["delta"]

        print(f"{player}"+" "*(17-len(player))+f"{start}"+" "*(11-len(str(start))), end="")
        print(f"{current}"+" "*(11-len(str(current)))+f"{delta}"+" "*(11-len(str(delta))))
    
    print(f"\nTotal Delta: {trkr_mdata['total_delta']}")

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="team_tracker.py",
        description="Team Tracker - KCs and XPs",
        allow_abbrev=False
    )

    parser.add_argument("tracker_name", type=str, help="Name of tracker")
    parser.add_argument("command", choices=["create", "update", "destroy", "print"])
    parser.add_argument("--players_file", type=FileType('r'), help="List of players to create new tracker")
    parser.add_argument("-o", "--overwrite", default=False, action="store_true", help="Overwrite a tracker file that already exists")
    
    group_create = parser.add_mutually_exclusive_group(required=False)
    group_create.add_argument('--boss', choices=BOSSES, help="Create a boss tracker")
    group_create.add_argument('--activity', choices=ACTIVITIES, help="Create an activity tracker")
    group_create.add_argument('--skill', choices=SKILLS, help="Create a skill tracker")

    args = parser.parse_args()
    
    tracker_name = args.tracker_name
    command = args.command

    if command == "create":
        if not args.players_file:
            parser.error("Missing argument: --players_file")
        elif not args.boss and not args.activity and not args.skill:
            parser._handle_conflict_error("One of required arguments is missing: --boss BOSS, --skill SKILL, --activity ACTIVITY")
        else:
            tracker_create_fn = None
            value = None
            if args.boss:
                value = args.boss
                option = BOSS
            elif args.skill:
                value = args.skill
                option = SKILL
            elif args.activity:
                value = args.activity
                option = ACTIVITY
            tracker_create(tracker_name, args.players_file, option, value, args.overwrite)
    elif command == "update":
        tracker_update(tracker_name)
    elif command == "destroy":
        tracker_destroy(tracker_name)
    elif command == "print":
        tracker_print(tracker_name)
    else:
        parser.print_help()
