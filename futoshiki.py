import os
import copy
import time

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
        #self.update_domain()

    def check_consistent(self, coord, value):
        (r,c) = coord

        # Non-repeating values in a row or column
        for j in range(self.grid_size):
            if (self.state[r][j] == value and j != c) or (self.state[j][c] == value and j != r):
                return False

        # Horizontal Constraints
        left  = (r, c-1)
        right = (r, c+1)
        if (r,c) in self.hrz_con.keys():
            constraint = self.hrz_con[(r,c)]
            if left != 0 and right != 0:
                if self.state[r][c+1] != 0:
                    if constraint == '>' and value <= self.state[r][c+1]:
                        return False
                    if constraint == '<' and value >= self.state[r][c+1]:
                        return False
            
        if (r, c-1) in self.hrz_con.keys():
            constraint = self.hrz_con[(r,c-1)]
            if left != 0 and right != 0:
                if self.state[r][c-1] != 0:
                    if constraint == '>' and value >= self.state[r][c-1]:
                        return False
                    if constraint == '<' and value <= self.state[r][c-1]:
                        return False

        # Vertical Constraints
        up   = (r-1, c)
        down = (r+1, c)

        if (r,c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r,c)]
            if up != 0 and down != 0:
                if self.state[r+1][c] != 0:
                    if constraint == '^' and value >= self.state[r+1][c]:
                        return False
                    if constraint == 'v' and value <= self.state[r+1][c]:
                        return False
            
        if (r-1, c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r-1,c)]
            if up != 0 and down != 0:
                if self.state[r-1][c] != 0:
                    if constraint == '^' and value <= self.state[r-1][c]:
                        return False
                    if constraint == 'v' and value >= self.state[r-1][c]:
                        return False

        return True

    def complete(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.state[i][j] == 0:
                    return False
        
        return True

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

    def assign(self, coord, value):
        (r,c) = coord
        self.state[r][c] = value
        del self.domains[(r,c)]

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

def solve_futoshiki(node:Futoshiki) -> Futoshiki:
    if node.complete():
        return node
    
    coord = node.select_unassigned_variable()
    for value in node.get_domain_values(coord):
        if node.check_consistent(coord, value):
            child = copy.deepcopy(node)
            child.assign(coord, value)
            result = solve_futoshiki(child)

            if result:
                return result

    return False

def load_input():
    tests_dir = sorted([x for x in os.listdir(INPUT_PATH) if "Input" in x])

    # Holds all the boards to solve
    ftsk_boards = []

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

            ftsk_boards.append((Futoshiki(initial_state, horizontal_constraints,
                                vertical_constraints, GRID_N), test))
   
    return ftsk_boards

def write_and_print_output(state, output_suffix):
    with open(OUTPUT_PATH + "Output" + output_suffix, "w") as f:
        N = len(state)

        for i in range(N):
            print(*state[i])
            for j in range(N):
                f.write(str(state[i][j]))
                if j != N-1:
                    f.write(' ')
            
            if i != N-1:
                f.write('\n')

def main():
    ftsk_boards = load_input()

    for (board, input_name) in ftsk_boards:
        print("\n***************************************************")
        print("Attempting to solve", input_name + "...")
        start_time = time.time()
        solution = solve_futoshiki(board)
        end_time = time.time()
        runtime = str(end_time - start_time)
        print("***************************************************")
        if not solution:
            print("No solution was found. took", runtime + "s")
        else:
            print("A solution was found! took", runtime + "s\n")
            output_suffix = input_name.split("Input")[1]
            write_and_print_output(solution.state, output_suffix)
            print("\nOutput written to", OUTPUT_PATH + "Output" + output_suffix)

if __name__ == "__main__":
    main()
