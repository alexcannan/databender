from pathlib import Path

import numpy as np


FLIP_LATTER_HALF = True
MU = 255


def load_data_ulaw(input_file: Path) -> np.ndarray:
    input_bytes = input_file.read_bytes()
    uint8_array = np.frombuffer(input_bytes, dtype=np.uint8)
    if FLIP_LATTER_HALF:
        uint8_array = np.where(uint8_array >= 0x80, 0xFF - uint8_array + 0x80, uint8_array)
    y = (uint8_array / 255.0) * 2 - 1
    y = np.sign(y) * ((1 + MU) ** np.abs(y) - 1) / MU  # μ-law F^-1
    return y


def make_output_file(input_file: Path) -> Path:
    ext = input_file.suffix
    return input_file.with_suffix(f".bent{ext}")


def save_data_ulaw(bend: np.ndarray, output_file: Path):
    x = np.clip(bend, -1, 1)
    x = np.sign(x) * (np.log1p(MU * np.abs(x)) / np.log1p(MU))  # μ-law F
    uint8_array = np.round(np.clip((x + 1) / 2 * 255, 0, 255)).astype(np.uint8)
    if FLIP_LATTER_HALF:
        uint8_array = np.where(uint8_array >= 0x80, 0xFF - uint8_array + 0x80, uint8_array)
    output_bytes = uint8_array.tobytes()
    output_file.write_bytes(output_bytes)
