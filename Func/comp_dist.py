import Levenshtein
import sys
import os
import torch
from torch import nn
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

# Append paths for custom functions if needed
sys.path.append("/workspaces/ForPrax/Func")
sys.path.append("/workspaces/ForPrax/Models")
from data_prep_func import get_data_loader, get_device, vectors_to_sequence
from eval_utils import evaluate_model_ham, plot_training_curves_separate
from CTC_Test import CTC_Test_Model

def hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings.
    Precondition: Both strings must be of the same length.
    """
    if len(s1) != len(s2):
        raise ValueError("Hamming distance requires strings of equal length")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def compare_distances(string1, string2):
    """
    Compares the Levenshtein distance and the Hamming distance
    between two strings.
    """
    # Calculate Levenshtein distance
    lev_distance = Levenshtein.distance(string1, string2)

    # Calculate Hamming distance (if possible)
    try:
        ham_distance = hamming_distance(string1, string2)
    except ValueError as e:
        ham_distance = str(e)

    return ham_distance, lev_distance


string1 = input("Enter the first phrase: ")
string2 = input("Enter the second phrase: ")

# Compare distances
ham_distance, lev_distance = compare_distances(string1, string2)

    # Output results
print(f"Hamming Distance: {ham_distance}")
print(f"Levenshtein Distance: {lev_distance}")


