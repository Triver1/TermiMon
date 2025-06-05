import os
import time
import random

import questionary
from termimon.termimon import TermiVironment, LifeStage

# Helper to clear the terminal screen


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Real-time countdown (seconds) with HH:MM:SS display


def countdown(duration_seconds):
    for remaining in range(duration_seconds, 0, -1):
        hrs, rem = divmod(remaining, 3600)
        mins, secs = divmod(rem, 60)
        timer_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        print(f"\rStudying… Time left: {timer_str}", end="", flush=True)
        time.sleep(1)
    print("\rStudying… Time left: 00:00:00          ")


def start_game():
    clear_screen()
    print("Welcome to TermiStudy! Each 2 h study session = 4 game days.")
    print("You start with TWO random adult Termimons. Breed, train, and manage your party as you study!")
    env = TermiVironment()

    # Generate two adult starters and add to party
    starter_types = ["Fire", "Grass"]
    for stype in starter_types:
        entity = env.generate_starter(stype, to_party=True)
        entity.age = 3000  # Force into ADULT stage
        entity.progress_age(0)
    env.passtime(0)  # Trigger any stage updates
    env.display()
    main_loop(env)


def main_loop(env: TermiVironment):
    while True:
        clear_screen()
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "View Party",
                "View Storage",
                "Move Termimon (Party ↔ Storage)",
                "Breed Termimons (Party)",
                "Study Session (2 h → 4 days)",
                "Save & Exit"
            ]).ask()

        if choice == "View Party":
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

        elif choice == "View Storage":
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

        elif choice == "Move Termimon (Party ↔ Storage)":
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
                    questionary.text("").skip_if(
                        lambda _: True, default="").ask()
                    continue
                if len(env.current_party) >= 6:
                    questionary.print("Party is full!", style="bold fg:red")
                    questionary.text("").skip_if(
                        lambda _: True, default="").ask()
                    continue
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

            else:  # Party → Storage
                if not env.current_party:
                    questionary.print("Party is empty!", style="bold fg:red")
                    questionary.text("").skip_if(
                        lambda _: True, default="").ask()
                    continue
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

        elif choice == "Breed Termimons (Party)":
            clear_screen()
            adults = [t for t in env.current_party if t.lifestage ==
                      LifeStage.ADULT]
            if len(adults) < 2:
                questionary.print(
                    "Need at least 2 adults in your party to breed!", style="bold fg:red")
                questionary.text("").skip_if(lambda _: True, default="").ask()
                continue

            parent1 = questionary.select(
                "Choose first parent:",
                choices=[t.nickname for t in adults]
            ).ask()
            parent2 = questionary.select(
                "Choose second parent:",
                choices=[t.nickname for t in adults]
            ).ask()
            if parent1 == parent2:
                questionary.print(
                    "Cannot breed the same Termimon with itself!", style="bold fg:red")
                questionary.text("").skip_if(lambda _: True, default="").ask()
                continue

            t1 = next(t for t in adults if t.nickname == parent1)
            t2 = next(t for t in adults if t.nickname == parent2)
            child = t1.breed(t2)
            if child:
                questionary.print(
                    f"New baby {child.nickname} added to storage!", style="bold fg:green")
            questionary.text("").skip_if(lambda _: True, default="").ask()

        elif choice == "Study Session (2 h → 4 days)":
            clear_screen()
            questionary.print(
                "You begin studying for 2 hours…", style="bold fg:blue")
            # Real-time 1 hour countdown
            countdown(3600)

            # After 1 hour, student can choose to keep studying another hour or finish.
            cont = questionary.confirm(
                "Continue studying the second hour?").ask()
            if cont:
                countdown(3600)

            # Once 2 hours are up, advance 4 in-game days
            questionary.print(
                "\n2 hours complete. 4 game days pass…", style="fg:blue")
            env.passtime(400)

            # Catch 2 random wild Termimons (added to storage)
            questionary.print(
                "\nYou spot and catch 2 wild Termimons!", style="fg:green")
            all_types = ["Fire", "Grass", "Steel", "Air", "Earth", "Water",
                         "Electric", "Technic", "Cosmic", "Dragon", "Mythic", "Ghost", "Sound"]
            for _ in range(2):
                wild_type = random.choice(all_types)
                wild = env.generate_starter(
                    wild_type, to_party=False)  # added to storage
                questionary.print(f" • Caught {wild.info.Name} ({
                                  wild_type}-type)!", style="fg:green")

            env.display()
            questionary.text("\nPress Enter to continue…").skip_if(
                lambda _: True, default="").ask()

        else:  # "Save & Exit"
            env.save_to_file("termivironment_save.json")
            questionary.print("Game saved. Goodbye!", style="bold fg:green")
            break


if __name__ == "__main__":
    start_game()
