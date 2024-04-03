from PIL import Image
import os
import numpy as np
import json
from tqdm import tqdm
from matplotlib import pyplot as plt


needles_images_dir = f"data/spacenet_coco_negAugs/val/images"
haystack_images_dir = f"data/spacenet_coco_negAugs/train/images"


with open(f"spacenet_coco_negAug_valAugInTrainAug.json", 'r') as f:
    leaks = json.load(f)


needles_images_vis = []
haystack_images_vis = []

# Initialize leaks table
leaks_table = {}
for l in leaks:
    if any(l['duplicates_in_haystack']):
        leaks_table[l['needle_image_name']] = []

# Populate leaks table
for l in tqdm(leaks):
    if any(l['duplicates_in_haystack']):
        needles_images_vis.append(l['needle_image_name'])
        haystack_images_vis.extend(l['duplicates_in_haystack'])
        leaks_table[l['needle_image_name']].extend(l['duplicates_in_haystack'])

needles_images_vis = set(needles_images_vis)
haystack_images_vis = set(haystack_images_vis)

for k in leaks_table.keys():
    leaks_table[k] = set(leaks_table[k])


for k, v in leaks_table.items():
    # f, axarr = plt.subplots(2,2)
    needle = Image.open(os.path.join(needles_images_dir, k))
    needle = np.asarray(needle)
    if np.sum(needle) > 5:
        plt.imshow(needle)
        plt.show()
    # axarr[0,0].imshow(image_datas[0])
    # axarr[0,1].imshow(image_datas[1])
    # axarr[1,0].imshow(image_datas[2])
    # axarr[1,1].imshow(image_datas[3])
    # print(k, len(v))
    # break