# -*- encoding: utf-8 -*-
##
## Copyright (C) 2011 Thibaut Girka <thib@sitedethib.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 3 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##

from math import cos, sin

from pytouhou.vm import ANMRunner
from pytouhou.game.bullet import Bullet
from pytouhou.game.bullettype import BulletType
from pytouhou.game.sprite import Sprite

class SampleBullet(Bullet):
    def __init__(self, pos, bullet_type, sprite_idx_offset,
                       angle, speed, target, game,
                       hitbox=None, custom_update = None, custom_attributes = ()):
        Bullet.__init__(self, pos, bullet_type, game, hitbox, angle, sprite_idx_offset)

        self.grazed = False

        self.target = target

        self.custom_update = custom_update
        self.custom_attributes = custom_attributes

        self.speed = speed
        self.dx, self.dy = cos(angle) * speed, sin(angle) * speed

        self.launch()


    def set_anim(self, sprite_idx_offset=None):
        if sprite_idx_offset is not None:
            self.sprite_idx_offset = sprite_idx_offset

        bt = self._bullet_type
        self.sprite = Sprite()
        self.sprite.angle = self.angle
        self.anmrunner = ANMRunner(bt.anm, bt.anim_index,
                                   self.sprite, self.sprite_idx_offset)


    def launch(self):
        Bullet.launch(self)

        self.frame = 0
        self.dx, self.dy = cos(self.angle) * self.speed, sin(self.angle) * self.speed

    def cancel(self):
        Bullet.cancel(self)

        # Cancel animation
        bt = self._bullet_type
        self.sprite = Sprite()
        self.sprite.angle = self.angle
        self.anmrunner = ANMRunner(bt.anm, bt.cancel_anim_index,
                                   self.sprite, bt.launch_anim_offsets[self.sprite_idx_offset])
        self.dx, self.dy = self.dx / 2., self.dy / 2.


    def update(self):
        self.update_anm()

        if self.state == LAUNCHING:
            pass
        elif self.state == CANCELLED:
            pass
        elif self.custom_update:
            self.custom_update(self, self._game)

        self.update_position()
        self.cleanup()


    def cleanup(self):
        game_width, game_height = self._game.width, self._game.height

        # Filter out-of-screen bullets
        if self.is_visible(game_width, game_height):
            self.was_visible = True
        elif self.was_visible:
            self.removed = True
