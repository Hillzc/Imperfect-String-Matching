import numpy as np
import sys

class Bitap_Imperfect_Search():
    def __init__(self, P, T, max_distance, mismatch_penalty=1, gap_penalty=1):

        self.P = P
        self.T = T
        self.max_distance = max_distance

        self.mismatch_penalty = int(mismatch_penalty)
        self.gap_penalty = int(gap_penalty)

    def find_pattern(self):

        # create pattern mask
        if (len(self.P) > 63): # python has a max int size based on the os
            print("Pattern is too long.")
            return

        print(self.P)

        print("pattern mask")
        pattern_mask = dict()
        for letter in self.T:
            if letter not in pattern_mask:
                mask = 0
                for i in range(len(self.P)):
                    mask |= (int(letter == self.P[i]) << i)
                pattern_mask[letter] = mask
        for letter in pattern_mask:
            print(letter, ":", bin(pattern_mask[letter]))

        # initialize R
        # R[d] stores all possible matches with up to d errors
        print("\nR[d, 0]")
        R = np.zeros([self.max_distance+1, len(self.T)+1], dtype=np.int64)
        for d in range(1, self.max_distance+1):
            R[d, 0] = R[d-1, 0] << 1 | 1
        
        for col in R:
            print(bin(col[0]))

        # iterate
        print("\n")
        found_locations = set()
        for i in range(1, len(self.T)+1):
            # R[0] is with no errors
            R[0, i] = (R[0, i-1] << 1 | 1) & pattern_mask[self.T[i-1]]
            if R[0, i] >> (len(self.P)-1) == 1:
                found_locations.add(i-len(self.P))

            for d in range(1, self.max_distance+1):
                R[d, i] = (R[d, i-1] << 1 | 1) & pattern_mask[self.T[i-1]] \
                    | ((R[d-1, i-1] | R[d-1, i]) << 1 | 1) \
                        | R[d-1, i-1]
                if(R[d, i] >> len(self.P)-1) == 1:
                    found_locations.add(i-len(self.P))

        for location in found_locations:
            print("-"*-location + self.T)
            print("-"*location + self.P + "-"*(len(self.T) - location - len(self.P)))
            print()

def main():
    sequences_path = "test.txt"

    # Get sequences
    with open(sequences_path, "r") as sequences_file:
        p = sequences_file.readline().rstrip().upper()
        t = sequences_file.readline().rstrip().upper()
        max_distance = int(sequences_file.readline().rstrip())

    searcher = Bitap_Imperfect_Search(p, t, max_distance)
    
    searcher.find_pattern()


    return

if __name__ == '__main__':
    main()
