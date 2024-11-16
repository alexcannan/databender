import numpy as np
from PIL import Image
import argparse
import matplotlib.pyplot as plt


def apply_delay_effect(data, delay_samples, decay_factor=0.5):
    """Applies a simple delay effect to each color channel in the image data."""
    flattened_data = data.flatten()
    output = np.copy(flattened_data)

    delay_offset = delay_samples * 3

    output[delay_offset:] = np.clip(
        output[delay_offset:] + decay_factor * flattened_data[:-delay_offset],
        0, 255
    ).astype(np.uint8)

    return output.reshape(data.shape)


def load_compressed_image_as_raw_data(file_path):
    """Load a compressed image and convert it to a bitmap-like numpy array."""
    img = Image.open(file_path)
    img = img.convert("RGB")
    data = np.array(img)
    return data, img.size


def save_raw_data_as_image(data, file_path):
    """Save the modified data as a new image."""
    img = Image.fromarray(data)
    img.save(file_path)


def display_image(data):
    """Display the modified image using matplotlib."""
    plt.imshow(data)
    plt.axis("off")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Databend an image using a delay effect.")
    parser.add_argument("image_path", type=str, help="Path to the input image.")
    parser.add_argument("--output_path", type=str, help="Path to save the modified image.")
    parser.add_argument("--delay_samples", type=int, default=100, help="Number of samples to delay.")
    parser.add_argument("--decay_factor", type=float, default=0.5, help="Decay factor for the delay effect.")

    args = parser.parse_args()

    raw_data, img_size = load_compressed_image_as_raw_data(args.image_path)
    modified_data = apply_delay_effect(raw_data, args.delay_samples, args.decay_factor)

    if args.output_path:
        save_raw_data_as_image(modified_data, args.output_path)
        print(f"Modified image saved to {args.output_path}")
    else:
        display_image(modified_data)


if __name__ == "__main__":
    main()
