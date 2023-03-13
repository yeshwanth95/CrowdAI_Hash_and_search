import json
import os
from copy import copy
from tqdm import tqdm


def main(json_fn):
    # json_fn = "train_noLeak_hashes.json"
    with open(json_fn, 'r') as f_in:
        json_data = json.load(f_in)

    # Create img_to_hash_dict, where each img will be a unique key that will contain its 6 hashes.
    # Create hash_to_dict, where each hash will be a unique key that will contain all the images that correspond to
    # this hash. The set() type is used here to remove image names that are found more than once)
    img_to_hash_dict, hash_to_img_dict = {}, {}
    for val in tqdm(json_data):
        if val["image_name"] not in img_to_hash_dict.keys():
            img_to_hash_dict.update({val["image_name"]: []})
        if val["hash"] not in hash_to_img_dict.keys():
            hash_to_img_dict.update({val["hash"]: set()})
        img_to_hash_dict[val["image_name"]].append(val["hash"])
        hash_to_img_dict[val["hash"]].add(val["image_name"])

    # Create uniq_img_to_dup_img_dict, where each unique img (according to hash) its mapped to all its duplicates
    uniq_img_to_dup_img_dict, img_found = {}, dict(zip(img_to_hash_dict.keys(), [False for _ in img_to_hash_dict]))
    for query_img in tqdm(img_to_hash_dict.keys()):
        if img_found[query_img]:
            # Image has been already visited, as it was duplicate of a unique image
            continue

        # Unique image found
        uniq_img_to_dup_img_dict[query_img] = set()
        img_found[query_img] = True

        # Iterate over the hashes of the unique image, in order to find all of its duplicates
        for hash in img_to_hash_dict[query_img]:
            hash_img_list = copy(hash_to_img_dict[hash])
            # Remove unique image from the list
            hash_img_list.remove(query_img)
            # Update set() with the new duplicate images
            uniq_img_to_dup_img_dict[query_img].update(hash_img_list)
            for dup_img in hash_img_list:
                # Mark all the duplicate images as visited
                img_found[dup_img] = True

    # Sanity check; verify that each unique image is not present in the duplicate list of another unique image
    for img in tqdm(uniq_img_to_dup_img_dict):
        for img_, img_list in uniq_img_to_dup_img_dict.items():
            try:
                assert img not in img_list
            except AssertionError:
                print(f"{img=}: {img_=},{img_list=}")
                continue

    # Dump to JSON
    uniq_img_to_dup_img_json = {}
    for k, v in uniq_img_to_dup_img_dict.items():
        uniq_img_to_dup_img_json[k] = list(v)
    with open("uniq_to_dup_imgs.json", 'w') as f_out:
        json.dump(uniq_img_to_dup_img_json, f_out, indent=2)

    # Print stats
    dup_imgs = set()
    for dup_img in uniq_img_to_dup_img_dict.values():
        dup_imgs.update(dup_img)
    n_total_imgs = len(img_to_hash_dict)
    n_unique_imgs = len(uniq_img_to_dup_img_dict.keys())
    n_dup_imgs = len(dup_imgs)
    assert n_total_imgs == n_unique_imgs + n_dup_imgs
    print(f"Total images: {n_total_imgs}")
    print(f"Unique images: {n_unique_imgs}")
    print(f"Duplicate images: {n_dup_imgs}")


if __name__ == '__main__':
    main(json_fn=f"crowdai_noLeak/train_hashes/train_noLeak_hashes.json")
