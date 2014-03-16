# -*- encoding: utf-8 -*-

from pytouhou.game.enemy import Callback

current_card = -1

# TODO:
#   - Screen cleaning.
#   - Lives counting.
#   - Hitpoints counting.
#   - Scoring.
#   - Spellcards data.
#   - Many other things.

class Spell(object):
    def __init__(self, spellcard, code, life, timeout, end_of_life = False, drop = [], truce = 150, score = -1):
        self.spellcard = None if spellcard is False or None else spellcard
        self.life = life
        self.timeout = timeout
        self.code = code

        self.drop = drop
        self.end_of_life = end_of_life
        self.truce_time = truce

# game.kill_enemies() triggers callbacks, which is a problem.
def kill_enemies(game):
    for enemy in game.enemies:
        if not enemy.boss:
            enemy.life = 0

def death_callback(enemy, game, deck):
    global current_card

    print("Death callback.")

    enemy.frame = 0
    current_card = current_card + 1

    enemy.timeout = -1

def low_life_callback(enemy, game, deck):
    global current_card

    print("Low life callback.")

    enemy.frame = 0
    current_card = current_card + 1

    enemy.timeout = -1

def timeout_callback(enemy, game, deck):
    global current_card

    print("Timeout callback.")

    enemy.frame = 0
    current_card = current_card + 1

    # Lowering the life of the mob. For aesthetic purposes only.
    # Note that its life will be reset when the next card begins anyway.
    if enemy.low_life_trigger:
        enemy.low_life_callback = Callback()
        enemy.low_life_trigger, enemy.life = -1, enemy.low_life_trigger
    else:
        enemy.death_callback = Callback()
        enemy.life = 0

# FIXME: Does it work? Does it work?
def get_spell_life(enemy, deck, current_card):
    life = 0
    i = len(deck) - 1

    while i >= 0:
        card = deck[i]

        if card.end_of_life:
            life = card.life
        else:
            life = life + card.life

        if i == current_card:
            return life

        i = i - 1

    print("TROUBLE (get_spell_life): ", i, " :: ", len(deck), "  :: ", life, " :: ", current_card)

def bossmode(enemy, game, entry, deck, exit = None):
    global current_card

    if enemy.frame == 0:
        enemy.boss = True

        enemy.touchable = True
        enemy.damageable = False
    elif enemy.frame == 36000: # 10 minutes :|
        # “Emergency counter-trouble red-alert back-up stuff”.
        print("For some reason, this mob survived for too long.")
        enemy.removed = True

    #print(enemy.life, " :: ", current_card)
    if current_card == -1:
        if entry(enemy, game):
            current_card = 0
            enemy.frame = 0
    elif current_card == len(deck):
        if exit:
            exit(enemy, game)
        else:
            # FIXME: Maybe setting enemy.removed would be enough?
            enemy.death_flags = 0
            enemy.death_callback = Callback()
            enemy.life = 0
    else:
        card = deck[current_card]
        if enemy.frame >= card.truce_time:
            if enemy.frame == card.truce_time:
                if card.end_of_life or current_card + 1 >= len(deck):
                    # FIXME: somehow naming the flags might be of interest.
                    enemy.death_flags = 1
                    enemy.death_callback = Callback(death_callback, (enemy, game, deck))
                    enemy.life = card.life # get_spell_life is kinda pointless here.
                else:
                    enemy.low_life_callback = Callback(low_life_callback, (enemy, game, deck))
                    enemy.low_life_trigger = get_spell_life(enemy, deck, current_card + 1)
                    enemy.life = get_spell_life(enemy, deck, current_card)

                enemy.timeout_callback = Callback(timeout_callback, (enemy, game, deck))
                enemy.timeout = game.frame + card.timeout

                # Can be set back to False from the Spell’s code.
                enemy.touchable = True
                enemy.damageable = True

            card.code(enemy, game, enemy.frame - card.truce_time)

