import pathlib

from pygame import mixer


mixer.init()


DEFAULT_SFX_VOLUME = 0.3


SFX_DIR = pathlib.Path('sfx')
SFX_FILES = SFX_DIR.iterdir()
SFX = {file.stem: mixer.Sound(file) for file in SFX_FILES}


def set_sfx_volume(vol):
    global SFX
    for s_effect in SFX.values():
        s_effect.set_volume(vol)


def play_sfx(name: str):
    SFX[name].play()
