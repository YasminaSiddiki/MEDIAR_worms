import argparse
import os
from PIL import Image


def convert_pngs_to_tiff(input_dir: str, output_dir: str):
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        print(os.listdir(input_dir))
        # Iterate through all files in the input directory
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)

            # Check if the file is a PNG image
            if os.path.isfile(input_path) and filename.lower().endswith('.png'):
                # Construct the output path with the same filename but TIFF extension
                output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.tiff')

                # Open the PNG image and save it as a TIFF file
                with Image.open(input_path) as img:
                    img.save(output_path, 'TIFF')
                print(f"Conversion successful. TIFF image saved at {output_path}")
            else:
                print("g")

    except Exception as e:
        print(f"Error: {e}")


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Convert PNG images in a directory to TIFF format.")

    # Adding the arguments
    parser.add_argument('--input_dir', type=str, required=True,
                        help='Directory path containing PNG images.')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Directory path where converted TIFF images will be saved.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the convert_pngs_to_tiff function with the parsed arguments
    convert_pngs_to_tiff(input_dir=args.input_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
