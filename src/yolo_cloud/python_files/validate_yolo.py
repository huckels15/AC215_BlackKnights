import yolov5
from yolov5 import val
import os
import torch
import yaml

if __name__ == "__main__":
    val.run(
        weights='runs/train/exp/weights/best.pt', 
        data='../data/dataset.yaml',
        img=640
    )