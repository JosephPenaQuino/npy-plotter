"""Plot npy files."""

import warnings
import argparse
from typing import List
import matplotlib.pyplot as plt
import numpy as np


warnings.filterwarnings("ignore")


def get_title(
    index: int,
    img: np.ndarray,
    num: int,
    limits: bool,
    stats: bool,
    offset: int,
    enable_index: bool = False
):
    """Generate the size and the title of the image."""
    title = ''
    if enable_index:
        title += f"idx: {index+offset}"
    size = 12
    if num > 5:
        size = 9
    if limits:
        title += (
            f"\nmin: {round(np.min(img), 3)},"
            f"max: {round(np.max(img), 3)}"
        )
    if stats:
        avg = np.average(img)
        med = np.median(img)
        title += (
            f"\navg: {round(avg, 3):0.3f}, med: {round(med, 3):0.3f},"
            f"\n shape: {img.shape}"
        )
    return size, title


def picshow(images: List[np.ndarray], **kwargs):
    """Plot the images in a grid.

    Kwargs options:
        - limits (bool: False): show min and max values
        - stats (bool: False): show average and median values
        - offset (bool: False): offset the index
        - image_names (List[str]: None): list of image names
        - enable_index (bool: False): enable index
        - sort (bool: False): sort the images
    """
    images_len = len(images)
    dims: tuple[int, int] = (
        int(np.ceil(np.sqrt(images_len))),
        int(np.rint(np.sqrt(images_len)))
    )

    fig = plt.figure(figsize=(10, 12))
    for i, img in enumerate(images):
        _, title = get_title(
            i,
            img,
            images_len,
            limits=kwargs.get('limits', False),
            stats=kwargs.get('stats', False),
            offset=kwargs.get('offset', False),
            enable_index=kwargs.get('enable_index', False),
            )
        image_names = kwargs.get('image_names', None)
        if image_names is not None:
            title += '\n' if title != '' else ''
            title += image_names[i]

        # Plot image with its title
        fig.add_subplot(dims[0], dims[1], i + 1)
        # sub.set_title(title, size=title_size)
        # sub.axis('off')
        if len(img.shape) == 3:
            img = img[:, :, 0]
        if np.amax(img) < 10 or np.amax(img) > 256:
            plt.imshow(img, cmap='jet', interpolation='nearest')
        else:
            plt.imshow(
                img,
                cmap='jet',
                interpolation='nearest',
                vmin=0,
                vmax=255
            )


def plot(image_paths: List[str], **kwargs):
    """Read and plot npy files in a grid.

    Kwargs options:
        - limits (bool: False): show min and max values
        - stats (bool: False): show average and median values
        - offset (bool: False): offset the index
        - image_names (List[str]: None): list of image names
        - enable_index (bool: False): enable index
        - sort (bool: False): sort the images
        - default_titles (bool: False): use default titles
    """
    images = []

    if kwargs.get('sort', False):
        image_paths.sort()

    # TODO: Perhaps add a check to see if the images are the same size
    # TODO: Perhaps there is a optimization to be made here
    for image_path in image_paths:
        images.append(np.load(image_path))

    image_names = kwargs.get('image_names', None)
    if kwargs.get('default_titles', False):
        image_names = [image_path.split('/')[-1] for image_path in image_paths]

    picshow(
        images,
        limits=kwargs.get('limits', False),
        stats=kwargs.get('stats', False),
        offset=kwargs.get('offset', False),
        titles=kwargs.get('image_names', None),
        enable_index=kwargs.get('enable_index', False),
        image_names=image_names,
    )
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('img_file_paths', nargs='+')
    parser.add_argument(
        '--no-index',
        dest='no_index',
        action='store_true',
        default=False
    )
    parser.add_argument('--limits', action='store_true', default=False)
    parser.add_argument('--stats', action='store_true', default=False)
    parser.add_argument('--sort', action='store_true', default=False)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--default-titles', action='store_true', default=False)
    args = parser.parse_args()
    plot(
        args.img_file_paths,
        limits=args.limits,
        stats=args.stats,
        offset=args.offset,
        enable_index=not args.no_index,
        default_titles=args.default_titles,
    )


if __name__ == "__main__":
    main()
