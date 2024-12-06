import Levenshtein

def hamming_distance(s1, s2):
    """
    Berechnet die Hamming-Distanz zwischen zwei Strings.
    Voraussetzung: Beide Strings müssen die gleiche Länge haben.
    """
    if len(s1) != len(s2):
        raise ValueError("Hamming distance requires strings of equal length")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def compare_distances(string1, string2):
    """
    Vergleicht die Levenshtein-Distanz und die Hamming-Distanz
    zwischen zwei Strings.
    """
    # Berechne die Levenshtein-Distanz
    lev_distance = Levenshtein.distance(string1, string2)

    # Berechne die Hamming-Distanz (falls möglich)
    try:
        ham_distance = hamming_distance(string1, string2)
    except ValueError as e:
        ham_distance = str(e)

    # Ergebnisse ausgeben
    print(f"String 1: {string1}")
    print(f"String 2: {string2}")
    print(f"Levenshtein Distance: {lev_distance}")
    print(f"Hamming Distance: {ham_distance}")

# Nutzereingaben einholen
if __name__ == "__main__":
    print("Vergleich von Levenshtein- und Hamming-Distanz")
    string1 = input("Bitte den ersten String eingeben: ")
    string2 = input("Bitte den zweiten String eingeben: ")

    compare_distances(string1, string2)