import code
import json
import os
import imagehash
import argparse
from tqdm import tqdm
import multiprocessing
import numpy as np


parser = argparse.ArgumentParser(
    prog="Compare hashes",
    description="Compare two hash databases and store duplicates."
)
parser.add_argument('needles_hashfile')
parser.add_argument('haystack_hashfile')
parser.add_argument('--output_filename', required=True)
args = parser.parse_args()


def duplicates_per_image(im_name, im_hash, duplicate_images: list):
    _result = {}
    _result["train_image_name"] = im_name
    _result["train_image_hash"] = im_hash
    _result["duplicates_in_train"] = duplicate_images

    return _result


def main(args):
    haystack_hashes_path = args.haystack_hashfile
    needles_hashes_path = args.needles_hashfile

    with open(haystack_hashes_path) as f:
        haystack_hashes = json.loads(f.read())
    with open(needles_hashes_path) as f:
        needles_hashes = json.loads(f.read())
    haystack_names_array, haystack_hash_array = [], []
    for i in range(len(haystack_hashes)):
        haystack_names_array.append(haystack_hashes[i]["image_name"])
        haystack_hash_array.append(haystack_hashes[i]["hash"])

    haystack_names_array = np.array(haystack_names_array)
    haystack_hash_array = np.array(haystack_hash_array)

    counter = 0
    duplicates_results = []
    for needle in tqdm(needles_hashes):
        v_name = needle['image_name']
        v_hash = np.array(needle['hash'])

        duplicates = haystack_names_array[haystack_hash_array == v_hash].tolist()
        if len(duplicates) > 0:
            counter += 1
        duplicates_results.append(duplicates_per_image(v_name, str(v_hash), duplicates))
        # code.interact(local=locals())

    print(f"{counter} images of {len(needles_hashes)} images in needles haves duplicates in haystack.")

    with open(os.path.join(args.output_filename), "w") as f:
            f.write(json.dumps(duplicates_results))


if __name__ == "__main__":
    main(args)
