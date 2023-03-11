#!/bin/bash

python hash_and_compare.py data/crowdai_full/train/images train_hashes --output_filename train_hashes.json
python hash_and_compare.py data/crowdai_full/val/images val_hashes --output_filename val_hashes.json
