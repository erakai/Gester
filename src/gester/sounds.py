import pygame.mixer as mix

mix.init()

_loaded_sounds = {}


def pause():
    mix.pause()


def unpause():
    mix.unpause()


def force_quit():
    mix.stop()


def create_sound(name: str, path: str) -> None:
    global _loaded_sounds
    """
    Loads a sound that can be played
    """
    new_sound = mix.Sound(path)
    _loaded_sounds[name] = new_sound


def play_sound(name: str) -> None:
    """
    Plays a previously loaded sound
    """
    mix.Sound.play(_loaded_sounds[name])


def start_looping_sound(name: str) -> None:
    """
    Begin playing some previously created sound and loop it continuously
    """
    mix.Sound.play(_loaded_sounds[name], loops=-1)


def stop_looping_sound(name: str) -> None:
    """
    Stop playing a sound that is playing on loop
    """
    mix.Sound.stop(_loaded_sounds[name])
