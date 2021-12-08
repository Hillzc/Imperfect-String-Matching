import numpy as np
import sys

# also known as global alignment
def levenshtein_distance(a, b, mismatch_cost = 1, gap_cost = 1):

    # initialize distance matrix
    distance_matrix = np.zeros([len(a)+1, len(b)+1])

    for i in range(1, len(a)+1):
        distance_matrix[i, 0] = i
    for j in range(1, len(b)+1):
        distance_matrix[0, j] = j
    
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                match_cost = distance_matrix[i-1, j-1]
            else:
                match_cost = distance_matrix[i-1, j-1] + mismatch_cost

            deletion_cost = distance_matrix[i-1, j] + gap_cost
            insertion_cost = distance_matrix[i, j-1] + gap_cost

            distance_matrix[i, j] = min(match_cost, deletion_cost, insertion_cost)

    max_distance = distance_matrix[len(a), len(b)]
    return max_distance


class Naive_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

    def find_pattern(self):

        found_locations = []
        for i in range(len(self.T) - len(self.P)):
            if levenshtein_distance(self.P, self.T[i: i+len(self.P)]) <= self.max_distance:
                found_locations.append(i)

        return found_locations

def main():
    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    searcher = Naive_Imperfect_Search(p, t, max_distance)
    
    searcher.find_pattern()


    return

if __name__ == '__main__':
    main()
