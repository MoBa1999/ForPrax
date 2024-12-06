import numpy as np  # Import der NumPy-Bibliothek, die hier nicht verwendet wird (kann optional entfernt werden).
import matplotlib.pyplot as plt  # Import der Matplotlib-Bibliothek zum Plotten von Daten.
import os  # Import der os-Bibliothek, die hier nicht verwendet wird (kann optional entfernt werden).
import subprocess  # Import der Subprocess-Bibliothek, um externe Prozesse auszuführen.
import pyslow5  # Import der pyslow5-Bibliothek, um BLOW5-Dateien zu lesen.

# Verzeichnis, in dem sich die Fasta Files befinden
fasta_folder = "/media/hdd1/MoritzBa/Time/Rd_Data_Fasta"
# Sequenznummer, die zur Identifikation der Datei dient.
seq = 0
# Verzeichnis, in dem die Ausgabe-BLOW5-Dateien gespeichert werden (temporär)
blow5_folder = "/workspaces/ForPrax/Temp"
# Pfad zur Eingabedatei im FASTA-Format.
input_file = f"/media/hdd1/MoritzBa/Time/Test/t.fasta"
# Pfad zur Ausgabedatei im BLOW5-Format.
output_file = f"{blow5_folder}/seq_{seq}_{0}.blow5"
# Seed 1: Definition des Random Seeds
seed = 24124
command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--seed", str(seed), "--ideal"]
subprocess.run(command, check=True)  # Ausführen des Squigulator-Befehls.

# Öffnen der generierten BLOW5-Datei im Lesemodus.
s5 = pyslow5.Open(output_file, 'r')
reads = s5.seq_reads()  # Abrufen der simulierten Reads aus der BLOW5-Datei.

# Iteration über alle Reads, um die Signale zu verarbeiten. -> hier nur 1 Read
for read in reads:
    signal = read['signal']  # Extrahieren des Signals aus dem Read.
    plt.plot(signal, label=f"Seed: {seed}")  # Plotten des Signals mit dem Seed-Wert als Label.
    print(signal[0:5])  # Ausgabe der ersten fünf Werte des Signals.

# Seed 1: Definition des Random Seeds
seed = 34081
command = ["/workspaces/ForPrax/Squigulator/squigulator", "-x", "dna-r9-min", input_file, "-o", output_file, "-n", "1", "--seed", str(seed), "--ideal"]
subprocess.run(command, check=True)  # Ausführen des Squigulator-Befehls.

# Öffnen der generierten BLOW5-Datei im Lesemodus.
s5 = pyslow5.Open(output_file, 'r')
reads = s5.seq_reads()  # Abrufen der simulierten Reads aus der BLOW5-Datei.

# Iteration über alle Reads, um die Signale zu verarbeiten. -> hier nur 1 Read
for read in reads:
    signal = read['signal']  # Extrahieren des Signals aus dem Read.
    plt.plot(signal, label=f"Seed: {seed}")  # Plotten des Signals mit dem Seed-Wert als Label.
    print(signal[0:5])  # Ausgabe der ersten fünf Werte des Signals.

# Einschränken der X-Achse auf die ersten 400 Datenpunkte.
plt.xlim(0, 400)
plt.legend()  # Anzeigen der Legende im Plot.
plt.plot()  # Anzeigen des finalen Plots.
