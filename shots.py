# -*- encoding: utf-8 -*-

from math import atan2
from copy import copy

from sample_data.helpers import spawn_enemy
from pytouhou.game.bullet import SampleBullet

##
# PRIVATE STUFF
# WARNING: Do not use directly. Use the shoot_* family of functions instead!
#          (it’s down below)
##
def temp_fire(self, game, offset=None, bullet_attributes=None, launch_pos=None, custom_update = None, custom_attributes = ()):
    (
        type_idx, sprite_idx_offset,
        speed, angle
    ) = bullet_attributes

    bullet_type = game.bullet_types[type_idx]

    if launch_pos is None:
        ox, oy = offset or self.bullet_launch_offset
        launch_pos = self.x + ox, self.y + oy

    if speed < 0.3 and speed != 0.0:
        speed = 0.3

    player = self.select_player()

    bullets = game.bullets
    nb_bullets_max = game.nb_bullets_max

    if nb_bullets_max is None or len(bullets) < nb_bullets_max:
        bullets.append(
            SampleBullet(
                launch_pos,
                bullet_type,
                sprite_idx_offset,
                angle,
                speed,
                player,
                game,
                custom_update = custom_update,
                custom_attributes = custom_attributes
            )
        )

##
# PUBLIC API BELOW
##

class Shot(object):
    def __init__(self, type = 0, speed = 3.0, angle = 0., delay = 0, color = 0, offset = None, launch_pos = None, custom_update = None, custom_attributes = ()):
        self.type = type
        self.speed = speed
        self.angle = angle
        self.delay = delay
        self.color = color
        self.launch_pos = launch_pos
        self.offset = offset
        self.custom_update = custom_update
        self.custom_attributes = custom_attributes

def shoot_single(enemy, game, shot):
    if shot.delay == 0:
        temp_fire(
            enemy, game,
            bullet_attributes = (
                shot.type,
                shot.color,
                shot.speed,
                shot.angle
            ),
            offset = shot.offset,
            launch_pos = shot.launch_pos,
            custom_update = shot.custom_update,
            custom_attributes = shot.custom_attributes
        )
    else:
        # FIXME: This method is ugly. I’d be happier if we could find a nicer
        #        way of doing this.
        # add_burst(enemy, game, shot)
        shot = copy(shot)
        def update(helper, game):
            helper.x = enemy.x
            helper.y = enemy.y

            if helper.frame == 0:
                enemy.touchable = False
                enemy.collidable = False
                enemy.visible = False
            elif helper.frame == shot.delay:
                shot.delay = 0

                shoot_single(helper, game, shot)

        spawn_enemy(game, update, enemy.x, enemy.y)

def shoot_at(enemy, game, target, shots):
    # FIXME: Copy the shots?
    for shot in shots:
        shot.angle += atan2(target.y - enemy.y, target.x - enemy.x)
        shoot_single(enemy, game, shot)

def shoot(enemy, game, shots):
    for shot in shots:
        shoot_single(enemy, shot)

def row(shots_per_row, angle_between_shots, shots):
    new_shots = []

    for shot in shots:
        for i in xrange(shots_per_row):
            new_shot = copy(shot)
            new_shot.angle = (
                shot.angle -
                    (i - (shots_per_row - 1) / 2.) * angle_between_shots
            )

            new_shots.append(new_shot)

    return new_shots

