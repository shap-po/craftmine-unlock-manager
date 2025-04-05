import os
import requests
import json
import re
import inquirer
import sys

# Path to a minecraft language file
LANG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "en_us.json"
)

# Default unlocks
UNLOCKS = [
    "minecraft:exploration",
    "minecraft:ender_pearl_starter",
    "minecraft:more_pearls",
    "minecraft:more_more_pearls",
    "minecraft:speed_1",
    "minecraft:amphibian",
    "minecraft:speed_2",
    "minecraft:speed_3",
    "minecraft:shazboots",
    "minecraft:pathfinder",
    "minecraft:lodestone_exits",
    "minecraft:starter_compass",
    "minecraft:sneak_1",
    "minecraft:sneak_2",
    "minecraft:movement_boost",
    "minecraft:crafting",
    "minecraft:smelter_1",
    "minecraft:smelter_2",
    "minecraft:smelt_value_1",
    "minecraft:smelt_value_2",
    "minecraft:inventory_slots_1",
    "minecraft:inventory_slots_2",
    "minecraft:inventory_slots_3",
    "minecraft:bundle_of_fortune",
    "minecraft:inventory_crafting",
    "minecraft:inventory_crafting_3x3",
    "minecraft:crafting_efficiency",
    "minecraft:starter_crafting",
    "minecraft:enchanting",
    "minecraft:magic_starter_kit",
    "minecraft:magic_master_kit",
    "minecraft:runemaster",
    "minecraft:fire_wand",
    "minecraft:wind_wand",
    "minecraft:teleportation_wand",
    "minecraft:efficient_enchanting",
    "minecraft:alchemy",
    "minecraft:mise_en_place",
    "minecraft:allez_cuisine",
    "minecraft:mass_production",
    "minecraft:gatherer",
    "minecraft:pickup_area_size",
    "minecraft:dirt_enjoyer_1",
    "minecraft:apprentice_shoveler",
    "minecraft:journeyman_shoveler",
    "minecraft:expert_shoveler",
    "minecraft:master_shoveler",
    "minecraft:dirt_enjoyer_2",
    "minecraft:dirt_enjoyer_3",
    "minecraft:dirt_destroyer_1",
    "minecraft:dirt_destroyer_2",
    "minecraft:dirt_connoisseur",
    "minecraft:hunter",
    "minecraft:campfire",
    "minecraft:you_are_the_campfire",
    "minecraft:mining",
    "minecraft:sub_mining_efficiency",
    "minecraft:fishing",
    "minecraft:fishing_rod",
    "minecraft:trident",
    "minecraft:poseidon",
    "minecraft:mining_efficiency",
    "minecraft:mining_efficiency_2",
    "minecraft:mining_efficiency_3",
    "minecraft:starter_pick",
    "minecraft:silky_pick",
    "minecraft:ore_seeker_1",
    "minecraft:ore_seeker_2",
    "minecraft:lucky_pick",
    "minecraft:rare_earth_specialist",
    "minecraft:combatant",
    "minecraft:sorcerer_supreme",
    "minecraft:wing_guardian_lift_off_to_the_sky",
    "minecraft:dragon_fire",
    "minecraft:archer",
    "minecraft:quiver",
    "minecraft:fletcher",
    "minecraft:arrowverse",
    "minecraft:tracker",
    "minecraft:armaments",
    "minecraft:decked_out",
    "minecraft:full_metal",
    "minecraft:starter_shield",
    "minecraft:shield_bash",
    "minecraft:fire_shield",
    "minecraft:crusher",
    "minecraft:starter_apples",
    "minecraft:more_starter_apples",
    "minecraft:golden_starter_apples",
    "minecraft:starter_sword",
    "minecraft:starter_sword_iron",
    "minecraft:better_starter_sword",
    "minecraft:best_starter_sword",
    "minecraft:chopper",
    "minecraft:viking",
    "minecraft:berserker",
    "minecraft:varangian",
    "minecraft:pets",
    "minecraft:pet_chicken",
    "minecraft:pet_the_animal",
    "minecraft:pet_armadillo",
    "minecraft:pet_frog",
    "minecraft:pet_cow",
    "minecraft:pet_mooshroom",
    "minecraft:pet_axolotl",
    "minecraft:pet_turtle",
    "minecraft:pet_cat",
    "minecraft:pet_bee",
    "minecraft:pet_fox",
    "minecraft:pet_polar_bear",
    "minecraft:pet_slime",
    "minecraft:pet_creeper",
    "minecraft:pet_wolf",
    "minecraft:pet_wolf_big",
    "minecraft:pet_wolf_armored",
    "minecraft:pet_wolf_sword",
    "minecraft:school_of_hard_knocks",
    "minecraft:school_of_actual_hard_knocks",
    "minecraft:rewrite_in_rust",
    "minecraft:extra_firepower",
    "minecraft:proper_walking_pace",
    "minecraft:thorns_plus_plus",
    "minecraft:learning_1",
    "minecraft:learning_2",
    "minecraft:learning_3",
    "minecraft:learning_4",
    "minecraft:learning_5",
    "minecraft:learning_6",
    "minecraft:learning_7",
    "minecraft:learning_8",
    "minecraft:learning_9",
    "minecraft:learning_10",
    "minecraft:learning_11",
    "minecraft:learning_12",
    "minecraft:learning_13",
    "minecraft:learning_14",
    "minecraft:learning_15",
    "minecraft:learning_16",
    "minecraft:learning_17",
    "minecraft:learning_18",
    "minecraft:learning_19",
    "minecraft:learning_20",
    "minecraft:jump_king",
    "minecraft:mega_jump",
    "minecraft:safe_falling",
    "minecraft:jump_king_2",
    "minecraft:jump_king_3",
    "minecraft:jump_king_4",
    "minecraft:jump_king_5",
    "minecraft:jump_king_6",
    "minecraft:jump_king_7",
    "minecraft:jump_king_8",
    "minecraft:jump_king_9",
    "minecraft:jump_king_10",
    "minecraft:elytra",
    "minecraft:rockets",
]

