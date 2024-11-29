from pathlib import Path

import numpy as np


MU = 255


def load_data_ulaw(input_file: Path) -> np.ndarray:
    with open(input_file, "rb") as f:
        input_bytes = f.read()
    uint8_bytes = np.frombuffer(input_bytes, dtype=np.uint8)
    y = (uint8_bytes / 255.0) * 2 - 1
    y = np.sign(y) * ((1 + MU) ** np.abs(y) - 1) / MU  # u-law F^-1
    return y


def make_output_file(input_file: Path) -> Path:
    ext = input_file.suffix
    return input_file.with_suffix(f".bent{ext}")


def save_data_ulaw(bend: np.ndarray, output_file: Path):
    """ map u-law floats to -1 to 1, map to uint8, write to file """
    x = np.clip(bend, -1, 1)
    x = np.sign(x) * (np.log1p(MU * np.abs(x)) / np.log1p(MU))  # u-law F
    uint8_bytes = np.round(np.clip((x + 1) / 2 * 255, 0, 255)).astype(np.uint8)
    with open(output_file, "wb") as f:
        f.write(uint8_bytes.tobytes())
