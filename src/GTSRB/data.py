import os
import shutil
from pathlib import Path

source_dir = "data/Train"
destination_dir = "adversarial_data"

os.makedirs(destination_dir, exist_ok=True)

for subdir in os.listdir(source_dir):
    subdir_path = os.path.join(source_dir, subdir)
    
    if os.path.isdir(subdir_path):
        dest_subdir_path = os.path.join(destination_dir, subdir)
        os.makedirs(dest_subdir_path, exist_ok=True)
        
        files = os.listdir(subdir_path)
        
        for file in files[:10]:
            src_file_path = os.path.join(subdir_path, file)
            dest_file_path = os.path.join(dest_subdir_path, file)
            shutil.copy(src_file_path, dest_file_path)

print(f"Test data created at: {destination_dir}")
