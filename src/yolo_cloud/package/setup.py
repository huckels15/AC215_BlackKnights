from setuptools import find_packages
from setuptools import setup


REQUIRED_PACKAGES = [
    "wandb==0.15.11",
    "yolov5",   
    "torch", 
    "torchvision", 
    "torchaudio",
    "huggingface_hub==0.24.7",
    "requests",
    "ultralytics",
    "ipython",
]

setup(
    name="yolo-trainer",
    version="0.0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="YOLO Trainer",
)