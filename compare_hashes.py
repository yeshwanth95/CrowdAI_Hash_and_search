import json
import os
import imagehash
import argparse
from tqdm import tqdm
import multiprocessing


parser = argparse.ArgumentParser(
    prog="Compare hashes",
    description="Compare two hash databases and store duplicates."
)
parser.add_argument('needles_hashfile')
parser.add_argument('haystack_hashfile')
parser.add_argument('--output_filename', required=True)
args = parser.parse_args()


haystack_hashes_path = args.haystack_hashfile
needles_hashes_path = args.needles_hashfile

with open(haystack_hashes_path) as f:
    haystack_hashes = json.loads(f.read())
with open(needles_hashes_path) as f:
    needles_hashes = json.loads(f.read())


def duplicates_per_image(im_name, im_hash, duplicate_images: list):
    _result = {}
    _result["val_image_name"] = im_name
    _result["val_image_hash"] = im_hash
    _result["duplicates_in_train"] = duplicate_images

    return _result


def compare_single_needle_in_haystack(needle):
        duplicates = []
        v_name = needle['image_name']
        v_hash = imagehash.hex_to_hash(needle['hash'])
        for sample in haystack_hashes:
            t_name = sample['image_name']
            t_hash = imagehash.hex_to_hash(sample['hash'])
            if t_hash == v_hash:
                duplicates.append(sample)

        return [v_name, str(v_hash), duplicates]


def main(args):

    duplicates_results = []
    counter = 0
    with multiprocessing.Pool() as pool:
        for result in tqdm(pool.imap(compare_single_needle_in_haystack, needles_hashes), total=len(needles_hashes)):
            duplicates_results.append(duplicates_per_image(result[0], result[1], result[2]))
            # if len(duplicates_results) > 10:
            #     with open(os.path.join(args.output_filename), "w") as f:
            #         f.write(json.dumps(duplicates_results))
            #     break
    # for image in tqdm(needles_hashes):
    #     v_name = image['image_name']
    #     v_hash = image['hash']
    #     v_hash = imagehash.hex_to_hash(v_hash)
    #     duplicates = []
    #     for sample in haystack_hashes:
    #         t_name = sample['image_name']
    #         t_hash = sample['hash']
    #         t_hash = imagehash.hex_to_hash(t_hash)
    #         if t_hash == v_hash:
    #             duplicates.append(sample)
    #     duplicates_results.append(duplicates_per_image(v_name, str(v_hash), duplicates))

    for n in duplicates_results:
        if len(n['duplicates_in_train']) > 0:
            counter += 1
    print(f"{counter} images of {len(needles_hashes)} images in needles haves duplicates in haystack.")

    with open(os.path.join(args.output_filename), "w") as f:
            f.write(json.dumps(duplicates_results))


if __name__ == "__main__":
    main(args)
