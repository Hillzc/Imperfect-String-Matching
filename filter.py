import numpy as np
import sys

class Filter_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

    def find_pattern(self):

        pattern_letter_freqs = dict()

        for letter in self.P:
            if letter in pattern_letter_freqs:
                pattern_letter_freqs[letter] = pattern_letter_freqs[letter] + 1
            else:
                pattern_letter_freqs[letter] = 1

def main():
    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    searcher = Filter_Imperfect_Search(p, t, max_distance)
    
    searcher.find_pattern()


    return

if __name__ == '__main__':
    main()
