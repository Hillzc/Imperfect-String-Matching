import sys
from time import time
from matplotlib import pyplot as plt
from naive import Naive_Imperfect_Search
from dp import DP_Imperfect_Search
from bitap import Bitap_Imperfect_Search

def init_searcher(name, p, t, k):
    if name=="Naive":
        return Naive_Imperfect_Search(p, t, k)
    if name=="DP":
        return DP_Imperfect_Search(p, t, k, print_alignment=False)
    if name=="Bitap":
        return Bitap_Imperfect_Search(p, t, k)

def main():
    sequences_path = "test.txt"
    repeats = 1
    pattern_lengths = [10, 20, 30, 40, 50, 60]
    errors = [0, 1, 2]

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    algorithms = ["Naive", "DP", "Bitap"]
    
    # init dicts
    pattern_length_data = dict()
    error_number_data = dict()

    for algorithm in algorithms:

        pattern_length_data[algorithm] = []
        max_errors = 2
        for pattern_length in pattern_lengths:
            pattern = t[:pattern_length]
            searcher = init_searcher(algorithm, pattern, t, max_errors)
            t0 = time()
            for i in range(repeats):
                searcher.find_pattern()
            t1 = time()
            time_taken = (t1 - t0)/repeats
            pattern_length_data[algorithm] = pattern_length_data[algorithm] + [time_taken]

        error_number_data[algorithm] = []
        pattern = t[:10]
        for error in errors:
            searcher = init_searcher(algorithm, pattern, t, error)
            t0 = time()
            for i in range(repeats):
                searcher.find_pattern()
            t1 = time()
            time_taken = (t1 - t0)/repeats
            error_number_data[algorithm] = error_number_data[algorithm] + [time_taken]

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    for algorithm in pattern_length_data:
        ax1.plot(pattern_lengths, pattern_length_data[algorithm])
    ax1.legend(algorithms)

    for algorithm in error_number_data:
        ax2.plot(errors, error_number_data[algorithm])
    ax2.legend(algorithms)

    plt.show()

if __name__ == '__main__':
    main()
