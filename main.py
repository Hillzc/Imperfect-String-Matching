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
        searcher = DP_Imperfect_Search(p, t, max_distance)
    elif sys.argv[1] == "BITAP":
        searcher = Bitap_Imperfect_Search(p, t, max_distance)
    
    t0 = time()
    for i in range(10):
        searcher.find_pattern()
    t1 = time()
    time_taken = (t1 - t0)/10

    print("time elapsed: {}".format(time_taken))

    return

if __name__ == '__main__':
    main()