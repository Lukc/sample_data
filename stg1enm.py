from pytouhou.formats.anm0 import ANM0

texture_name = u'stgenm.png'
width = 256
height = 256

class ANM(ANM0):
    def __init__(self, width, height, texture_name):
        self.version = -1
        self.size = (width, height)
        self.first_name = texture_name
        self.secondary_name = None

anm = ANM(width, height, texture_name)

sprites = {0: (1, 1, 56, 56),
           1: (1, 226, 15, 30)}

def ufo(self, sprite):
    global sprites
    global anm

    if self.frame == 0:
        sprite.anm = anm
        sprite.texcoords = sprites[0]
    elif self.frame == 1000:
        self.running = False

    sprite.rotations_3d = (0., 0., self.frame * 0.1)
    sprite.changed = True

def boss(self, sprite):
    global sprites

    if self.frame == 0:
        sprite.anm = anm
        sprite.texcoords = sprites[1]
        self.running = False

scripts = {0: ufo,
           3: boss}
