from pathlib import Path

import numpy as np

from getbent.effects import process_effect
from getbent.io import load_data_ulaw, make_output_file, save_data_ulaw


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=Path)
parser.add_argument("effects", type=str, nargs="*")
parser.add_argument("--output_file", type=Path, default=None)
args = parser.parse_args()


bend = load_data_ulaw(args.input_file)

# prepare central 90% of file
start = bend.shape[0] // 20
end = bend.shape[0] - start

# shift bounds randomly
p005 = bend.shape[0] // 200
shift = np.random.randint(-p005, p005)
start += shift
end += shift

for effect in args.effects:
    bend[start:end] = process_effect(bend[start:end], effect)

if not args.output_file:
    args.output_file = make_output_file(args.input_file)
save_data_ulaw(bend, args.output_file)