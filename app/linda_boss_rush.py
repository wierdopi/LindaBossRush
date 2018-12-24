import copy
import random
import sys
import time

import adventurelib
from adventurelib import when, get_context, set_context, start

from app.Constants import *
from app.enums import *
from classes.attack import Attack
from classes.character import Character
from classes.effect import *

greg_name = 'Greg'
pionteks_name = 'The Piontek Siblings'
tilly_name = 'Tilly'
noah_name = 'Noah'
gabe_name = 'Gabe'
cookies_name = 'Store-Bought Chocolate Chip Cookies'

inventory = []
dict_enemies = {}
dict_effects = {}
dict_attacks = {}
enemy_order = [greg_name, pionteks_name, tilly_name, noah_name, gabe_name, cookies_name]
current_character_enemy_index = 0
score = 0

num_turns_in_battle = 0
battle_over = False
standard_delay = 1
next_attack_delay = 2


def print_delayed(print_string, delay):
    time.sleep(delay)
    print(print_string)


def prompt():
    if 'attacking' in get_context():
        prompt_string = f"\nLinda's health:\t{character_mom.health_remaining} / {character_mom.max_health}" \
            f"\n{character_enemy.name}'s health:\t{character_enemy.health_remaining} / {character_enemy.max_health}" \
            f"\n > "
    else:
        prompt_string = f"\nLinda's health:\t{character_mom.health_remaining} / {character_mom.max_health}\n > "
    return prompt_string

def no_command_matches(command):
    print(f'"{command}" cannot be used in this fight.')


def decrement_health(character, health_lost):
    '''
    :param health_lost:
    '''
    if health_lost >= character.health_remaining:
        print_delayed(f'{character.name} was defeated!', standard_delay)
        end_battle(character)
        return
    else:
        character.health_remaining -= health_lost
        return


def increment_health(character, health_gained):
    character.health_remaining += health_gained
    if character.health_remaining > character.max_health:
        character.health_remaining = character.max_health


def apply_active_effect(character):
    '''
    :return: True if Mom's turn is skipped, False otherwise
    '''
    if character.active_effect.name == Effects.NONE:
        return False

    # Check if effect is still active
    if character.active_effect.turns_effective == 0:
        if character.active_effect.name == Effects.SUPER_RELAXED:
            print_delayed(f'{character.name} is no longer super relaxed.', standard_delay)
        elif character.active_effect.name == Effects.CONFUSION:
            print_delayed(f'{character.name} is no longer confused.', standard_delay)
        elif character.active_effect.name == Effects.POISON:
            print_delayed(f'The fart dispersed. {character.name} is no longer taking toxic damage.', standard_delay)
        character.active_effect = dict_effects[Effects.NONE]
        return False

    character.active_effect.turns_effective -= 1

    # If the effect is still active, handle it
    if character.active_effect.name == Effects.SKIP_NEXT_TURN:
        print_delayed(f'{character.name} was laughing too hard to do anything.', standard_delay)
        return True
    elif character.active_effect.name == Effects.POISON:
        print_delayed(f'{character.name} took 10 points of toxic damage from the lingering fart!', standard_delay)
        character.decrement_health(10)
        if battle_over:
            return True
        return False
    elif character.active_effect.name == Effects.CONFUSION:
        print_delayed(f'{character.name} is confused!', standard_delay)
        if random.randint(0,10) < 5:
            print_delayed(f'{character.name} hurt herself in her confusion!', standard_delay)
            character.decrement_health(10)
            if battle_over:
                return True
            return True
        else:
            return False

#########################################
#         Mom's Break Actions           #
#########################################

@when("brew coffee", context='break')
def brew_coffee():
    print_delayed('Linda brewed a cup of coffee.', standard_delay)
    print_delayed('One cup of coffee has been added to your inventory!', standard_delay)
    inventory.append('coffee')
    start_battle()


@when("go to wegmans", context='break')
def go_to_wegmans():
    print_delayed('Linda went to Wegmans and bought dark chocolates.', standard_delay)
    print_delayed('Two dark chocolates have been added to your inventory!', standard_delay)
    inventory.append('dark chocolate')
    inventory.append('dark chocolate')
    start_battle()


@when("drink red wine", context='break')
def drink_red_wine():
    print_delayed('Linda drank a glass of red wine.', standard_delay)
    character_mom.active_effect = copy.deepcopy(dict_effects[Effects.SUPER_RELAXED])
    print_delayed(character_mom.active_effect.text, standard_delay)
    start_battle()


@when("eat out at jojo", context='break')
def eat_out():
    print_delayed('Linda went out and got dinner at Jojo', standard_delay)
    print_delayed('It was a really good dinner. Linda\'s base health increased by 20 points!', standard_delay)
    character_mom.max_health += 20
    start_battle()


