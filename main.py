import os
import time
import random
import questionary

from termimon.termimon import TermiVironment, LifeStage


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def countdown(duration_seconds):
    for remaining in range(duration_seconds, 0, -1):
        hrs, rem = divmod(remaining, 3600)
        mins, secs = divmod(rem, 60)
        timer_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        print(f"\rStudying… Time left: {timer_str}", end="", flush=True)
        time.sleep(1)
    print("\rStudying… Time left: 00:00:00          ")


def show_party(env):
    clear_screen()
    print("-- Party --\n")
    if not env.current_party:
        print("Party is empty.")
    else:
        for idx, t in enumerate(env.current_party, start=1):
            print(f"{idx}. {t.nickname} ({
                  t.lifestage.value}, HP: {t.current_health})")
    questionary.text("\nPress Enter to continue…").skip_if(
        lambda _: True, default="").ask()


def show_storage(env):
    clear_screen()
    print("-- Storage --\n")
    if not env.storage:
        print("Storage is empty.")
    else:
        for idx, t in enumerate(env.storage, start=1):
            print(f"{idx}. {t.nickname} ({
                  t.lifestage.value}, HP: {t.current_health})")
    questionary.text("\nPress Enter to continue…").skip_if(
        lambda _: True, default="").ask()


def move_termimon(env):
    clear_screen()
    direction = questionary.select(
        "Move which direction?",
        choices=[
            "Storage → Party",
            "Party → Storage"
        ]).ask()
    if direction == "Storage → Party":
        if not env.storage:
            questionary.print("Storage is empty!", style="bold fg:red")
            questionary.text("").skip_if(lambda _: True, default="").ask()
            return
        if len(env.current_party) >= 6:
            questionary.print("Party is full!", style="bold fg:red")
            questionary.text("").skip_if(lambda _: True, default="").ask()
            return
        pick = questionary.select(
            "Which to move to party?",
            choices=[t.nickname for t in env.storage]
        ).ask()
        for t in env.storage:
            if t.nickname == pick:
                env.move_to_party(t)
                questionary.print(
                    f"Moved {pick} to the party.", style="fg:green")
                break
        questionary.text("").skip_if(lambda _: True, default="").ask()
    else:
        if not env.current_party:
            questionary.print("Party is empty!", style="bold fg:red")
            questionary.text("").skip_if(lambda _: True, default="").ask()
            return
        pick = questionary.select(
            "Which to move to storage?",
            choices=[t.nickname for t in env.current_party]
        ).ask()
        for t in env.current_party:
            if t.nickname == pick:
                env.move_to_storage(t)
                questionary.print(
                    f"Moved {pick} to storage.", style="fg:green")
                break
        questionary.text("").skip_if(lambda _: True, default="").ask()


def breed_party(env):
    clear_screen()
    adults = [t for t in env.current_party if t.lifestage == LifeStage.ADULT]
    if len(adults) < 2:
        questionary.print(
            "Need at least 2 adults in your party to breed!", style="bold fg:red")
        questionary.text("").skip_if(lambda _: True, default="").ask()
        return
    parent1 = questionary.select(
        "Choose first parent:",
        choices=[t.nickname for t in adults]
    ).ask()
    parent2 = questionary.select(
        "Choose second parent:",
        choices=[t.nickname for t in adults if t.nickname != parent1]
    ).ask()
    t1 = next(t for t in adults if t.nickname == parent1)
    t2 = next(t for t in adults if t.nickname == parent2)
    child = t1.breed(t2)
    if child:
        questionary.print(
            f"New baby {child.nickname} added to storage!", style="bold fg:green")
    questionary.text("").skip_if(lambda _: True, default="").ask()


def manage_breeding_room(env):
    clear_screen()
    print("-- Breeding Room --\n")
    if not env.breeding_pairs:
        print("No pairs currently breeding.")
    else:
        for idx, pair in enumerate(env.breeding_pairs, start=1):
            left = max(0, 200 - pair['elapsed'])
            print(f"{idx}. {pair['parent1'].nickname} × {
                  pair['parent2'].nickname} ({left//100} days left)")
    storage_adults = [t for t in env.storage if t.lifestage == LifeStage.ADULT]
    if len(storage_adults) >= 2:
        add = questionary.confirm(
            "Add a new breeding pair from storage?").ask()
        if add:
            p1_name = questionary.select("First parent:", choices=[
                                         t.nickname for t in storage_adults]).ask()
            p1 = next(t for t in storage_adults if t.nickname == p1_name)
            remaining = [t for t in storage_adults if t != p1]
            p2_name = questionary.select("Second parent:", choices=[
                                         t.nickname for t in remaining]).ask()
            p2 = next(t for t in remaining if t.nickname == p2_name)
            env.start_breeding(p1, p2)
    else:
        print("Not enough adults in storage to breed.")
    questionary.text("\nPress Enter to continue…").ask()


def study_session(env):
    clear_screen()
    questionary.print("You begin studying for 2 hours…", style="bold fg:blue")
    countdown(3600)  # 1 hour timer (real)
    cont = questionary.confirm("Continue studying the second hour?").ask()
    if cont:
        countdown(3600)
    questionary.print("\n2 hours complete. 4 game days pass…", style="fg:blue")
    env.passtime(400)

    # Catch 2 wilds
    questionary.print(
        "\nYou spot and catch 2 wild Termimons!", style="fg:green")
    all_types = ["Fire", "Grass", "Steel", "Air", "Earth", "Water",
                 "Electric", "Technic", "Cosmic", "Dragon", "Mythic", "Ghost", "Sound"]
    for _ in range(2):
        wild_type = random.choice(all_types)
        wild = env.generate_starter(wild_type, to_party=False)
        questionary.print(f" • Caught {wild.info.Name} ({
                          wild_type}-type)!", style="fg:green")
    env.display()
    questionary.text("\nPress Enter to continue…").skip_if(
        lambda _: True, default="").ask()


def save_and_exit(env):
    env.save_to_file("termivironment_save.json")
    questionary.print("Game saved. Goodbye!", style="bold fg:green")


def main_menu(env):
    while True:
        clear_screen()
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "View Party",
                "View Storage",
                "Move Termimon (Party ↔ Storage)",
                "Breed Termimons (Party)",
                "Manage Breeding Room",
                "Study Session (2 h → 4 days)",
                "Save & Exit"
            ]).ask()

        if choice == "View Party":
            show_party(env)
        elif choice == "View Storage":
            show_storage(env)
        elif choice == "Move Termimon (Party ↔ Storage)":
            move_termimon(env)
        elif choice == "Breed Termimons (Party)":
            breed_party(env)
        elif choice == "Manage Breeding Room":
            manage_breeding_room(env)
        elif choice == "Study Session (2 h → 4 days)":
            study_session(env)
        elif choice == "Save & Exit":
            save_and_exit(env)
            break


def start_game():
    clear_screen()
    print("Welcome to TermiStudy! Each 2 h study session = 4 game days.")
    print("You start with TWO random adult Termimons. Breed, train, and manage your party as you study!")
    try:
        env = TermiVironment.load_from_file("termivironment_save.json")
    except Exception:
        env = TermiVironment()
        starter_types = ["Fire", "Grass"]
        for stype in starter_types:
            entity = env.generate_starter(stype, to_party=True)
            entity.age = 3000
            entity.progress_age(0)
        env.passtime(0)
        env.save_to_file("termivironment_save.json")
    env.display()
    questionary.text("Press Enter to continue…").skip_if(
        lambda _: True, default="").ask()
    main_menu(env)


if __name__ == "__main__":
    start_game()
