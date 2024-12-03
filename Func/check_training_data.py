import numpy as np
import matplotlib.pyplot as plt
import os 
import subprocess
import pyslow5


def check_squigulator(fasta_folder, blow5_folder, reads_per_sequence):

    clear_seeds = []
    input_file = f"{fasta_folder}/fasta_file_{1000}.fasta"
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
        if signal[0] == 633:
            clear_seeds.append(j+1)
    return clear_seeds

def plot_squigulator(fasta_folder, blow5_folder, reads_per_sequence,seeds):
    print("Function to plot Squigulator")
    input_file = f"{fasta_folder}/fasta_file_{1111}.fasta"
    start_test_point = None
    for j in range (reads_per_sequence):
        output_file = f"{blow5_folder}/seq_{2}_read_{j}.blow5"
        # Command to be executed
        if j != 0:
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--ideal","--seed", str(seeds[j])]
        else:
            command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--ideal", "--seed",str(seeds[j])]
        

        # Run the command
        subprocess.run(command, check=True)
        s5 = pyslow5.Open(output_file, 'r')
        reads = s5.seq_reads()
        for read in reads:
            signal = read['signal']
            #plt.plot(signal, label = "Ideal Squigulator Signal")
            if j == 0:
                start_test_point = signal[0]
        if start_test_point != signal[0]:
            print(f"WTF at {seeds[j]}")
            input()



fasta_dir = "/media/hdd1/MoritzBa/Ideal_Data/Rd_Data_Fasta"
example_folder = "/workspaces/ForPrax/Temp"
#seeds = check_squigulator(fasta_dir,example_folder,40000)
#print(seeds)
#seeds = np.array(seeds)
#np.save("clear_seeds.npy", seeds)
signals = []
seqs = []
data_path = "/media/hdd1/MoritzBa/Ideal_Data/Rd_Data_Numpy"

sequence = 1 #7000 zum trainieren
num_reads = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
signals = np.load(f"{data_path}/signals_seq_{sequence}.npy")
for j in num_reads:
    # Load signal and pad to max_length
    
    plt.plot(signals[j,:])







#seeds = np.load("clear_seeds.npy")
#plot_squigulator(fasta_dir,example_folder,len(seeds),seeds)    
plt.xlim(0,400)
#plt.legend()
plt.show()
