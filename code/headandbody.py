# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 19:59:19 2024

@author: yasya
"""

import os
import numpy as np
import tifffile as tiff
from skimage import io
from skimage.color import label2rgb

def load_tiff_images(directory):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith(".tiff") or filename.endswith(".tif"):
            path = os.path.join(directory, filename)
            images[filename] = tiff.imread(path)
    return images

def combine_masks(mask1, mask2, color1=[255, 0, 0], color2=[0, 255, 0]):
    combined = np.zeros((mask1.shape[0], mask1.shape[1], 3), dtype=np.uint8)
    
    combined[mask1 > 0] = color1
    combined[mask2 > 0] = color2
    
    overlap = (mask1 > 0) & (mask2 > 0)
    combined[overlap] = [255, 255, 0]  # Different color for overlapping areas
    
    return combined

def save_combined_images(output_dir, combined_images):
    os.makedirs(output_dir, exist_ok=True)
    for filename, image in combined_images.items():
        tiff.imwrite(os.path.join(output_dir, filename), image)

def main(dir1, dir2, output_dir):
    masks1 = load_tiff_images(dir1)
    masks2 = load_tiff_images(dir2)
    
    combined_images = {}
    for filename in masks1:
        if filename in masks2:
            mask1 = masks1[filename]
            mask2 = masks2[filename]
            combined_images[filename] = combine_masks(mask1, mask2)
    
    save_combined_images(output_dir, combined_images)
    print(f"Combined images saved to {output_dir}")

if __name__ == "__main__":
    dir1 = "path/to/dir1"
    dir2 = "path/to/dir2"
    output_dir = "path/to/output_dir"
    
    main(dir1, dir2, output_dir)
