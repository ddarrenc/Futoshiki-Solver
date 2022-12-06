import os

INPUT_PATH = "inputs/"    # Path of input text files
OUTPUT_PATH = "outputs/"  # Path of output text files
INPUT_SIZE = 16           # Required number of lines in input file
GRID_N = 5                # Size of puzzle board NxN

class Futoshiki:
    def __init__(self, istate, hrz_con, vrt_con, n):
        self.istate = istate
        self.state = istate
        self.hrz_con = hrz_con
        self.vrt_con = vrt_con
        self.grid_size = n
        self.domains = {}
        self.init_domain()

    def init_domain(self):
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.state[r][c] == 0:
                    self.domains[(r,c)] = list(range(1, GRID_N+1))
        
        self.update_domain()

    # Just to update the domain values.
    # Don't care about satisfying constraints,
    # which should be handled in different function.
    def update_domain(self):
        # Non-repeating values in a row or column
        needs_update = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.state[i][j] != 0:
                    needs_update.append((i, j, self.state[i][j]))

        # Update horizontal domains
        for (r, _, val) in needs_update:
            for j in range(0, self.grid_size):
                if (r,j) in self.domains.keys() and val in self.domains[(r,j)]:
                    print(self.domains[(r,j)], val)
                    self.domains[(r,j)].remove(val)

        # Update vertical domains
        for (_, c, val) in needs_update:
            for i in range(0, self.grid_size):
                if (i,c) in self.domains.keys() and val in self.domains[(i,c)]:
                    self.domains[(i,c)].remove(val)
        
        # TODO: Add horizontal / vertical constraint checker
        print(self.domains)
                    

    def complete(self):
        return len(self.domains) == 0

    def mrv(self):
        minlen = min(list(map(len, self.domains.values())))
        return list(filter(lambda x: len(self.domains[x])==minlen, self.domains))

    def select_unassigned_variable(self):
        print(self.mrv())
        

    def print_all(self):
        print("STATE:", self.state, "\n",)
        print("Hrz Con:", self.hrz_con)
        print("Vrt Con:", self.vrt_con)
        print("GridSize:", self.grid_size)
        print("Domains:", self.domains)

            
def solve_futoshiki(node):
    if node.complete():
        print("SOLVED!")
        return
    
    #node.select_unassigned_variable()
    





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
                        horizontal_constraints[(i-GRID_N-1, j)] = ln[j]
            
            # Build the dict of vertical constraints
            for i in range(2*GRID_N+2, line_length):
                ln = lines[i].strip().split(" ")
                for j in range(len(ln)):
                    if ln[j] in ['^','v']:
                        vertical_constraints[(i-2*GRID_N-2, j)] = ln[j]

            return Futoshiki(initial_state, horizontal_constraints, vertical_constraints, GRID_N)


if __name__ == "__main__":
    ftsk = load_input()
    solve_futoshiki(ftsk)