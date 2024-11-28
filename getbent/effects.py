"""
effects can be passed into the command line with a syntax similar to ffmpeg filters.
name=key1=value1:key2=value2:...
"""

import numpy as np


def process_effect(data: np.ndarray, effect_string: str) -> np.ndarray:
    if "=" in effect_string:
        effect_name, arg_string = effect_string.split("=", maxsplit=1)
        kwargs = {
            key: value
            for key, value in (arg.split("=") for arg in arg_string.split(":"))
        }
    else:
        effect_name = effect_string
        kwargs = {}
    if effect_name not in globals():
        raise ValueError(f"Unknown effect: {effect_name}")
    return globals()[effect_name](data, **kwargs)


def reverse(data: np.ndarray) -> np.ndarray:
    return data[::-1]


def invert(data: np.ndarray) -> np.ndarray:
    return -data
