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

#test_path = "/media/hdd1/MoritzBa/Test_Data/Rd_Data_Numpy"
test_path = "/media/hdd1/MoritzBa/Time/Rd_Data_Numpy"

model_path_general = "/media/hdd1/MoritzBa/Models"


test_lev_accuracies = {}

seqs = [10000, 20000, 40000]
nr = [1, 5, 10]
device = get_device(gpu_index=1)
max_length = 2100

# Initialize the structure for each `nr` value
for r in nr:
    test_lev_accuracies[r] = {"sequences": [], "test_accs": []}

for seq in seqs:
    for r in nr:
        try:
            model_name = f"Time_{seq}_s_75_ep_{r}_r.pth"
            model_path = os.path.join(model_path_general, model_name)
      
            _, test_loader = get_data_loader(
                test_path, 
                end_sequence=50000, 
                start_sequence=40000, 
                batch_size=16, 
                num_reads=r, 
                overwrite_max_length=max_length, 
                dim_squeeze=True
            )
        
            model = CTC_Test_Model(input_length=max_length, tar_length=200, conv_1_dim=16,conv_2_dim=32, attention_dim=16, num_reads=r,
                 n_heads = 16, at_layer = 2)
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
        test_lev_accuracies[r]["sequences"].append(seq)
        test_lev_accuracies[r]["test_accs"].append(test_lev_ac)

# Example usage






    

# Create the plot
sns.set_palette("muted")
plt.figure(figsize=(10, 6))

for r in nr:
    plt.scatter(test_lev_accuracies[r]["sequences"], test_lev_accuracies[r]["test_accs"], label = f" Number of Input-Reads: {r}", marker ='o', s=50)

        

plt.xlabel('Training Sequences', fontsize=14)
plt.ylabel('Test Levenshtein Accuracy', fontsize=14)
plt.tick_params(axis='both', labelsize=12)
plt.xlim(0,50000)
plt.ylim(60,100)
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()