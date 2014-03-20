# -*- encoding: utf-8 -*-

from copy import copy
from math import atan2
from math import radians, cos, sin, pi

from sample_data.helpers import spawn_enemy, distance_to_border
from sample_data.shots import Shot, shoot_single, shoot_at, shoot, circle, row, reset_bullet_movement
from sample_data.bossmode import Spell, bossmode

##
# And so it begins.
##

def gravity(bullet, f = 10000.):
    bullet.y += (bullet.frame ** 2) / f

def flowers_petals(game, timeout):
    def update(bullet):
        gravity(bullet)

        if (game.frame - timeout) % 120 == 0:
            # FIXME: sprite_idx_offset == sucky name
            bullet.sprite_idx_offset += 2
            bullet.sprite_idx_offset %= 8

            bullet.set_anim()

        if game.frame == timeout:
            bullet.cancel()

    return update

def flowers_custom_update(enemy, game, timeout):
    def update(bullet):
        gravity(bullet, 2500.)

        if bullet.frame % 14 == 13:
            if distance_to_border(bullet, game) < 13:
                return

            r = 9
            angle_offset = game.prng.rand_double() * 2 * pi
            offset = (
                game.prng.rand_uint16() % 33 - 16,
                game.prng.rand_uint16() % 33 - 16
            )
            for i in xrange(5):
                angle = 2 * pi / 5 * i + angle_offset

                shoot_single(
                    enemy, game,
                    Shot(
                        type = 2,
                        angle = angle,
                        color = 1,
                        speed = 0.,
                        launch_pos = (
                            bullet.x + r * cos(angle) + offset[0],
                            bullet.y + r * sin(angle) + offset[1]
                        ),
                        custom_update = flowers_petals(game, timeout)
                    )
                )

                angle = angle + 2. * pi / 5. * 0.5
                shoot_single(
                    enemy, game,
                    Shot(
                        type = 2,
                        angle = angle,
                        color = 1,
                        speed = 0.,
                        launch_pos = (
                            bullet.x + 1.666 * r * cos(angle) + offset[0],
                            bullet.y + 1.666 * r * sin(angle) + offset[1]
                        ),
                        custom_update = flowers_petals(game, timeout)
                    )
                )

    return update
        

##
# Chiro’s ashes all over again.
# @todo grooming
# @todo boss movements
# @todo better colors management
##
def spell1(enemy, game, frame):
    if frame % 120 == 0:
        shoot_at(
            enemy, game,
            game.players[0],
            [
                Shot(
                    type = 9,
                    angle = 2 * pi / 5 * (i + 0.5),
                    custom_update = flowers_custom_update(
                        enemy, game, game.frame + 480
                    ),
                    delay = i * 8
                ) for i in xrange(5)
            ]
        )

        # FIXME: workaround. Seriously. Remove that ASAP.
        if frame == 0:
            enemy.frame += 1

    if frame % 180 == 0 and frame > 0:
        shoot_at(
            enemy, game,
            game.players[0],
            [
                Shot(
                    type = 1,
                    color = 5,
                    angle = 2 * pi / 6 * i,
                    speed = 1.6
                ) for i in xrange(6)
            ]
        )

def spell2_bullet(bullet, game):
    if bullet.frame == 40:
        # FIXME
        player = game.players[0]
        bullet.angle = atan2(player.y - bullet.y, player.x - bullet.x)
        reset_bullet_movement(bullet)

def spell2(enemy, game, frame):
    if frame % 120 == 0:
        shoot(
            enemy, game,
            circle(36, row(2, 0.04, [
                Shot(type = 1, color= 13),
                Shot(type = 1, color= 13, delay = 3),
            ]))
        )
    elif frame % 120 == 12:
        shoot(
            enemy, game,
            circle(36, row(2, 0.04, [
                Shot(type = 1, color= 14, angle = pi / 4),
                Shot(type = 1, color= 14, angle = pi / 4, delay = 3),
            ]))
        )
    elif frame % 120 == 24:
        shoot(
            enemy, game,
            circle(36, row(2, 0.04, [
                Shot(type = 1, color= 13),
                Shot(type = 1, color= 13, delay = 3),
            ]))
        )

    for i in xrange(6):
        if frame % 120 == 24 + 12 * i:
            shoot(
                enemy, game,
                circle(4, row(2, 0.04, [
                    Shot(type = 1, color= 3 + i % 2),
                    Shot(type = 1, color= 3 + i % 2, delay = 3),
                ]))
            )
        if frame % 120 == 24 + 12 * i:
            shoot(
                enemy, game,
                circle(4, row(2, 0.04, [
                    Shot(type = 1, angle = pi / 4, color = 7 + i % 2, custom_update = spell2_bullet),
                    Shot(type = 1, angle = pi / 4, color = 7 + i % 2, custom_update = spell2_bullet, delay = 3),
                ]))
            )

def exampleEntry(enemy, game):
    if enemy.frame == 0:
        enemy.set_anim(0)
        enemy.speed = 1.
        enemy.angle = pi / 2
    elif enemy.frame == 120:
        enemy.speed = 0.
        return True

def example(enemy, game):
    bossmode(enemy, game,
        exampleEntry,
        [Spell(True, spell2, 800, 30 * 60, end_of_life = True)]
        [Spell(True, spell1, 800, 30 * 60, end_of_life = True)]
    )

def stage1(_game):
    global game
    game = _game

    if game.frame == 0:
        spawn_enemy(game, example, game.width / 2., -32.)

