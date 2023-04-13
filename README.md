# Efficient Deduplication and Leakage Detection in Large Scale Image Datasets with a focus on the CrowdAI Mapping Challenge Dataset

### Yeshwanth Kumar Adimoolam, Bodhiswatta Chatterjee, Charalambos Poullis and Melinos Averkiou


Official repository of the paper: [Efficient Deduplication and Leakage Detection in Large Scale Image Datasets with a focus on the CrowdAI Mapping Challenge Dataset](https://arxiv.org/abs/2304.02296v1).


## Updates

April 13, 2023 - We release a data inspection web interface to manually inspect the extend of data leakage and duplication in the CrowdAI Mapping Challenge dataset. The web interface can be found at [datainspector.app](https://datainspector.app/)


## Highlights
- We propose an easy-to-adopt de-duplication and leakage detection pipeline for large-scale image datasets that utilizes collision detection of perceptual hashes of images.
- We employ the proposed de-duplication pipeline to identify and eliminate instances of data duplication and leakage in the CrowdAI mapping challenge dataset. Approximately 250k of the 280k training images were either exact or augmented duplicates.
- We demonstrate cases of significant overfitting of the recent state-of-the-art methods, potentially invalidating a number of prior art reporting on this dataset for the task of building footprint extraction.

## Installation

```
conda create -n hash_and_search python=3.10
conda activate hash_and_search
pip install -r requirements.txt
```
Alternatively, the following requirements can be installed manually:
```
ImageHash
numpy
Pillow
PyWavelets
scipy
tqdm
```

## Compute Hashes
To compute p-hashes for images in a folder, run:

```
python compute_hashes.py <input_images_directory> <output_directory> <output_hashtable_filename>
```

To compute p-hashes of augmented images in the dataset, run:
```
python compute_hashes_augmented.py <input_images_directory> <output_directory> <output_hashtable_filename>
```

## Compare Hashes
Once hashtables are constructed for two image datasets, it is possible to compare the hashtables to detect duplicates using the following command:
```
python compare_hashes.py <needles_hashtable> <haystack_hashtable> <output_filename>
```
The above command results in a `.json` file containing all instances of duplicates in the haystack set for each image in the needles set.

## Visualise Duplicates
To inspect and visualise these duplicates between the needles and haystack sets, run:

```
python inspect_hashes.py
python json_to_html.py
```
These commands would generate a HTML file that can be opened in any standard web browser. To view the HTML file:

1. Download the CrowdAI dataset train split images from [here](https://www.aicrowd.com/challenges/mapping-challenge/dataset_files).
2. Place the train images in the same folder as the HTML file in the following directory structure: `./data/train/images/<place_images_here>`.
    ```
    └───data
        └───train
            └───images
                └───<place_images_here.>
    ```

3. Open the HTML file in a standard web browser (e.g., Google Chrome).

## Dataset

Download link coming soon...
<!-- Download the deduplicated and corrected subset of the CrowdAI dataset [here](). -->

<!-- ## Citation
If you find our work useful in your research, please consider citing:
```

``` -->

## Acknowledgement
This repository benefits from
- [ImageHash](https://github.com/JohannesBuchner/imagehash)
- [https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html](https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)
<!-- - [hawp](https://github.com/cherubicXN/hawp) -->
<!-- - [hawp](https://github.com/cherubicXN/hawp) -->
<!-- - [hawp](https://github.com/cherubicXN/hawp) -->
<!-- - [hawp](https://github.com/cherubicXN/hawp) -->