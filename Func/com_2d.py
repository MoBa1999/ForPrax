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
from CTC_2D import CTC_2D_Model
import seaborn as sns
import numpy as np

#test_path = "/media/hdd1/MoritzBa/Test_Data/Rd_Data_Numpy"
test_path = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"

model_path_general = "/media/hdd1/MoritzBa/Models"
model_path_2D = "/workspaces/ForPrax/Model_Save"
model_path_2d = "/workspaces/ForPrax/Model_Save"


test_lev_accuracies = {}

seqs = [10000,80000]
nr = [1,2,3,5,10]
device = get_device(gpu_index=1)
max_length = 2100

# Initialize the structure for each `nr` value
for seq in seqs:
    test_lev_accuracies[f"1D_{seq}"] = {"reads": [], "test_accs": []}

for r in nr:
    _, test_loader = get_data_loader(
                test_path, 
                end_sequence=100000, 
                start_sequence=80000, 
                batch_size=16, 
                num_reads=r, 
                overwrite_max_length=max_length, 
                dim_squeeze=True
            )
    for seq in seqs:
        model = CTC_Test_Model(input_length=max_length, tar_length=200, conv_1_dim=16,conv_2_dim=32, attention_dim=16, num_reads=r,
                 n_heads = 16, at_layer = 2,kernel_1 = 29, kernel_2 = 9)
        model_name = f"Data_{seq}_s_10_ep_{r}_r.pth"
        try:
            
            model_path = os.path.join(model_path_general, model_name)
      
            model.load_state_dict(torch.load(model_path))
            print(f"The following model is analyzed: {model_path}")
        except Exception as e:
            try:
            
                model_path = os.path.join(model_path_2d, model_name)
      
                model.load_state_dict(torch.load(model_path))
                print(f"The following model is analyzed: {model_path}")
            except Exception as e:
                print(f"The following model is missing: {model_path}\nError: {e}")
                continue

            
        
        model.eval()
        model.to(device)
        
        criterion = nn.CrossEntropyLoss()
        test_lev_ac = evaluate_model_ham(model, test_loader,device)

        # Save the sequence and test accuracy to the structure
        test_lev_accuracies[f"1D_{seq}"]["reads"].append(r)
        test_lev_accuracies[f"1D_{seq}"]["test_accs"].append(test_lev_ac)

seqs = [10000, 80000]
# Initialize the structure for each `nr` value
for seq in seqs:
    test_lev_accuracies[f"2D_{seq}"] = {"reads": [], "test_accs": []}


for r in nr:
    _, test_loader = get_data_loader(
                test_path, 
                end_sequence=100000, 
                start_sequence=80000, 
                batch_size=16, 
                num_reads=r, 
                overwrite_max_length=max_length, 
                dim_squeeze=True
            )
    for seq in seqs:
        try:
            model_name = f"2D_Data_{seq}_s_{10}_ep_{r}_r.pth"
            model_path = os.path.join(model_path_2D, model_name)
      
            
        
            model = CTC_2D_Model(input_length=max_length, tar_length=200, conv_1_dim=32,conv_2_dim=32, attention_dim=16, num_reads=r,
                 n_heads = 16, at_layer = 2, kernel_2=9, kernel_1 = 29)
            model.load_state_dict(torch.load(model_path))
            print(f"The following model is analyzed: {model_path}")
        except Exception as e:
            print(f"The following model is missing: {model_path}\nError: {e}")
            continue
        
        model.eval()
        model.to(device)
        
        criterion = nn.CrossEntropyLoss()
        test_lev_ac = evaluate_model_ham(model, test_loader,device)

        # Save the sequence and test accuracy to the structure
        test_lev_accuracies[f"2D_{seq}"]["reads"].append(r)
        test_lev_accuracies[f"2D_{seq}"]["test_accs"].append(test_lev_ac)






    

# Create the plot
sns.set_palette("Paired")
plt.figure(figsize=(10, 6))

for seq in seqs:
    plt.plot(test_lev_accuracies[f"2D_{seq}"]["reads"], test_lev_accuracies[f"2D_{seq}"]["test_accs"],'-o', label = f"2D Model - Training-Set Size: {seq}", markersize =10)
for seq in seqs:
    plt.plot(test_lev_accuracies[f"1D_{seq}"]["reads"], test_lev_accuracies[f"1D_{seq}"]["test_accs"],'-o', label = f"1D Model - Training-Set Size: {seq}", markersize =10)
        

plt.xlabel('Number of Input Reads', fontsize=20)
plt.ylabel('Test Levenshtein Accuracy', fontsize=20)
plt.tick_params(axis='both', labelsize=16)
plt.xticks(np.arange(min(test_lev_accuracies[f"1D_{seq}"]["reads"]), max(test_lev_accuracies[f"1D_{seq}"]["reads"])+1, 1), fontsize=16)
plt.xlim(0,11)
plt.ylim(45,75)
plt.legend(fontsize =16)
plt.tight_layout()
plt.grid(True)
plt.show()