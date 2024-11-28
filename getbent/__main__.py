from pathlib import Path

import numpy as np

from getbent.effects import process_effect
from getbent.io import load_data, make_output_file, save_data


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=Path)
parser.add_argument("effects", type=str, nargs="*")
parser.add_argument("--output_file", type=Path, default=None)
args = parser.parse_args()


bend = load_data(args.input_file)


# apply effects to central 90% of file
print(f"{bend.shape=}")
start = bend.shape[0] // 10
end = bend.shape[0] - start
for effect in args.effects:
    bend[start:end] = process_effect(bend[start:end], effect)

if not args.output_file:
    args.output_file = make_output_file(args.input_file)
save_data(bend, args.output_file)