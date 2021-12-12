import sys
from time import time
from matplotlib import pyplot as plt
from naive import Naive_Imperfect_Search
from dp import DP_Imperfect_Search
from bitap import Bitap_Imperfect_Search
from filter import init_searcher

def main():
    sequences_path = "test.txt"
    repeats = 10
    pattern_lengths = range(10, 50, 2)
    errors = [0, 1, 2, 3, 4, 5]

    algorithms = ["Naive", "DP", "Bitap", "Filter_Naive", "Filter_DP", "Filter_Bitap"]
    
    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())
    
    # init data dicts
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
        pattern = t[:20]
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
    ax1.set_ylabel("Average Time (s)")
    ax1.set_xlabel("Pattern Length")

    for algorithm in error_number_data:
        ax2.plot(errors, error_number_data[algorithm])
    ax2.set_ylabel("Average Time (s)")
    ax2.set_xlabel("Maximum Allowed Errors")

    ax1.legend(algorithms)
    plt.show()

if __name__ == '__main__':
    main()
