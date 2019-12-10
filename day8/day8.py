import numpy as np
from matplotlib import pyplot as plt

def get_input(input_path):
    with open(input_path) as f:
        line = f.readline().strip('\n')
    return line

def count_zeros(image):
    """Count the number of zeros in an image string."""
    return image.count('0')


def read_image(digits, image_len):
    """Split the image string into images, return num 1's * num 2's for the
       image with the fewest zeros.
    """
    images = [digits[i:i+image_len] for i in range(0, len(digits), image_len)]
    zero_counts = list(map(count_zeros, images))
    min_zeros_ix = zero_counts.index(min(zero_counts))
    out_image = images[min_zeros_ix]
    return out_image.count('1') * out_image.count('2')


def find(x, c):
    """A custom str find function that returns infinity if not found"""
    try:
        return x.index(c)
    except ValueError:
        return np.inf


def decode_image(digits, image_len):
    """Decodes an image by finding the first non 2-valued pixel in the image"""

    # Gets an array of all pixel values in the "z" dimension
    pixel_strs = [digits[i::image_len] for i in range(image_len)]

    # Figure out if a 0 or 1 comes first
    f = lambda x: '0' if find(x, '0') < find(x, '1') else '1'

    return [f(s) for s in pixel_strs]


def main():
    digits = get_input('input.txt')
    image_len = 25 * 6
    
    # PART 1
    part_1 = read_image(digits, image_len)
    print('Answer to part 1: {}'.format(part_1))

    # PART 2
    decoded = decode_image(digits, image_len)
    pixel_grid = np.array(decoded, dtype=int).reshape(6, 25)
    plt.imshow(pixel_grid)
    plt.show()

main()