lang: dict[str, str] | None = json.load(open(LANG_PATH, "r", encoding="utf-8")) \
    if os.path.exists(LANG_PATH) else None


def get_uuid(player_name: str) -> str:
    """Get UUID from a player name."""
    id = requests.get(
        f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()["id"]
    return f"{id[:8]}-{id[8:12]}-{id[12:16]}-{id[16:20]}-{id[20:]}"


def is_uuid(name_or_uuid: str) -> bool:
    """Check if a string matches the UUID format (e.g. XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)."""
    return re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", name_or_uuid) is not None


def get_unlocks(unlocks_folder: str, uuid: str) -> dict | None:
    """Get unlocks for a player."""
    unlocks_file = os.path.join(unlocks_folder, f"{uuid}.json")

    if not os.path.exists(unlocks_file):
        print(f"Unlocks file for {uuid} does not exist.")
        return {}

    with open(unlocks_file, "r", encoding="utf-8") as f:
        unlocks = json.load(f)

    return unlocks


def set_unlock(unlocks_folder: str, uuid: str, unlock: str, value: bool) -> bool:
    """Set a single unlock for a player."""
    unlocks_file = os.path.join(unlocks_folder, f"{uuid}.json")

    if not os.path.exists(unlocks_file):
        print(f"Unlocks file for {uuid} does not exist.")
        return False

    with open(unlocks_file, "r", encoding="utf-8") as f:
        unlocks = json.load(f)

    if unlock not in unlocks["obtained"]:
        print(f"Unlock {unlock} not found in {uuid}'s unlocks.")
        return False

    unlocks["obtained"][unlock] = value

    with open(unlocks_file, "w", encoding="utf-8") as f:
        json.dump(unlocks, f, indent=4)

    print(f"Successfully set unlock {unlock} to {value} for {uuid}.")
    return True


def set_unlocks(unlocks_folder: str, uuid: str, unlocks: dict[str, bool]) -> bool:
    """Set unlocks for a player."""
    unlocks_file = os.path.join(unlocks_folder, f"{uuid}.json")

    if not os.path.exists(unlocks_file):
        print(f"Unlocks file for {uuid} does not exist.")
        return False

    with open(unlocks_file, "r", encoding="utf-8") as f:
        unlocks_data = json.load(f)

    unlocks_data["obtained"] = unlocks

    with open(unlocks_file, "w", encoding="utf-8") as f:
        json.dump(unlocks_data, f, indent=4)

    print(f"Successfully set unlocks for {uuid}.")
    return True


def get_unlock_translation(unlock: str) -> str:
    """Get text translation for an unlock."""
    if lang is None:
        return ""

    unlock = unlock.removeprefix("minecraft:")  # trim minecraft namespace
    print(unlock)

    name = lang.get(f"unlocks.unlock.{unlock}.name", unlock)
    description = lang.get(f"unlocks.unlock.{unlock}.description", unlock)

    return f"{name} - {description}"


def prompt_and_set_player_unlocks(save_folder: str | None = None, name_or_uuid: str | None = None, new_unlocks: dict[str, bool] | None = None) -> None:
    if save_folder is None:
        save_folder = inquirer.prompt([
            inquirer.Path(
                "save_folder",
                message="Select save folder"
            )
        ])
        if not save_folder:  # if Ctrl+C
            return
        save_folder = save_folder["save_folder"]

    unlocks_folder = os.path.join(save_folder, "unlocks")

    if not os.path.exists(unlocks_folder):
        print(f"Unlocks folder does not exist for save in {save_folder}.")
        return

    if name_or_uuid is None:
        name_or_uuid = inquirer.prompt([
            inquirer.Text(
                "name_or_id",
                message="Enter UUID or player name"
            )
        ])
        if not name_or_uuid:  # if Ctrl+C
            return
        name_or_uuid = name_or_uuid["name_or_id"]

    uuid = name_or_uuid if is_uuid(name_or_uuid) else get_uuid(name_or_uuid)
    unlocks = get_unlocks(unlocks_folder, uuid).get("obtained", {})
    if not unlocks:
        print(f"No unlocks found for player with UUID {uuid}.")
        return

    if new_unlocks is None:
        set_true = inquirer.prompt([
            inquirer.Checkbox(
                "unlocks",
                message="Select unlocks",
                choices=UNLOCKS,
                hints={
                    unlock: get_unlock_translation(unlock)
                    for unlock in UNLOCKS
                } if lang is not None else None,
                default=[
                    unlock
                    for unlock in UNLOCKS
                    if unlocks.get(unlock, False)
                ]
            )
        ])
        if not set_true:  # if Ctrl+C
            return
        set_true = set_true["unlocks"]

        new_unlocks = {
            unlock: unlock in set_true
            for unlock in UNLOCKS
        }

    set_unlocks(unlocks_folder, uuid, new_unlocks)


def main():
    save_folder: str | None = None
    name_or_uuid: str | None = None
    new_unlocks: dict[str, bool] | None = None

    if len(sys.argv) > 1:
        save_folder = sys.argv[1]
    if len(sys.argv) > 2:
        name_or_uuid = sys.argv[2]
    if len(sys.argv) > 3:
        unlocks = sys.argv[3:]
        new_unlocks = {
            unlock: unlock in unlocks or unlock.removeprefix(
                "minecraft:") in unlocks
            for unlock in UNLOCKS
        }

    prompt_and_set_player_unlocks(save_folder, name_or_uuid, new_unlocks)


if __name__ == "__main__":
    main()
