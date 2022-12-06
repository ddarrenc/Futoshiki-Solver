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
                    self.domains[(r,j)].remove(val)

        # Update vertical domains
        for (_, c, val) in needs_update:
            for i in range(0, self.grid_size):
                if (i,c) in self.domains.keys() and val in self.domains[(i,c)]:
                    self.domains[(i,c)].remove(val)
        
        # Horizontal Constraints
        for i in range(self.grid_size):
            for j in range(self.grid_size-1):
                if (i,j) in self.hrz_con.keys():
                    constraint = self.hrz_con[(i,j)]
                    left = self.state[i][j]
                    right = self.state[i][j+1]

                    if (left == 0) ^ (right == 0):
                        if constraint == '>':
                            if left == 0:
                                self.domains[(i,j)] = list(filter(lambda x: x > right, self.domains[(i,j)]))
                            else:
                                self.domains[(i,j+1)] = list(filter(lambda x: x < left, self.domains[(i,j+1)]))
                        if constraint == '<':
                            if left == 0:
                                self.domains[(i,j)] = list(filter(lambda x: x < right, self.domains[(i,j)]))
                            else:
                                self.domains[(i,j+1)] = list(filter(lambda x: x > left, self.domains[(i,j+1)]))
                    elif left == 0 and right == 0:
                        if constraint == '>':
                            min_right = min(self.domains[(i,j+1)])
                            self.domains[(i,j)] = list(filter(lambda x: x > min_right, self.domains[(i,j)]))
                        elif constraint == '<':
                            min_left = min(self.domains[(i,j)])
                            self.domains[(i,j+1)] = list(filter(lambda x: x > min_left, self.domains[(i,j+1)]))
        
        # Vertical Constraints
        for i in range(self.grid_size-1):
            for j in range(self.grid_size):
                if (i,j) in self.vrt_con.keys():
                    constraint = self.vrt_con[(i,j)]
                    up = self.state[i][j]
                    down = self.state[i+1][j]

                    if (up == 0) ^ (down == 0):
                        if constraint == '^':
                            if up == 0:
                                self.domains[(i,j)] = list(filter(lambda x: x < down, self.domains[(i,j)]))
                            else:
                                self.domains[(i+1,j)] = list(filter(lambda x: x > up, self.domains[(i+1,j)]))
                        if constraint == 'v':
                            if up == 0:
                                self.domains[(i,j)] = list(filter(lambda x: x > down, self.domains[(i,j)]))
                            else:
                                self.domains[(i+1,j)] = list(filter(lambda x: x < up, self.domains[(i+1,j)]))
                    elif up == 0 and down == 0:
                        if constraint == '^':
                            min_up = min(self.domains[(i,j)])
                            self.domains[(i+1,j)] = list(filter(lambda x: x > min_up, self.domains[(i+1,j)]))
                        elif constraint == 'v':
                            min_down = min(self.domains[(i+1,j)])
                            self.domains[(i,j)] = list(filter(lambda x: x > min_down, self.domains[(i,j)]))

    def complete(self):
        return len(self.domains) == 0

    def select_unassigned_variable(self):
        suv_result = mrv(self.domains)
        
        if len(suv_result) == 1:
            return suv_result[0]
        
        return list(max(map(lambda x: degree(self.state, x), suv_result)))[1]

    def get_domain_values(self, coord):
        (r,c) = coord

        if (r,c) not in self.domains.keys() or len(self.domains[(r,c)]) == 0:
            return []

        return self.domains[(r,c)]

    # Given a coordinate (r,c), check if assigning it the value
    # parameter will result in a legal board state.
    # Return true / false
    def check_consistent(self, coord, value):
        # Check all different horizontal and vertical
        (r,c) = coord
        for j in range(self.grid_size):
            if (self.state[r][j] == value and j != c) or (self.state[j][c] == value and j != r):
                return False
        
        # Check inequalities
        return True

    def print_all(self):
        print("STATE:", self.state, "\n",)
        print("Hrz Con:", self.hrz_con)
        print("Vrt Con:", self.vrt_con)
        print("GridSize:", self.grid_size)
        print("Domains:", self.domains)

def mrv(domains):
    minlen = min(list(map(len, domains.values())))
    return list(filter(lambda x: len(domains[x])==minlen, domains))

def degree(state, point):
    N = len(state)
    (r,c) = point
    value = 0

    # Check number of unassigned horizontal and vertical neighbors
    for j in range(N):
        if state[r][j] == 0 and j != c:
            value += 1
        if state[j][c] == 0 and j != r:
            value += 1

    # Return the total mumber along with the point
    return (value, (r,c))

def solve_futoshiki(node:Futoshiki, assignment):
    if node.complete():
        print("SOLVED!")
        return True
    
    coord = node.select_unassigned_variable()
    
    for value in node.get_domain_values(coord):
        if node.check_consistent(coord, value):
            # TODO: Append to assignment
            # ...

            # TODO: Update state
            # ...

            # TODO: Recurse ?
            # ...
            return True

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
    solve_futoshiki(ftsk, {})
