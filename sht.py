# -*- encoding: utf-8 -*-
##
## Copyright (C) 2013 Emmanuel Gil Peyrot <linkmauve@linkmauve.fr>
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

from math import radians
from pytouhou.formats.exe import SHT, Shot


player0 = SHT()
player0.horizontal_vertical_speed = 2.
player0.horizontal_vertical_focused_speed = 1.5
player0.diagonal_speed = 1.5
player0.diagonal_focused_speed = 1.

shot = Shot()
shot.interval = 10
shot.delay = 5
shot.pos = (0, -32)
shot.hitbox = (5, 5)
shot.angle = radians(-90)
shot.speed = 5.
shot.damage = 16
shot.orb = 0
shot.type = 2
shot.sprite = 64
shot.unknown1 = 0

# Always at least define the shot for max power.
player0.shots[999] = [shot]

characters = [(player0, player0)]
