from pathlib import Path

import numpy as np


MU = 255


def load_data_ulaw(input_file: Path) -> np.ndarray:
    input_bytes = input_file.read_bytes()
    uint8_bytes = np.frombuffer(input_bytes, dtype=np.uint8)
    y = (uint8_bytes / 255.0) * 2 - 1
    y = np.sign(y) * ((1 + MU) ** np.abs(y) - 1) / MU  # μ-law F^-1
    return y


def make_output_file(input_file: Path) -> Path:
    ext = input_file.suffix
    return input_file.with_suffix(f".bent{ext}")


def save_data_ulaw(bend: np.ndarray, output_file: Path):
    x = np.clip(bend, -1, 1)
    x = np.sign(x) * (np.log1p(MU * np.abs(x)) / np.log1p(MU))  # μ-law F
    output_bytes = np.round(np.clip((x + 1) / 2 * 255, 0, 255)).astype(np.uint8).tobytes()
    output_file.write_bytes(output_bytes)
