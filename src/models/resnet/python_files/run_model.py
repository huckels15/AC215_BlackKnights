from load_data import load_dataset
from model_development import model_creation
from train_model import train
from test_model import test
from train_script import train_epochs
from visualize_model import plot_accuracy, plot_loss
import torch.optim as optim
import torch



def run_model(train_model = True):
    train_data, train_loader, test_data, test_loader, classes = load_dataset()

    # Number of classes
    num_classes = len(classes)

    # Create model
    model, criterion, optimizer, device = model_creation(train_data)

    model = model.to(device)

    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

    if train_model:
        # Train the model for 50 epochs, saving every 5 epochs
        num_epochs = 50
        save_interval = 5
        model, train_losses, train_accuracies, test_losses, test_accuracies = train_epochs(
            model, train_loader, test_loader, criterion, optimizer, device,
            num_epochs, save_interval)

        # Save the final trained model
        torch.save(model.state_dict(), f'output/resnet50_HAM10000_final_model_epochs_{num_epochs}.pth')

        # Plot and save the loss and accuracy plots
        plot_loss(train_losses, test_losses)
        plot_accuracy(train_accuracies, test_accuracies)
    else:
        # Load the pre-trained model
        model.load_state_dict(torch.load('output/resnet50_HAM10000_final_model_epochs_50.pth'))
        # Load the variables
        checkpoint = torch.load("output/resnet50_HAM10000_variables.pth")
        epoch = checkpoint['epoch']
        train_losses = checkpoint['train_losses']
        train_accuracies = checkpoint['train_accuracies']
        test_losses = checkpoint['test_losses']
        test_accuracies = checkpoint['test_accuracies']
        classes = checkpoint['classes']
        model.to(device)
        model.eval()

run_model()
