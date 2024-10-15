import torch
import torchvision
from torchvision import transforms

def load_dataset():
    # Set dataset path
    # Define the transformation
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Load the data
    train_data = torchvision.datasets.ImageFolder(root="data/train/", transform=transform)
    test_data = torchvision.datasets.ImageFolder(root="data/test/", transform=transform)

    # Define the dataloaders
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True, num_workers=4)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=32, shuffle=False, num_workers=4)

    # Class names for HAM10000 dataset
    classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

    return train_data, train_loader, test_data, test_loader, classes