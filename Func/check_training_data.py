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
            plt.plot(signal, label = "Ideal Squigulator Signal")



fasta_dir = "/media/hdd1/MoritzBa/Ideal_Data/Rd_Data_Fasta"
example_folder = "/workspaces/ForPrax/Temp"
#seeds = check_squigulator(fasta_dir,example_folder,500)
#print(seeds)
signals = []
seqs = []
data_path = "/media/hdd1/MoritzBa/Ideal_Data/Rd_Data_Numpy"

sequence = 1000 #7000 zum trainieren
num_reads = []
for j in num_reads:
    # Load signal and pad to max_length
    signal = np.load(f"{data_path}/signal_seq_{sequence}_read_{j}.npy")
    print(signal)
    plt.plot(signal)







seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 37, 38, 40, 41, 43, 44, 45, 47, 48, 52, 54, 55, 58, 59, 60, 61, 62, 64, 66, 69, 71, 75, 76, 79, 80, 82, 83, 86, 88, 89, 90, 92, 93, 101, 104, 105, 107, 108, 111, 113, 115, 116, 118, 119, 120, 122, 123, 124, 125, 131, 133, 137, 138, 141, 142, 146, 149, 160, 163, 164, 166, 167, 169, 171, 172, 173, 176, 177, 180, 183, 184, 186, 188, 190, 191, 193, 195, 197, 201, 202, 205, 207, 208, 211, 214, 215, 220, 221, 222, 225, 226, 227, 228, 230, 233, 235, 238, 239, 240, 241, 243, 246, 247, 249, 251, 253, 254, 256, 257, 262, 264, 265, 266, 267, 268, 269, 271, 274, 276, 279, 281, 287, 292, 293, 295, 298, 303, 304, 305, 308, 309, 313, 317, 318, 320, 321, 322, 323, 325, 326, 329, 330, 331, 332, 333, 334, 335, 337, 338, 340, 341, 342, 344, 345, 346, 347, 352, 353, 355, 358, 362, 363, 365, 366, 368, 370, 372, 375, 376, 379, 382, 383, 386, 387, 389, 393, 394, 395, 398, 399, 402, 403, 404, 406, 409, 410, 411, 412, 414, 415, 419, 422, 425, 429, 430, 431, 432, 434, 440, 442, 443, 444, 447, 448, 450, 451, 452, 453, 454, 456, 458, 461, 464, 465, 466, 471, 475, 477, 478, 481, 482, 483, 484, 486, 488, 491, 492, 493, 494, 495, 500]
plot_squigulator(fasta_dir,example_folder,len(seeds),seeds)    
plt.xlim(0,400)
#plt.legend()
plt.show()
