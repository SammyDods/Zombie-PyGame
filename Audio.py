"""Shared sound effects with volume and pitch helpers."""
from os.path import exists, join as join_path, dirname, splitext
from random import choice
import pygame
import GameState

_sfx_sounds = []  # list of (sound, volume_scale)
_zombie_variants = []
_explode_sound = None
_laser_sound = None
_jump_sound = None
_hover_sound = None
_hovered_buttons = set()

DEFAULT_SFX_SCALE = 0.1


def _audio_path(filename):
    """Prefer .ogg (pygbag/web), fall back to the given extension."""
    base = join_path(dirname(__file__), "Assets", "Audio")
    name, ext = splitext(filename)
    ogg_path = join_path(base, name + ".ogg")
    given_path = join_path(base, filename)
    if exists(ogg_path):
        return ogg_path
    return given_path


def _load_sound(filename):
    return pygame.mixer.Sound(_audio_path(filename))


def _resample(sound, pitch):
    """Return a new Sound pitched by `pitch` (>1 higher, <1 lower)."""
    import numpy as np

    arr = pygame.sndarray.array(sound)
    if arr.size == 0:
        return sound
    indices = np.round(np.arange(0, len(arr), pitch)).astype(int)
    indices = indices[indices < len(arr)]
    if len(indices) == 0:
        return sound
    pitched = np.ascontiguousarray(arr[indices])
    return pygame.sndarray.make_sound(pitched)


def init(laser_sound=None):
    """Load SFX and build pitched zombie variants. Call after mixer init."""
    global _explode_sound, _laser_sound, _zombie_variants, _sfx_sounds
    global _jump_sound, _hover_sound

    _laser_sound = laser_sound if laser_sound is not None else _load_sound("laser.ogg")
    _explode_sound = _load_sound("retro-video-game-sfx-explode.ogg")
    _jump_sound = _load_sound("launching-1.ogg")
    _hover_sound = _load_sound("button-hover.ogg")
    base_zombie = _load_sound("zombie-tries-to-talk.ogg")

    pitches = (0.75, 0.85, 0.95, 1.05, 1.15, 1.25)
    _zombie_variants = []
    try:
        for pitch in pitches:
            _zombie_variants.append(_resample(base_zombie, pitch))
    except Exception:
        _zombie_variants = [base_zombie]

    _sfx_sounds = [
        (_laser_sound, DEFAULT_SFX_SCALE),
        (_explode_sound, DEFAULT_SFX_SCALE),
        (_jump_sound, DEFAULT_SFX_SCALE),
        (_hover_sound, 1.0),
    ] + [(variant, DEFAULT_SFX_SCALE) for variant in _zombie_variants]
    apply_volumes()


def music_path():
    return _audio_path("723496__tomentum__80s-space-mission-music.ogg")


def apply_volumes():
    for sound, scale in _sfx_sounds:
        if sound is not None:
            sound.set_volume(min(1.0, GameState.sfx_volume * scale))


def play_laser():
    if _laser_sound is not None:
        _laser_sound.play()


def play_explode():
    if _explode_sound is not None:
        _explode_sound.play()


def play_jump():
    if _jump_sound is not None:
        _jump_sound.play()


def play_button_hover():
    if _hover_sound is not None:
        _hover_sound.play()


def handle_button_hover(button_id, hovered):
    """Play hover sound once when the cursor first enters a button."""
    if hovered:
        if button_id not in _hovered_buttons:
            _hovered_buttons.add(button_id)
            play_button_hover()
    else:
        _hovered_buttons.discard(button_id)


def play_zombie_moan():
    if not _zombie_variants:
        return
    sound = choice(_zombie_variants)
    sound.play()
