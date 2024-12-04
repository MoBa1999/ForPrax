import subprocess
import h5py
import pyslow5
import os
import numpy as np
import random 
import string
import re
import matplotlib.pyplot as plt
import random


def base_to_vector(base):
        """Konvertiert eine Base (A, T, C, G) in einen 4-dimensionalen Vektor."""
        vector = [0, 0, 0, 0]
        if base == 'A':
            vector[0] = 1
        elif base == 'T':
            vector[1] = 1
        elif base == 'C':
            vector[2] = 1
        elif base == 'G':
            vector[3] = 1
        return vector

def generate_fasta_files(num_files, output_folder, sequences_per_file, bias=0.5):
    """
    Generates multiple FASTA files with random sequences, with an optional bias against repeated bases.

    Args:
        num_files: The number of FASTA files to create.
        output_folder: The directory to save the FASTA files.
        sequences_per_file: The number of sequences per file.
        bias: The bias factor for repeated bases. A value of 0.5 means half the likelihood of repeated bases.
    """

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

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_files):
        filename = f"fasta_file_{i}.fasta"
        filepath = os.path.join(output_folder, filename)

        with open(filepath, 'w') as f:
            for j in range(sequences_per_file):
                sequence = generate_random_sequence(200, bias)
                f.write(f">File_{i}_Seq_{j}\n{sequence}\n")
        if i % 100 == 0:
            print(f"{i/num_files * 100} % done")

def process_sequence(fasta_folder, blow5_folder, output_dir, reads_per_sequence, cs_file, squigulator_type=None):
    """
    Processes sequences from FASTA files, generating blow5 files and converting them to NumPy arrays.

    Args:
        fasta_folder (str): Directory containing FASTA files.
        blow5_folder (str): Directory to store intermediate blow5 files.
        output_dir (str): Directory to store final NumPy arrays.
        reads_per_sequence (int): Number of reads to generate per sequence.
        cs_file (str): Path to the clear seeds file (.npy format).
        squigulator_type (str, optional): Additional squigulator parameter, if any.
    """
    fixed_length = 2100  # Fixed length to pad signal reads
    clear_seeds = np.load(cs_file)
    fasta_files = [os.path.join(fasta_folder, file) for file in os.listdir(fasta_folder) if file.endswith(".fasta")]
    num_files = len(fasta_files)
    print(f"{num_files} FASTA Files found in {fasta_folder}")

    for i, fasta_file in enumerate(fasta_files):
        try:
            # Read and process the FASTA file (assuming second line contains the sequence)
            with open(fasta_file, 'r') as file:
                lines = file.readlines()
                sequence = lines[1].strip()  # Second line (assuming sequence)

            sequence_data = np.array([base_to_vector(base) for base in sequence])
            all_signals = []
            
            # First loop: Generate blow5 files
            for j in range(reads_per_sequence):
                output_file = os.path.join(blow5_folder, f"seq_{i}_read_{j}.blow5")
                s = random.randint(0, len(clear_seeds)-1)

                # Generate the blow5 file using squigulator
                if squigulator_type:
                    command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", fasta_file, "-o", output_file, "-n", "1", "--seed", str(clear_seeds[s]), squigulator_type]
                else:
                    command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", fasta_file, "-o", output_file, "-n", "1", "--seed", str(clear_seeds[s])]
                subprocess.run(command, check=True)

            # Second loop: Read blow5 files and pad signals to the fixed length
            for j in range(reads_per_sequence):
                output_file = os.path.join(blow5_folder, f"seq_{i}_read_{j}.blow5")
                try:
                    s5 = pyslow5.Open(output_file, 'r')
                    reads = s5.seq_reads()

                    for read in reads:
                        signal = read['signal']
                        signal_array = np.array(signal, dtype=np.int16)

                        # Pad signal to the fixed length
                        if len(signal_array) < fixed_length:
                            signal_array = np.pad(signal_array, (0, fixed_length - len(signal_array)), mode='constant')
                        elif len(signal_array) > fixed_length:
                            print("Aaachtung zu lang!")
                            input()
                            signal_array = signal_array[:fixed_length]

                        all_signals.append(signal_array)

                    s5.close()
                except FileNotFoundError:
                    print(f"BLOW5 file not found: {output_file}")
                
                # Delete the BLOW5 file after processing
                if os.path.exists(output_file):
                    os.remove(output_file)

            # Combine signals into one NumPy array
            signal_array = np.vstack(all_signals)  # Combine aligned signals into one array

            # Save combined signal and sequence data for the current sequence
            output_signal_path = os.path.join(output_dir, f'signals_seq_{i}.npy')
            output_sequence_path = os.path.join(output_dir, f'sequence_seq_{i}.npy')

            np.save(output_signal_path, signal_array)
            np.save(output_sequence_path, sequence_data)

            print(f"Saved signals for sequence {i} to {output_signal_path}")
            print(f"Saved sequence {i} to {output_sequence_path}")

        except FileNotFoundError:
            print(f"FASTA file not found: {fasta_file}")


fasta_folder = "/media/hdd1/MoritzBa/Data/Rd_Data_Fasta"
blow5_folder = "/media/hdd1/MoritzBa/Data/Rd_Data_Blow5"
numpy_folder = "/media/hdd1/MoritzBa/Data/Rd_Data_Numpy"
clear_seed_file = "/workspaces/ForPrax/Func/clear_seeds.npy"


#generate_fasta_files(50000,fasta_folder,20,bias=0.75)
process_sequence(fasta_folder,blow5_folder,numpy_folder,20,clear_seed_file)
