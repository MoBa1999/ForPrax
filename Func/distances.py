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

    # Ergebnisse ausgeben
    print(f"String 1: {string1}")
    print(f"String 2: {string2}")
    print(f"Levenshtein Distance: {lev_distance}")
    print(f"Hamming Distance: {ham_distance}")


print("Vergleich von Levenshtein- und Hamming-Distanz")
string1 = input("Bitte den ersten String eingeben: ")
string2 = input("Bitte den zweiten String eingeben: ")

compare_distances(string1, string2)




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
                start_sequence=80000, 
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


# Example usage






    

# Create the plot
sns.set_palette("muted")
plt.figure(figsize=(10, 6))

for r in nr:
    plt.scatter(test_lev_accuracies[r]["sequences"], test_lev_accuracies[r]["test_accs"], label = f" Number of Input-Reads: {r}", marker ='o', s=90)

        

plt.xlabel('Training Sequences', fontsize=20)
plt.ylabel('Test Levenshtein Accuracy', fontsize=20)
plt.tick_params(axis='both', labelsize=16)
plt.xlim(0,90000)
plt.ylim(45,75)
plt.legend(fontsize =16)
plt.tight_layout()
plt.grid(True)
plt.show()