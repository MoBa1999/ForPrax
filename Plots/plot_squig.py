import numpy as np
import matplotlib.pyplot as plt
import os 
import subprocess
import pyslow5
import seaborn as sns


def check_squigulator(fasta_folder, blow5_folder, reads_per_sequence):

    clear_seeds = []
    input_file = f"{fasta_folder}/fasta_file_{1001}.fasta"
    start_data = 0
    for j in range (reads_per_sequence):
        output_file = f"{blow5_folder}/seq_{2}_read_{j}.blow5"
        # Command to be executed
        if j != 0:
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--ideal","--seed", str(j+1)]
        else:
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--ideal", "--seed",str(j+1)]
        

        # Run the command
        subprocess.run(command, check=True)
        s5 = pyslow5.Open(output_file, 'r')
        reads = s5.seq_reads()
        for read in reads:
            signal = read['signal']
            #plt.plot(signal, label = "Ideal Squigulator Signal")
            if j == 0:
                start_data = signal[0]
        if signal[0] == start_data:
            clear_seeds.append(j+1)
    return clear_seeds

def plot_squigulator(fasta_folder, blow5_folder, reads_per_sequence,seeds, seq, squig="--ideal", label = None):
    print("Function to plot Squigulator")
    input_file = f"{fasta_folder}/fasta_file_{seq}.fasta"
    start_test_point = None
    for j in range (reads_per_sequence):
        output_file = f"{blow5_folder}/seq_{2}_read_{j}.blow5"
        # Command to be executed
        print(input_file)
        if squig != "":
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--seed", str(seeds[j]), squig]
        else:
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1","--seed",str(seeds[j])]
        

        # Run the command
        subprocess.run(command, check=True)
        s5 = pyslow5.Open(output_file, 'r')
        reads = s5.seq_reads()
        for read in reads:
            signal = read['signal']
            if label:
                 plt.plot(signal, label = label, linewidth = 3)
            else:
                plt.plot(signal, label = f"Squigulator Signal with ideal type: {squig}", linewidth = 10)
            if j == 0:
                start_test_point = signal[0]
        if start_test_point != signal[0]:
            print(f"WTF at {seeds[j]}")
            #input()



#fasta_dir = "/media/hdd1/MoritzBa/Data/Rd_Data_Fasta"
fasta_dir = "/workspaces/ForPrax/Data_Save/Data/Rd_Data_Fasta"
example_folder = "/workspaces/ForPrax/Temp"


signals = []
seqs = []
data_path = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"

sequence = 60002 #7000 zum trainieren

#seeds = seeds[len(seeds)-50:len(seeds)-1]

seeds = [1,2,3,4,5]

sns.set_palette("muted")
plt.figure(figsize=(10, 6))
plot_squigulator(fasta_dir,example_folder,1,seeds, sequence, squig="", label = "Realistic/Default Squigulator Data")  
plot_squigulator(fasta_dir,example_folder,1,seeds, sequence, squig="--ideal", label = "Ideal Squigulator Data")    
plot_squigulator(fasta_dir,example_folder,1,seeds, sequence, squig="--ideal-time", label = "Time-Ideal Squigulator Data")  
plt.xlim(0,200)
plt.xlabel("N samples", fontsize= 16)
plt.ylabel("Current (pA)", fontsize=16)
plt.tick_params(axis='both', labelsize=14)
plt.legend(fontsize = 14)
plt.tight_layout()
plt.grid(True)
plt.show()
