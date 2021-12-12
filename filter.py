import numpy as np
import sys
import naive
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
    if name=="Filter_Naive":
        return Filter_Imperfect_Search(p, t, k, searcher_name="Naive")
    if name=="Filter_DP":
        return Filter_Imperfect_Search(p, t, k, searcher_name="DP")
    if name=="Filter_Bitap":
        return Filter_Imperfect_Search(p, t, k, searcher_name="Bitap")

class Filter_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1, searcher_name=None):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

        self.searcher_name = searcher_name

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
                window_letters[next_char] = window_letters[next_char] + 1
                if window_letters[next_char] <= pattern_letter_freqs[next_char]:
                    pattern_counter += 1

            # remove end char from window
            if window_end < (len(self.T) - 1):
                last_char = self.T[window_end+1]
                if last_char in window_letters and window_letters[last_char] > 0:
                    window_letters[last_char] = window_letters[last_char] - 1
                    if window_letters[last_char] < pattern_letter_freqs[last_char]:
                        pattern_counter -= 1
            
            if pattern_counter > (len(self.P) - self.max_distance):
                window = self.T[window_start:window_end]
                if (self.searcher_name != None):
                    searcher_name = init_searcher(self.searcher_name, self.P, window, self.max_distance)
                    found = searcher_name.find_pattern()
                    if (len(found) > 0):
                        found_locations.append(window_start)
                if naive.levenshtein_distance(self.P, window) <= self.max_distance:
                    found_locations.append(window_start)
        
        return found_locations

def main():
    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    searcher_name = Filter_Imperfect_Search(p, t, max_distance)
    
    print(searcher_name.find_pattern())


    return

if __name__ == '__main__':
    main()
