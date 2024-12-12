import sys
sys.path.append("/workspaces/ForPrax/Func")
sys.path.append("/workspaces/ForPrax/Models")
from CTC_Test import CTC_Test_Model
from CTC_2D import CTC_2D_Model
import numpy as np
import matplotlib.pyplot as plt
import os
import torch 
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from data_prep_func import get_data_loader
from data_prep_func import get_device
from data_prep_func import vectors_to_sequence
from eval_utils import evaluate_model_ham
from eval_utils import plot_training_curves_separate

# Train Parameters
kernel_1 = 29
kernel_2 = 9
batch_size = 16
learning_rate = 0.001
n_heads = 16
at_dim = 16
at_layer = 2
dim_squeeze = True
train_seqs = 80000
test_seqs = 5000
num_epochs = 10

# List of num_reads values to iterate over
num_reads_list = [1, 2, 5,10]

device = get_device(gpu_index=2)
data_path = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"

for num_reads in num_reads_list:
    print(f"\nStarting training for num_reads={num_reads}\n")

    plot_dir = f"/media/hdd1/MoritzBa/Plots/2D_Data_{train_seqs}_s_{num_epochs}_ep_{num_reads}_r.png"
    output_dir_model = f"/workspaces/ForPrax/Model_Save/2D_Data_{train_seqs}_s_{num_epochs}_ep_{num_reads}_r.pth"

    print(f"""
    Training Process Details of Multi CTC 2D Training:
    -------------------------
    Batch Size: {batch_size}
    Heads : {n_heads}
    At Dim : {at_dim}
    Attention Layers : {at_layer}
    kernel_1 : {kernel_1}
    kernel_2 : {kernel_2}
    Number of Reads: {num_reads}
    Number of Epochs: {num_epochs}
    Start Learning Rate: {learning_rate}
    Dimensional Squeeze: {dim_squeeze}
    Training Sequences: {train_seqs}
    Testing Sequences: {test_seqs}
    """)

    # Prepare data loaders
    max_length = 2100
    max_length, train_loader = get_data_loader(data_path, train_seqs, batch_size=batch_size, num_reads=num_reads, dim_squeeze=True, overwrite_max_length=max_length)
    max_2, test_loader = get_data_loader(data_path, end_sequence=train_seqs+test_seqs, start_sequence=train_seqs, batch_size=batch_size, num_reads=num_reads, dim_squeeze=True, overwrite_max_length=max_length)

    # Create Model and Train
    model = CTC_2D_Model(
        input_length=max_length, tar_length=200, conv_1_dim=32, conv_2_dim=32, 
        attention_dim=at_dim, num_reads=num_reads, n_heads=n_heads, 
        at_layer=at_layer, kernel_2=kernel_2, kernel_1=kernel_1
    )

    losses, n_accuracies, ham_accuracies, test_accs = model.train_model(
        train_loader, num_epochs=num_epochs, learning_rate=learning_rate,
        device=device, test_set=test_loader, save_path=output_dir_model, scheduler_type="cosine_restart"
    )

    # Evaluate training data accuracy
    train_ham_ac = evaluate_model_ham(model, train_loader, device)
    print(f" Training Lev-Accuracy for num_reads={num_reads}: {train_ham_ac:.2f}%")

    # Evaluate model on test data
    test_ham_ac = evaluate_model_ham(model, test_loader, device)
    print(f"Test Lev-Accuracy for num_reads={num_reads}: {test_ham_ac:.2f}%")

    # Plot training curves
    plot_training_curves_separate(losses, n_accuracies, ham_accuracies, test_accs, plot_dir)
