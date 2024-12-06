import numpy as np
import matplotlib.pyplot as plt
import os 
import subprocess
import pyslow5


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

def plot_squigulator(fasta_folder, blow5_folder, reads_per_sequence,seeds, seq, squig="--ideal"):
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
            plt.plot(signal, label = f"Squigulator Signal with ideal type: {squig}")
            if j == 0:
                start_test_point = signal[0]
        if start_test_point != signal[0]:
            print(f"WTF at {seeds[j]}")
            #input()



fasta_dir = "/media/hdd1/MoritzBa/Data/Rd_Data_Fasta"
example_folder = "/workspaces/ForPrax/Temp"
#seeds = check_squigulator(fasta_dir,example_folder,40000)
#print(seeds)
#seeds = np.array(seeds)
#np.save("/media/hdd1/MoritzBa/Data/clear_seeds.npy", seeds)
signals = []
seqs = []
data_path = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"

sequence = 1000 #7000 zum trainieren
num_reads = []
signals = np.load(f"{data_path}/signals_seq_{sequence}.npy")
for j in num_reads:
    # Load signal and pad to max_length
    
    plt.plot(signals[j,:], label = f"Data Read {j}")


seeds = np.load("/media/hdd1/MoritzBa/Data/clear_seeds.npy")
#seeds = seeds[len(seeds)-50:len(seeds)-1]


plot_squigulator(fasta_dir,example_folder,5,seeds, sequence, squig="")  

#plot_squigulator(fasta_dir,example_folder,3,[1,2,3,4,5], sequence, squig="")    
plt.xlim(0,400)
plt.legend()
plt.show()
