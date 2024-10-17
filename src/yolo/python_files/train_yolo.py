import yolov5
from yolov5 import train
import os
import torch
import yaml
from sklearn.model_selection import train_test_split

def make_yaml():
    class_names = ['prohibitory', 'danger', 'mandatory', 'other']

    data_dir = os.path.abspath('../data/ts/ts')
    train_image_list = os.path.abspath('../data/train_images.txt')
    val_image_list = os.path.abspath('../data/val_images.txt')
    yaml_file = os.path.abspath('../data/dataset.yaml')

    image_files = [f for f in os.listdir(data_dir) if f.endswith('.jpg')]

    train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

    with open(train_image_list, 'w') as f:
        for item in train_files:
            f.write("%s\n" % os.path.join(data_dir, item))

    with open(val_image_list, 'w') as f:
        for item in val_files:
            f.write("%s\n" % os.path.join(data_dir, item))

    data = {
        'train': train_image_list,
        'val': val_image_list,
        'nc': len(class_names),
        'names': {i: name for i, name in enumerate(class_names)}
    }

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

if __name__ == "__main__":

    make_yaml()

    train.run(
        img=416,
        batch=8,
        epochs=50,
        data="../data/dataset.yaml",
        weights='yolov5m.pt',
        device='0',
        workers=1
    )