@when("go to body pump class", context='break')
def go_to_body_pump():
    print_delayed('Linda went to Body Pump.', standard_delay)
    print_delayed('Linda got PUMPED! Linda\'s attack damage increased!', standard_delay)
    character_mom.damage_boost = 1.3
    start_battle()



#########################################
#           Mom's Attacks               #
#########################################

@when("use reason", context='attacking.Greg')
@when("use reason", context='attacking.The Piontek Siblings')
@when("use reason", context='attacking.Tilly')
def use_reason():
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    attack_data = dict_attacks[Attacks.USE_REASON]
    if get_context() == 'attacking.tilly':
        print_delayed('It has no effect. Tilly is a cat. Duh.', standard_delay)
        enemy_turn()
        return
    else:
        print_delayed('Linda used "use reason"', standard_delay)
        damage = attack_data.damage * character_mom.damage_boost
        print_delayed(f'Linda did {damage} points of damage to {character_enemy.name}', standard_delay)
        decrement_health(character_enemy, damage)
        if battle_over:
            return
        else:
            enemy_turn()
            return

@when("roundhouse kick", context='attacking.Greg')
def roundhouse_kick():
    global character_mom
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    attack_data = dict_attacks[Attacks.KICK]
    print_delayed('Linda used "roundhouse kick"', standard_delay)
    damage = attack_data.damage * character_mom.damage_boost
    print_delayed(smash, standard_delay)
    print_delayed(f'Linda did {damage} points of damage to {character_enemy.name}', 3)
    decrement_health(character_enemy, damage)
    if battle_over:
        return
    else:
        enemy_turn()
        return


@when("close a big sale", context='attacking.Greg')
def close_sale():
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    attack_data = dict_attacks[Attacks.BIG_SALE]
    print_delayed('Linda used "close a big sale"', standard_delay)
    damage = attack_data.damage * character_mom.damage_boost
    print_delayed('Yay! (fingers apart)', standard_delay)
    print_delayed(f'Linda did {damage} points of damage to {character_enemy.name}', standard_delay)
    decrement_health(character_enemy, damage)
    if battle_over:
        return
    else:
        enemy_turn()
        return


@when("give good advice", context='attacking.Greg')
def give_good_advice():
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    attack_data = dict_attacks[Attacks.GIVE_ADVICE]
    damage = attack_data.damage * character_mom.damage_boost
    print_delayed('Linda used "give good advice"', standard_delay)
    print_delayed('Linda gave Greg some good advice! He said thanks and immediately ignored it, to his own detriment...', standard_delay)
    print_delayed(f'Linda did {damage} points of damage to {character_enemy.name}', standard_delay)
    decrement_health(character_enemy, damage)
    if battle_over:
        return
    else:
        enemy_turn()
        return


@when("bake chocolate chip cookies", context='attacking.Gabe')
@when("bake chocolate chip cookies", context='attacking.Store-Bought Chocolate Chip Cookies')
def bake_cookies():
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    print_delayed('Linda used "bake chocolate chip cookies"', standard_delay)
    if character_enemy == dict_enemies[cookies_name]:
        print_delayed(instant_kill, standard_delay)
        print_delayed('The store-bought cookies could not compete!', standard_delay)
        end_battle(character_enemy)
    elif character_enemy == dict_enemies[gabe_name]:
        if character_enemy.active_effect.name == Effects.LOW_BLOOD_SUGAR:
            print_delayed('Gabe was cured of his low blood sugar! Gabe\'s attack returned to normal.', standard_delay)
            character_enemy.active_effect = dict_effects[Effects.NONE]
            character_enemy.damage_boost = 1.0
        else:
            print_delayed('Gabe was prevented from getting low blood sugar for 10 more turns.', standard_delay)
            global num_turns_in_battle
            num_turns_in_battle = 0
    enemy_turn()
    return




@when("use ITEM", context='attacking')
def use_item(item):
    if apply_active_effect(character_mom):
        if battle_over:
            return
        else:
            enemy_turn()
            return
    if battle_over:
        return

    if item not in inventory:
        print_delayed(f'You do not have any {item}', standard_delay)
        return
    else:
        inventory.remove(item)
        print_delayed(f'Linda used {item}', standard_delay)
        if item.lower() == 'dark chocolate':
            print_delayed('Linda was healed for 20 points!', standard_delay)
            character_mom.heal(20)
        elif item.lower() == 'coffee':
            print_delayed('Linda got wired! Linda\'s attack damage increased!', standard_delay)
            character_mom.damage_boost += 0.2
        else:
            print_delayed("ERROR: SOMETHING GOT MESSED UP!!!!!", standard_delay)
    enemy_turn()
    return


