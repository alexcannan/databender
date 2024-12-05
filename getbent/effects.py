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


def add(data: np.ndarray, value: float=0.1) -> np.ndarray:
    return data + value


def echo(data: np.ndarray, delay: float=1.0, decay: float=0.5) -> np.ndarray:
    delay_hop = int(delay * SAMPLE_RATE)
    n_samples = data.shape[0]
    n_delays = n_samples // delay_hop

    decay_factors = decay ** np.arange(n_delays)
    echo_buffer = np.zeros_like(data)

    for i, decay_coeff in enumerate(decay_factors):
        start_idx = i * delay_hop
        end_idx = n_samples - start_idx
        echo_buffer[start_idx:] += data[:end_idx] * decay_coeff

    result = data + echo_buffer
    if True:
        result /= np.max(np.abs(result))
    return result

def hpfft(data: np.ndarray, cutoff: float=1000.0) -> np.ndarray:
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(data.shape[0], d=1/SAMPLE_RATE)
    high_pass = freqs > cutoff
    return np.fft.irfft(fft * high_pass)


def lpfft(data: np.ndarray, cutoff: float=1000.0) -> np.ndarray:
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(data.shape[0], d=1/SAMPLE_RATE)
    low_pass = freqs < cutoff
    return np.fft.irfft(fft * low_pass)


def convolve(data: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    return np.convolve(data, kernel, mode="same")


def lpf_convolve(data: np.ndarray, cutoff: float=1000.0, kernel_size: int=101) -> np.ndarray:
    normalized_cutoff = cutoff / SAMPLE_RATE / 2
    t = np.arange(-kernel_size // 2, kernel_size // 2)
    sinc_kernel = np.sinc(2 * normalized_cutoff * t)
    sinc_kernel *= np.hamming(kernel_size)
    sinc_kernel /= np.sum(sinc_kernel)
    return np.convolve(data, sinc_kernel, mode="same")
