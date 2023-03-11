import os
from tqdm import tqdm

# Set the paths of the directories to compare
dir1 = 'data/crowdai_full/train/images'
dir2 = '/media/vcg1/data/Yeshwanth/Datasets/AICrowd_mapping_challenge_round_1_dataset/4186d95c-f949-4048-a963-c55d92644886_test_images (1)/test_images'

# Compare two files to see if they are identical
def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            chunk1 = f1.read(1024)
            chunk2 = f2.read(1024)
            if chunk1 != chunk2:
                return False
            if not chunk1:
                return True

counter =0

# Get a list of all files in both directories
files1 = [os.path.join(dir1, f) for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))]
files2 = [os.path.join(dir2, f) for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))]

# Get file sizes for files in directory 1
file_sizes1 = {}
for file in tqdm(files1):
    size = os.path.getsize(file)
    if size not in file_sizes1:
        file_sizes1[size] = []
    file_sizes1[size].append(file)

# Check file sizes for files in directory 2
for file in files2:
    size = os.path.getsize(file)
    if size in file_sizes1:
        for f in file_sizes1[size]:
            if compare_files(file, f):
                print(f"{file} is the same size as {f}")
                counter += 1

print(counter)