import sys
from adventurelib import *

from classes.attack import *
from app.Constants import *
from app.enums import *
from classes.effect import *
from commands import actions

greg_name = 'Greg'
pionteks_name = 'The Piontek Siblings'
tilly_name = 'Tilly'
noah_name = 'Noah'
gabe_name = 'Gabe'
cookies_name = 'Store-Bought Chocolate Chip Cookies'

character_mom = None
mom_attacks = {}
inventory = []
character_enemy = None
dict_enemies = {}
dict_effects = {}
dict_attacks = {}
enemy_order = [greg_name, pionteks_name, tilly_name, noah_name, gabe_name, cookies_name]
current_character_enemy_index = 0

global num_turns_in_battle


def init_game_data():
    '''
    TODO: This function will load hardcoded game data from JSON file(s) as well as initializing various data structures

    We will initialize the character_mom global with Mom's character object here, as well as the dict of enemy character
    objects.

    We will also initialize the dict of attacks within attacks.py by calling the 'load_attack_data' function
    '''
    init_effect_data()
    init_attack_data()
    init_character_data()
    return

def init_attack_data():
    # Linda's Attacks
    dict_attacks[Attacks.USE_REASON] = Attack(Attacks.USE_REASON, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.COOKIES] = Attack(Attacks.COOKIES, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.KICK] = Attack(Attacks.KICK, 40, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.BACH] = Attack(Attacks.BACH, 0, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.YAY] = Attack(Attacks.YAY, 0, Targets.SELF, Effects.NONE)
    dict_attacks[Attacks.BIG_SALE] = Attack(Attacks.BIG_SALE, 20, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.GIVE_ADVICE] = Attack(Attacks.GIVE_ADVICE, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.INCORRECT_REFERENCE] = (Attacks.INCORRECT_REFERENCE, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.GABE_COAT] = Attack(Attacks.GABE_COAT, 20, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.LONG_TIME_MAKEUP] = Attack(Attacks.LONG_TIME_MAKEUP, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.WATER_DOWN_COFFEE] = Attack(Attacks.WATER_DOWN_COFFEE, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.INSIST_ON_UBER] = Attack(Attacks.INSIST_ON_UBER, 17, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.CHANGE_SUBJECT] = Attack(Attacks.CHANGE_SUBJECT, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.INSIST_DINNER_LINDA] = Attack(Attacks.INSIST_DINNER_LINDA, 17, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.AIR_CANNON] = Attack(Attacks.AIR_CANNON, 5, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.CALL_GABE] = Attack(Attacks.CALL_GABE, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.YELL_AT_TILLY] = Attack(Attacks.YELL_AT_TILLY, 10, Targets.ENEMY, Effects.NONE)

    # Greg's Attacks
    dict_attacks[Attacks.MILD_SEXISM] = Attack(Attacks.MILD_SEXISM, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.SELL_COMPANY] = Attack(Attacks.SELL_COMPANY, 5, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.IGNORE_ADVICE] = Attack(Attacks.IGNORE_ADVICE, 10, Targets.BOTH, Effects.NONE)
    dict_attacks[Attacks.BLAME_LINDA] = Attack(Attacks.BLAME_LINDA, 15, Targets.ENEMY, Effects.NONE)

    # Piontek Siblings' Attacks
    dict_attacks[Attacks.VOTE_TRUMP] = Attack(Attacks.VOTE_TRUMP, 8, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.INSIST_DINNER_SIBLINGS] = Attack(Attacks.INSIST_DINNER_SIBLINGS, 13, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.PICK_ON_LINDA] = Attack(Attacks.PICK_ON_LINDA, 15, Targets.ENEMY, Effects.NONE)

    # Tilly's Attacks
    dict_attacks[Attacks.SCARF_AND_BARF] = Attack(Attacks.SCARF_AND_BARF, 8, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.DEAD_MOUSE] = Attack(Attacks.DEAD_MOUSE, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.ALIVE_MOUSE] = Attack(Attacks.ALIVE_MOUSE, 15, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.HAIRBALL] = Attack(Attacks.HAIRBALL, 8, Targets.ENEMY, Effects.NONE)

    #Gabe's Attacks
    dict_attacks[Attacks.SLEEP_TILL_3] = Attack(Attacks.SLEEP_TILL_3, 0, Targets.SELF, Effects.NONE)
    dict_attacks[Attacks.GABE_OUT] = Attack(Attacks.GABE_OUT, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.STOP] = Attack(Attacks.STOP, 10, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.OBSCURE_REFERENCE] = Attack(Attacks.OBSCURE_REFERENCE, 0, Targets.ENEMY, Effects.CONFUSION)

    # Noah's Attacks
    dict_attacks[Attacks.TOXIC_FART] = Attack(Attacks.TOXIC_FART, 0, Targets.ENEMY, Effects.POISON)
    dict_attacks[Attacks.HANGER] = Attack(Attacks.HANGER, 17, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.SAY_FAM] = Attack(Attacks.SAY_FAM, 10, Targets.BOTH, Effects.NONE)
    dict_attacks[Attacks.HERPDY_DERP] = Attack(Attacks.HERPDY_DERP, 0, Targets.ENEMY, Effects.SKIP_NEXT_TURN)

    # Store-Bought Cookie's Attacks
    dict_attacks[Attacks.LOOK_TASTY] = Attack(Attacks.LOOK_TASTY, 1, Targets.ENEMY, Effects.NONE)
    dict_attacks[Attacks.SIT_THERE] = Attack(Attacks.SIT_THERE, 0, Targets.ENEMY, Effects.NONE)

    return


