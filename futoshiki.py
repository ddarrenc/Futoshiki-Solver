import os

INPUT_PATH = "inputs/"    # Path of input text files
OUTPUT_PATH = "outputs/"  # Path of output text files
INPUT_SIZE = 16           # Required number of lines in input file
GRID_N = 5                # Size of puzzle board NxN

def load_input():
    tests_dir = sorted([x for x in os.listdir(INPUT_PATH) if "Input" in x])

    for test in tests_dir:
        with open(INPUT_PATH + test, "r") as f:
            lines = f.readlines()
            line_length = len(lines)

            if line_length != INPUT_SIZE:
                raise ValueError("Incorrect input formatting for",
                                 test, "refer to documentation")

            initial_state = []
            horizontal_constraints = {}
            vertical_constraints = {}


            # Build the initial state board
            for i in range(0, GRID_N):
                initial_state.append(list(map(int, lines[i].strip().split(" "))))

            # Build the dict of horizontal constraints
            for i in range(GRID_N+1, 2*GRID_N+1):
                ln = lines[i].strip().split(" ")
                for j in range(len(ln)):
                    if ln[j] in ['>', '<']:
                        horizontal_constraints[(i-GRID_N-1,j)] = ln[j]
            
            # Build the dict of vertical constraints
            for i in range(2*GRID_N+2, line_length):
                ln = lines[i].strip().split(" ")
                for j in range(len(ln)):
                    if ln[j] in ['^','v']:
                        vertical_constraints[(i-2*GRID_N-2,j)] = ln[j]



            



if __name__ == "__main__":
    load_input()