@when("view inventory")
def view_inventory():
    if len(inventory) == 0:
        print_delayed("Your inventory is empty", 0)
    print_delayed("Your inventory contains:", 0)
    for item in inventory:
        print_delayed(f'\t{item}', 0)
    return



#########################################
#           Enemy Attacks               #
#########################################
# TODO: change "character used attack" to "character attacked", also add punctuation
##### Greg's Attacks #####


def mild_sexism():
    attack_data = dict_attacks[Attacks.MILD_SEXISM]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nGreg used "mild sexism"', next_attack_delay)
    print_delayed('Greg said something mildly sexist! (Come on, dude...)', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def sell_company():
    attack_data = dict_attacks[Attacks.SELL_COMPANY]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nGreg used "sell company"', next_attack_delay)
    print_delayed('Greg sold Brand Integrity for fat stacks of cash! Linda now works for Reward Gateway...what a cruddy name', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def ignore_advice():
    attack_data = dict_attacks[Attacks.IGNORE_ADVICE]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nGreg used "ignore good advice"', next_attack_delay)
    print_delayed('Greg ignored the frankly quite helful advice of his underlings,\nhurting himself in the process', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Greg', standard_delay)
    decrement_health(character_mom, damage)
    decrement_health(character_enemy, damage)

def blame_linda():
    attack_data = dict_attacks[Attacks.IGNORE_ADVICE]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nGreg used "blame linda"', next_attack_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)


##### Piontek Siblings' Attacks #####
def vote_trump():
    attack_data = dict_attacks[Attacks.VOTE_TRUMP]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nThe Piontek Siblings used "vote for trump"', next_attack_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def insist_dinner_siblings():
    attack_data = dict_attacks[Attacks.INSIST_DINNER_SIBLINGS]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nThe Piontek Siblings used "insist on paying for dinner"', next_attack_delay)
    print_delayed('Linda feels bad for not paying', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def pick_on_linda():
    attack_data = dict_attacks[Attacks.PICK_ON_LINDA]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nThe Piontek Siblings used "pick on linda"', next_attack_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)


##### Tilly's Attacks #####
def scarf_and_barf():
    attack_data = dict_attacks[Attacks.SCARF_AND_BARF]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nTilly used "scarf and barf"', next_attack_delay)
    print_delayed('Ewww! Gaaaabe!', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def dead_mouse():
    attack_data = dict_attacks[Attacks.DEAD_MOUSE]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nTilly used "dead mouse surprise', next_attack_delay)
    print_delayed('Linda feels bad for that poor mouse', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def alive_mouse():
    attack_data = dict_attacks[Attacks.ALIVE_MOUSE]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nTilly used "dead mouse surprise"', next_attack_delay)
    print_delayed('Wait, is it dead?', standard_delay)
    print_delayed('Tilly used "alive mouse surprise"', standard_delay)
    print_delayed('Oh no! The mouse is still alive! Linda fled from the room!', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

def hairball():
    attack_data = dict_attacks[Attacks.HAIRBALL]
    damage = attack_data.damage * character_enemy.damage_boost
    print_delayed('\nTilly used "hairball"', next_attack_delay)
    print_delayed('Gross!', standard_delay)
    print_delayed(f'{character_enemy.name} did {damage} points of damage to Linda', standard_delay)
    decrement_health(character_mom, damage)

##### Gabe's Attacks #####
def sleep_till_3():
    # TODO: This heals, Noah pls do this one
    return

def gabe_out():
    return


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
    dict_attacks[Attacks.COOKIES] = Attack(Attacks.COOKIES, 0, Targets.ENEMY, Effects.NONE)
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
    dict_enemies[greg_name] = Character(greg_name, 100, [mild_sexism, sell_company, ignore_advice, blame_linda], dict_effects[Effects.NONE])
    dict_enemies[pionteks_name] = Character(pionteks_name, 100, [], dict_effects[Effects.NONE])
    dict_enemies[tilly_name] = Character(tilly_name, 50, None, dict_effects[Effects.NONE])
    dict_enemies[noah_name] = Character(noah_name, 100, None, dict_effects[Effects.NONE])
    dict_enemies[gabe_name] = Character(gabe_name, 100, None, dict_effects[Effects.NONE])
    dict_enemies[cookies_name] = Character(cookies_name, -1, None, dict_effects[Effects.NONE])

def init_effect_data():
    dict_effects[Effects.NONE] = Effect(Effects.NONE, '', -1)
    dict_effects[Effects.CONFUSION] = Effect(Effects.CONFUSION, 'Linda became confused!', 3)
    dict_effects[Effects.LOW_BLOOD_SUGAR] = Effect(Effects.LOW_BLOOD_SUGAR, 'Gabe got low blood sugar!\nGsbe\'s attack increased 50%!', -1)
    dict_effects[Effects.POISON] = Effect(Effects.POISON, 'Linda was poisoned by Noah\'s farts!', 3)
    dict_effects[Effects.SKIP_NEXT_TURN] = Effect(Effects.SKIP_NEXT_TURN, 'Linda\'s turn was skipped!', -1)
    dict_effects[Effects.SUPER_RELAXED] = Effect(Effects.SUPER_RELAXED, 'Linda became super relaxed!\nLinda is now invincible!', 2)


def print_start_of_game_text():
    print_delayed(title_banner_1, 1)
    print_delayed(title_banner_2, 1)
    print_delayed(title_banner_3, 1)
    print_delayed(title_banner_4, 1)
    print_delayed(title_banner_5, 1)
    print_delayed(title_banner_6, 1)
    print_delayed(title_banner_7, 1)
    print_delayed(intro_text, 5)
    print_delayed(greg_intro_text_1, 5)
    print_delayed(greg_intro_text_2, 2)
    print_delayed(greg_intro_text_3, 2)
    print_delayed(greg_intro_text_4, 2)
    print_delayed(instructions, 3)


def enemy_turn():
    '''
    This function is called at the end of any of Mom's attack functions during a battle. It will handle all logic of
    the enemy's turn (random attack choice, timing between attack being printed and flavor text being printed)
    '''
    if character_enemy is dict_enemies['Gabe'] and num_turns_in_battle == 5:
        character_enemy.active_effect = copy.deepcopy(dict_effects[Effects.Effects.LOW_BLOOD_SUGAR])
        character_enemy.damage_boost = 1.5
        character_enemy.damage_boost_turns_remaining = 1000
        print_delayed(character_enemy.active_effect.text, standard_delay)
    if character_enemy is dict_enemies['Tilly'] and num_turns_in_battle == 10:
        print_delayed('Tilly ran outside. The fight is over.', standard_delay)
        end_battle(character_enemy)

    outer_range = len(character_enemy.attacks)
    next_attack_int = random.randint(0, outer_range-1)
    next_attack = character_enemy.attacks[next_attack_int]


    if character_mom.active_effect.name == Effects.SUPER_RELAXED:
        print_delayed(f'{character_enemy.name} tried to attack, but Linda is so relaxed from the red wine that she is invincible!', standard_delay)
        print_delayed('Linda took no damage!', standard_delay)
    else:
        next_attack()
    return


def start_battle():
    global battle_over
    battle_over = False
    new_context = 'attacking.'+character_enemy.name
    set_context(new_context)
    print_delayed('\n\nNext combatant:', 3)
    print_delayed(f'{character_enemy.name}!!!!\n\n', next_attack_delay)
    print_delayed('Ready...', next_attack_delay)
    print_delayed('Fight!', next_attack_delay)


def end_battle(losing_character): # TODO: make mom's health go back to 100 at the start of each new fight? Maybe? Let's talk about it
    '''
    This function is called when a fight ends. It handles the cases where the enemy lost, and where Mom lost
    '''
    global num_turns_in_battle
    global character_enemy
    global current_character_enemy_index
    global battle_over
    if losing_character is character_mom:
        print_delayed(game_over, standard_delay)
        sys.exit()

    # First, print out character defeat info
    if losing_character is dict_enemies[tilly_name] and num_turns_in_battle == 10:
        print_delayed('Because Tilly escaped defeat, Linda did not gain any points', standard_delay)
    else:
        global score
        score += 10
        # TODO: Increment Mom's points here and print notification of current points held

    if character_enemy == dict_enemies[cookies_name]:
        print_end_game_text()
        sys.exit()

    # Set the next enemy Mom will face, and reset her damage boost and active effect. Set context to 'break' to enable
    # break actions
    num_turns_in_battle = 0
    current_character_enemy_index += 1
    character_enemy = dict_enemies[enemy_order[current_character_enemy_index]]
    set_context('break')
    character_mom.damage_boost = 1.0
    character_mom.active_effect = dict_effects[Effects.NONE]
    battle_over = True
    print_delayed('\n\nLinda went to the hooga zone', standard_delay)

def print_end_game_text():
    print_delayed(instant_kill, standard_delay)
    print_delayed(congrats, standard_delay)
    print_delayed(f'You have defeated all bosses! Your total score is {score}!', standard_delay)
    print_delayed(list_of_rewards, standard_delay)

def main():
    set_context('attacking.Greg')
    print_start_of_game_text()
    start()


adventurelib.prompt = prompt
adventurelib.no_command_matches = no_command_matches
init_game_data()
character_mom = Character('Linda', 100, None, dict_effects[Effects.NONE])
character_enemy = dict_enemies['Greg']

if __name__ == '__main__':
    main()