def init_character_data():


def init_effect_data():
    dict_effects[Effects.NONE] = Effect(Effects.NONE, '', -1)
    dict_effects[Effects.CONFUSION] = Effect(Effects.CONFUSION, 'Linda became confused!', 3)
    dict_effects[Effects.LOW_BLOOD_SUGAR] = Effect(Effects.LOW_BLOOD_SUGAR, 'Gabe got low blood sugar!\nGsbe\'s attack increased 50%!', -1)
    dict_effects[Effects.POISON] = Effect(Effects.POISON, 'Linda was poisoned by Noah\'s farts!', 3)
    dict_effects[Effects.SKIP_NEXT_TURN] = Effect(Effects.SKIP_NEXT_TURN, 'Linda\'s turn was skipped!', -1)
    dict_effects[Effects.SUPER_RELAXED] = Effect(Effects.SUPER_RELAXED, 'Linda became super relaxed!\nLinda is now invincible!', 2)


def print_start_of_game_text():
    print(title_banner)
    print(intro_text)
    print(instructions)

def print_new_enemy_text():
    

def main():
    init_game_data()
    set_context('attacking.greg')
    global character_enemy
    character_enemy = dict_enemies['Greg']
    print_start_of_game_text()
    start()


def enemy_turn():
    '''
    This function will be called at the end of any of Mom's attack functions during a battle. It will handle all logic of
    the enemy's turn (random attack choice, timing between attack being printed and flavor text being printed)

    Ex: if Gabe fight goes on for more than x turns, he develops low blood sugar. Custom function is called every turn which
    checks if num_turns > low_blood_sugar_turns
    '''
    if character_enemy.active_effect.name is Effects.SKIP_NEXT_TURN:
        print(f'{character_enemy.name}\'s turn was skipped!')
        character_enemy.active_effect = Effects.NONE
        return
    if character_enemy is dict_enemies['Gabe'] and num_turns_in_battle == 5:
        character_enemy.damage_boost = 1.5
    if character_enemy is dict_enemies['Tilly'] and num_turns_in_battle == 10:
        print('Tilly ran outside. The fight is over.')
        end_battle(character_enemy)


def end_battle(losing_character):
    '''
    This function is called when a fight ends. It handles the cases where the enemy lost, and where Mom lost
    '''
    if losing_character is character_mom:
        print("You were defeated! Oh no...")
        # TODO: switch 'Game Over' to ASCII art text
        print(game_over)
        sys.exit()

    # First, print out character defeat info
    print(f'{losing_character.name} was defeated!')
    # TODO: Increase Mom's points here and print notification

    # Set the next enemy Mom will face, and reset her damage boost and active effect. Set context to 'break' to enable
    # break actions
    global current_character_enemy_index
    current_character_enemy_index += 1
    global character_enemy
    character_enemy = dict_enemies[enemy_order[current_character_enemy_index]]
    set_context('break')
    character_mom.damage_boost = 1.0
    character_mom.active_effect = Effects.NONE

def start_battle():
    new_context = 'attacking.'+character_enemy.name
    set_context(new_context)
    print(f'Next combatant: {character_enemy.name}!!!!')




if __name__ == '__main__':
    main()