import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)

nr = [1, 5, 10]  # Different numbers of input reads



test_lev_accuracies = {}



# Generate random training sequences and test accuracies

for r in nr:

    sequences = np.linspace(1000, 90000, 20)  # Training sequences

    test_accs = 50 + (r * 2) + np.random.normal(0, 2, len(sequences))  # Simulated test accuracies

    test_lev_accuracies[r] = {"sequences": sequences, "test_accs": test_accs}









# Create the plot
sns.set_palette("muted")
plt.figure(figsize=(10, 6))

for r in nr:
    plt.scatter(test_lev_accuracies[r]["sequences"], test_lev_accuracies[r]["test_accs"], label = f" Number of Input-Reads: {r}", marker ='o', s=50)

        

plt.xlabel('Training Sequences', fontsize=20)
plt.ylabel('Test Levenshtein Accuracy', fontsize=20)
plt.tick_params(axis='both', labelsize=16)
plt.xlim(0,90000)
plt.ylim(45,75)
plt.legend(fontsize =16)
plt.tight_layout()
plt.grid(True)
plt.show()