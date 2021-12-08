import numpy as np
import sys

class Node():
    def __init__(self, value, parents=[]):
        self.value = value
        self.parents = parents


class DP_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

        self.alignment_matrix = np.empty([len(self.P)+1, len(self.T)+1], dtype=Node)

    def print_alignment_matrix(self):
        matrix = np.empty([len(self.P)+1, len(self.T)+1])

        for i in range(len(self.P)+1):
            for j in range(len(self.T)+1):
                matrix[i, j] = self.alignment_matrix[i, j].value

        print(matrix)

    def find_pattern(self):

        # initialization
        self.initialize_alignment()

        # recurrence
        self.fill_alignment_matrix()
        #self.print_alignment_matrix()

        # find where to backtrack		
        bottom_row = self.alignment_matrix[len(self.P), :]
        indices = []
        for j in range(len(bottom_row)):
            node = bottom_row[j]
            if node.value <= self.max_distance:
                indices.append(j)

        # dfs to find all paths
        for index in indices:
            self.backtrack(index)
        
        return

    def initialize_alignment(self):
        self.alignment_matrix[0,0] = Node(0, [])

        for i in range(1,len(self.P)+1):
            self.alignment_matrix[i, 0] = Node(i, [(i-1, 0)])

        for j in range(1,len(self.T)+1):
            self.alignment_matrix[0, j] = Node(0, [(0, j-1)])

    def fill_alignment_matrix(self):
        for i in range(1, len(self.P)+1):
            for j in range(1, len(self.T)+1):

                P_gap_score = self.alignment_matrix[i-1, j].value + self.gap_penalty
                T_gap_score = self.alignment_matrix[i, j-1].value + self.gap_penalty
                if(self.P[i-1] == self.T[j-1]):
                    no_gap_score = self.alignment_matrix[i-1, j-1].value
                else:
                    no_gap_score = self.alignment_matrix[i-1, j-1].value + self.mismatch_penalty

                best_score = np.min([P_gap_score, T_gap_score, no_gap_score])

                parents = []
                if best_score == P_gap_score: # gap in sequence 1
                    parents.append((i-1, j))
                if best_score == T_gap_score: # gap in sequence 2
                    parents.append((i, j-1))
                if best_score == no_gap_score: # no gap
                    parents.append((i-1, j-1))

                self.alignment_matrix[i, j] = Node(best_score, parents)

    def backtrack(self, j):      

        aligned_T = self.T[j:]
        aligned_P = "-" * len(aligned_T)

        T = self.T[0:j]
        P = self.P

        self.dfs(len(self.P), j, aligned_T, aligned_P, T, P)
        
        return

    def dfs(self, i, j, aligned_T, aligned_P, T, P):

        node = self.alignment_matrix[i, j]
        parents = node.parents


        if len(parents) == 0:
            print(aligned_T)
            print(aligned_P)
            print()
            return

        for parent in parents:
            if parent[0] == i:
                new_aligned_P = "-" + aligned_P
                new_P = P
                new_aligned_T = T[-1] + aligned_T
                new_T = T[:-1]
            elif parent[1] == j:
                new_aligned_P = P[-1] + aligned_P
                new_P = P[:-1]
                new_aligned_T = "-" + aligned_T
                new_T = T
            else:
                new_aligned_P = P[-1] + aligned_P
                new_P = P[:-1]
                new_aligned_T = T[-1] + aligned_T
                new_T = T[:-1]
            self.dfs(parent[0], parent[1], new_aligned_T, new_aligned_P, new_T, new_P)


def main():
    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    aligner = DP_Imperfect_Search(p, t, max_distance)
    
    aligner.find_pattern()


    return

if __name__ == '__main__':
    main()
