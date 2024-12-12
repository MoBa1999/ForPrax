import Levenshtein
from torch.utils.data import DataLoader, TensorDataset
import sys
sys.path.append("/workspaces/ForPrax/Func")
sys.path.append("/workspaces/ForPrax/Models")
from data_prep_func import get_data_loader
from data_prep_func import get_device
from data_prep_func import vectors_to_sequence
from eval_utils import evaluate_model_ham
from eval_utils import plot_training_curves_separate
import os
import torch
from torch import nn
import matplotlib.pyplot as plt
from CTC_Test import CTC_Test_Model
import seaborn as sns
import random
import numpy as np

def generate_random_sequence(length, bias):
        def biased_choice(last_base):
            weights = [0.25, 0.25, 0.25, 0.25]
            if last_base is not None:
                weights['ATGC'.index(last_base)] *= bias
                weights = [w / sum(weights) for w in weights]  # Normalize weights
            return random.choices('ATGC', weights=weights)[0]

        sequence = ""
        for _ in range(length):
            sequence += biased_choice(sequence[-1] if sequence else None)
        return sequence

def hamming_distance(s1, s2):
    """
    Berechnet die Hamming-Distanz zwischen zwei Strings.
    Voraussetzung: Beide Strings müssen die gleiche Länge haben.
    """
    if len(s1) != len(s2):
        raise ValueError("Hamming distance requires strings of equal length")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def compare_distances(string1, string2):
    """
    Vergleicht die Levenshtein-Distanz und die Hamming-Distanz
    zwischen zwei Strings.
    """
    # Berechne die Levenshtein-Distanz
    lev_distance = Levenshtein.distance(string1, string2)

    # Berechne die Hamming-Distanz (falls möglich)
    try:
        ham_distance = hamming_distance(string1, string2)
    except ValueError as e:
        ham_distance = str(e)

    return ham_distance, lev_distance

def check_random_sequences(count):
    ham_ = []
    lev_ = []
    for _ in range(count):
        string1 = generate_random_sequence(200, 0.75)
        string2 = generate_random_sequence(200, 0.75)
    
        ham, lev = compare_distances(string1, string2)
    
        ham_.append(ham)
        lev_.append(lev)
    return ham_,lev_




############



#test_path = "/media/hdd1/MoritzBa/Test_Data/Rd_Data_Numpy"
test_path = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"

model_path_general = "/media/hdd1/MoritzBa/Models/Data_80000_s_75_ep_1_r.pth"



test_lev_accuracies = {}

device = get_device(gpu_index=0)
max_length = 2100
_, test_loader = get_data_loader(
                test_path, 
                end_sequence=100000, 
                start_sequence=95000, 
                batch_size=16, 
                num_reads=1, 
                overwrite_max_length=max_length, 
                dim_squeeze=True
            )

model = CTC_Test_Model(input_length=max_length, tar_length=200, conv_1_dim=16,conv_2_dim=32, attention_dim=16, num_reads=1,
                 n_heads = 16, at_layer = 2)


model.load_state_dict(torch.load(model_path_general))

model.eval()
model.to(device)

lengths = evaluate_model_ham(model, test_loader,device,lengths=True)

print(lengths)
plt.figure(figsize=(10, 6))
plt.hist(lengths, bins='auto', edgecolor='black')
plt.title('Histogram of Lengths')
plt.xlabel('Length')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

hams, levs = check_random_sequences(5000)

plt.figure(figsize=(12, 6))

# Plot histograms
plt.hist(hams, bins='auto', alpha=0.7, label='Hamming Distance', edgecolor='black')
plt.hist(levs, bins='auto', alpha=0.7, label='Levenshtein Distance', edgecolor='black')

plt.title('Histogram of Hamming and Levenshtein Distances')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Add mean lines
mean_ham = np.mean(hams)
mean_lev = np.mean(levs)
plt.axvline(mean_ham, color='blue', linestyle='dashed', linewidth=2, label=f'Mean Hamming: {mean_ham:.2f}')
plt.axvline(mean_lev, color='red', linestyle='dashed', linewidth=2, label=f'Mean Levenshtein: {mean_lev:.2f}')

plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Plot histogram for Levenshtein distance
plt.hist(levs, bins='auto', alpha=0.7, label='Levenshtein Distance', edgecolor='black')

plt.xlabel('Levenshtein-Distance', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.legend(fontsize=16)
plt.grid(True, alpha=0.3)

# Increase tick label font size
plt.tick_params(axis='both', which='major', labelsize=16)

# Add mean line
mean_lev = np.mean(levs)
plt.axvline(mean_lev, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_lev:.2f}')

plt.legend(fontsize=16)
plt.tight_layout()
plt.show()






    
