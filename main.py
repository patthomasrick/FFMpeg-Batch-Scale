import argparse
import imghdr
import os
from tqdm import tqdm

WIDTH_4K = 3840
HEIGHT_4K = 3840


def find_all_images(directory):
    """Return a list of all images in the directory recursively."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            # Use MIME type.
            if imghdr.what(
                os.path.join(root, filename)
            ) and not filename.endswith((".heic", ".HEIC")):
                files.append(os.path.join(root, filename))
    files.sort()
    return files


if __name__ == "__main__":
    # Process args with Argparse.
    # Args - directory to recursively search for files.
    parser = argparse.ArgumentParser(
        description="Search for files in a directory."
    )
    parser.add_argument("directory", help="Directory to search for files.")
    args = parser.parse_args()
    directory = args.directory

    files = find_all_images(directory)

    # Example ffmpeg command: ffmpeg -i input.jpg -vf "scale='min(320,iw)':'min(240,ih)'" input_not_upscaled.png
    # Put all output in ./output
    try:
        os.mkdir("output")
    except FileExistsError:
        pass

    for file in tqdm(files):
        os.system(
            f"ffmpeg -hide_banner -loglevel error -y -i '{file}' -vf \"scale='min({WIDTH_4K},iw)':-1\" 'output/{os.path.basename(file)}'"
        )
