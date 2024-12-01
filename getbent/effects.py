"""
effects can be passed into the command line with a syntax similar to ffmpeg filters.
name=key1=value1:key2=value2:...
"""

import numpy as np


SAMPLE_RATE = 44100


def process_effect(data: np.ndarray, effect_string: str) -> np.ndarray:
    if "=" in effect_string:
        effect_name, arg_string = effect_string.split("=", maxsplit=1)
        kwargs = {
            key: float(value)
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


def add(data: np.ndarray, value: float) -> np.ndarray:
    return data + value


def echo(data: np.ndarray, delay: float=1.0, decay: float=0.5) -> np.ndarray:
    echo = data.copy()
    delay_hop = int(delay * SAMPLE_RATE)
    n_delays = data.shape[0] // delay_hop
    for i in range(n_delays):
        delay_i = echo[:data.shape[0] - i*delay_hop]
        decay_coeff = decay ** i
        delay_i *= decay_coeff
        data[i*delay_hop:] += delay_i
    return data