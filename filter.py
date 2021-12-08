import numpy as np
import sys
import naive
from naive import Naive_Imperfect_Search
from dp import DP_Imperfect_Search
from bitap import Bitap_Imperfect_Search

class Filter_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

    def find_pattern(self):

        # find initial letter frequency
        pattern_letter_freqs = dict()
        for letter in self.P:
            if letter in pattern_letter_freqs:
                pattern_letter_freqs[letter] = pattern_letter_freqs[letter] + 1
            else:
                pattern_letter_freqs[letter] = 1

        # initialize window letter frequency dict
        window_letters = dict()
        for letter in pattern_letter_freqs:
            window_letters[letter] = 0
        window_length = len(self.P) # variable sized windows can also be used

        window_end = len(self.T)-1
        pattern_counter = 0 # tracks how many letters within the pattern have been seen
        found_locations = []
        for window_start in range(window_end, -1, -1):
            # advance window end
            if window_start < (len(self.T) - window_length):
                window_end -= 1
            
            # add next char to window
            next_char = self.T[window_start]
            if next_char in window_letters:
                print("adding ", next_char)
                window_letters[next_char] = window_letters[next_char] + 1
                if window_letters[next_char] <= pattern_letter_freqs[next_char]:
                    pattern_counter += 1

            # remove end char from window
            if window_end < (len(self.T) - 1):
                last_char = self.T[window_end+1]
                print("removing ", last_char)
                if last_char in window_letters and window_letters[last_char] > 0:
                    window_letters[last_char] = window_letters[last_char] - 1
                    if window_letters[last_char] < pattern_letter_freqs[last_char]:
                        pattern_counter -= 1
            
            if pattern_counter > (len(self.P) - self.max_distance):
                if naive.levenshtein_distance(self.P, self.T[window_start:window_end]) <= self.max_distance:
                    found_locations.append(window_start)
        
        return found_locations

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
