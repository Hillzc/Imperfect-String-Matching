import sys
from time import time
from naive import Naive_Imperfect_Search
from dp import DP_Imperfect_Search
from bitap import Bitap_Imperfect_Search

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"NAIVE", "DP", "BITAP"}:
        print("USAGE: python main.py <Algorithm Type>")
        print("<Algorithm Type>: [NAIVE/DP/BITAP]")
        exit()

    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    if sys.argv[1] == "NAIVE":
        searcher = Naive_Imperfect_Search(p, t, max_distance)
    elif sys.argv[1] == "DP":
        searcher = DP_Imperfect_Search(p, t, max_distance, print_alignment=True)
    elif sys.argv[1] == "BITAP":
        searcher = Bitap_Imperfect_Search(p, t, max_distance)
    


    found_locations = searcher.find_pattern()

    if sys.argv[1] != "DP": # dynamic programming implememtation does backtracking and prints the alignments itself
        for location in found_locations:
                print("-"*-location + t)
                print("-"*location + p + "-"*(len(t) - location - len(p)))
                print()

    return

if __name__ == '__main__':
    main()
