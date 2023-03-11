import os
import argparse
from PIL import Image
import imagehash
import json
from tqdm import tqdm


parser = argparse.ArgumentParser(
    prog="Compute and store image hashes.",
    description="Compute and store image hashes for all images in a directory."
)
parser.add_argument('images_dir')
parser.add_argument('output_dir')
parser.add_argument('--output_filename', default="hashes.json", required=False)
args = parser.parse_args()


def main(args):

    print(f"Computing hashes for images in {args.images_dir}")

    image_paths = os.listdir(args.images_dir)

    def single_hash_entry(img_name, img_hash_string):
        hash_dict = {}
        hash_dict["image_name"] = img_name
        hash_dict["hash"] = img_hash_string
        return hash_dict


    image_hashes = []
    for im in tqdm(image_paths):
        img = Image.open(os.path.join(args.images_dir, im))
        im_hash = imagehash.phash(img)
        image_hashes.append(single_hash_entry(im, str(im_hash)))

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    with open(os.path.join(args.output_dir, args.output_filename), "w") as f:
        f.write(json.dumps(image_hashes))

    print(f"Finished computing hashes for {len(image_paths)} images in directory: {args.images_dir}.")


if __name__ == "__main__":
    main(args)
