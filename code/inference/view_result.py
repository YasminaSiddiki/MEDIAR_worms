import matplotlib.pyplot as plt
import os
from skimage import io

directory_path = '/content/out'

# Iterate through all filenames in the directory
for filename in os.listdir(directory_path):
    # Full path to the file
    full_path = os.path.join(directory_path, filename)
    # Define the paths for the images

    image_paths = [
        full_path.replace('_label', '').replace('out', 'in'),
        full_path
    ]

    # Load the images
    images = [io.imread(path) for path in image_paths]

    # Display the images in one figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(10, 8))

    for ax, img, path in zip(axes.flatten(), images, image_paths):
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(os.path.basename(path))

    plt.tight_layout()
    plt.show()
