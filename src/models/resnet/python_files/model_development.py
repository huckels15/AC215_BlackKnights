import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models import resnet50

def model_creation(train_data):
    # Define the model
    model = resnet50(weights='ResNet50_Weights.DEFAULT')

    # Replace the last layer
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(train_data.classes))

    # Define the loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

    # Move the model to the device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    return model, criterion, optimizer, device
