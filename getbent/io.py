from pathlib import Path

import numpy as np


dtype = np.dtype(np.float32)


def load_data(input_file: Path) -> np.ndarray:
    with open(input_file, "rb") as f:
        input_bytes = f.read()
    # append zeros to make it fit dtype
    input_bytes += b"\x00" * (dtype.itemsize - len(input_bytes) % dtype.itemsize)
    return np.fromstring(string=input_bytes, dtype=dtype)


def make_output_file(input_file: Path) -> Path:
    ext = input_file.suffix
    return input_file.with_suffix(f".bent{ext}")


def save_data(bend: np.ndarray, output_file: Path):
    with open(output_file, "wb") as f:
        f.write(bend.tobytes())
