


# VELA PULSAR
PAR_TEXT = r"""
f0              11.1946499395
F1              -1.5666E-11
F2              1.0280E-21
"""


# presets.py

PRESETS = {
    "crab": {
        "f0": 30.0,
        "f1": -0.0001,
        "f2": 0.0,
        "magnetic_tilt": 0.9,
        "noise_level": 0.7,
        "world_scale": 1.0
    },

    "vela": {
        "f0": 11.0,
        "f1": -0.00002,
        "f2": 0.0,
        "magnetic_tilt": 0.2,
        "noise_level": 0.35,
        "world_scale": 1.0
    },

    "millisecond": {
        "f0": 80.0,
        "f1": 0.0,
        "f2": 0.0,
        "magnetic_tilt": 0.2,
        "noise_level": 0.1,
        "world_scale": 1.0
    },

    "magnetar": {
        "f0": 2.0,
        "f1": -0.0005,
        "f2": 0.0001,
        "magnetic_tilt": 1.2,
        "noise_level": 1.0,
        "world_scale": 1.0
    },

    "psr_b1919": {
        "f0": 1.3,
        "f1": 0.0,
        "f2": 0.0,
        "magnetic_tilt": 0.4,
        "noise_level": 0.15,
        "world_scale": 1.0
    }
}