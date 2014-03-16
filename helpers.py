# -*- encoding: utf-8 -*-

from pytouhou.vm.common import EnemyRunner

def spawn_enemy(game, sub, x, y, life=1, item=-1, score=300, mirrored=False, random=False):
    instr_type = (2 if mirrored else 0) + (4 if random else 0)

    enemy = game.new_enemy((x, y, 0.), life, instr_type, item, score)
    enemy.process = EnemyRunner(enemy, game, sub)
    enemy.process.run_iteration()

    return enemy

def distance_to_border(element, game):
    return min(
        0 + element.x,
        0 + element.y,
        game.width - element.x,
        game.height - element.y
    )

