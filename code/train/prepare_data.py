import argparse

from PIL import ImageChops
from PIL import Image, ImageDraw
import json
import shutil

import zipfile
import os


# Function to create a mask from segmentation data
def create_mask(width, height, segmentation):
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    for segment in segmentation:
        draw.polygon(segment, outline=1, fill=1)
    return mask


def prepare_data(
        zip_path: str
):
    """Get our .zip (coco format) and create .tiff data in data/dataset/labels and data/dataset/converted_images"""
    extract_path = 'data/dataset'
    # Unzipping the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Path to the JSON file
    json_path = os.path.join(extract_path, 'result.json')

    # Reading the JSON file
    with open(json_path, 'r') as json_file:
        coco_data = json.load(json_file)

    # Path to save the label files
    labels_path = 'data/dataset/labels'
    os.makedirs(labels_path, exist_ok=True)

    # Creating masks for each image again
    for img_info in coco_data['images']:
        img_id = img_info['id']
        img_width = img_info['width']
        img_height = img_info['height']
        img_name = img_info['file_name'].replace('\\', '/').split('/')[-1].split('.')[0]

        # Creating an empty mask for the image
        mask = Image.new('L', (img_width, img_height), 0)

        # Adding masks for each annotation
        for ann in coco_data['annotations']:
            if ann['image_id'] == img_id:
                segmentation = ann['segmentation']
                ann_mask = create_mask(img_width, img_height, segmentation)
                mask = ImageChops.add(mask, ann_mask)

        # Saving the mask as a .tiff file
        mask.save(os.path.join(labels_path, f'{img_name}_label.tiff'))

    # Path to the images folder
    images_path = os.path.join(extract_path, 'images')

    # Path to save the converted images
    converted_images_path = 'data/dataset/converted_images'
    os.makedirs(converted_images_path, exist_ok=True)

    # Converting images to .tiff format
    for img_file in os.listdir(images_path):
        if img_file.lower().endswith(('.tif', '.tiff')):
            # If the image is already in .tiff format, just copy it to the new folder
            shutil.copy(os.path.join(images_path, img_file), os.path.join(converted_images_path, img_file))
        else:
            # If the image is not in .tiff format, convert and save it as .tiff
            img_path = os.path.join(images_path, img_file)
            img = Image.open(img_path)
            img_name = img_file.split('.')[0]
            img.save(os.path.join(converted_images_path, f'{img_name}.tiff'), 'TIFF')


def main():
    # Path to the uploaded file
    # zip_path = 'project-5-at-2023-12-26-23-30-2534b123.zip'
    parser = argparse.ArgumentParser(description="Run the script with a path to zip file.")
    parser.add_argument(
        "path_zip_file",
        type=str,
        help="path to zip file"
    )
    args = parser.parse_args()

    prepare_data(args.path_zip_file)


if __name__ == "__main__":
    main()
