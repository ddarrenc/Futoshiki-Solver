import os
import copy
import time

INPUT_PATH = "inputs/"    # Path of input text files
OUTPUT_PATH = "outputs/"  # Path of output text files
INPUT_SIZE = 16           # Required number of lines in input file
GRID_N = 5                # Size of puzzle board NxN

<<<<<<< HEAD
=======

>>>>>>> 7dbb449 (first local commit)
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
<<<<<<< HEAD
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
=======
        # Initialize the domains for each variable (coordinate) on the board
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.state[r][c] == 0:
                    self.domains[(r, c)] = list(range(1, GRID_N+1))
        # self.update_domain()

    def check_consistent(self, coord, value):
        # Check if assigning the value to the variable at the
        # given coordinate is consistent with the constraints
        (r, c) = coord

        # Check if the value is already present in the same row or column
        for j in range(self.grid_size):
            if (self.state[r][j] == value and j != c) or \
               (self.state[j][c] == value and j != r):
                return False

        # Horizontal Constraints
        left = (r, c-1)
        right = (r, c+1)
        if (r, c) in self.hrz_con.keys():
            constraint = self.hrz_con[(r, c)]
>>>>>>> 7dbb449 (first local commit)
            if left != 0 and right != 0:
                if self.state[r][c+1] != 0:
                    if constraint == '>' and value <= self.state[r][c+1]:
                        return False
                    if constraint == '<' and value >= self.state[r][c+1]:
                        return False
<<<<<<< HEAD
            
        if (r, c-1) in self.hrz_con.keys():
            constraint = self.hrz_con[(r,c-1)]
=======
        if (r, c-1) in self.hrz_con.keys():
            constraint = self.hrz_con[(r, c-1)]
>>>>>>> 7dbb449 (first local commit)
            if left != 0 and right != 0:
                if self.state[r][c-1] != 0:
                    if constraint == '>' and value >= self.state[r][c-1]:
                        return False
                    if constraint == '<' and value <= self.state[r][c-1]:
                        return False

        # Vertical Constraints
<<<<<<< HEAD
        up   = (r-1, c)
        down = (r+1, c)

        if (r,c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r,c)]
=======
        up = (r-1, c)
        down = (r+1, c)

        if (r, c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r, c)]
>>>>>>> 7dbb449 (first local commit)
            if up != 0 and down != 0:
                if self.state[r+1][c] != 0:
                    if constraint == '^' and value >= self.state[r+1][c]:
                        return False
                    if constraint == 'v' and value <= self.state[r+1][c]:
                        return False
<<<<<<< HEAD
            
        if (r-1, c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r-1,c)]
=======
        if (r-1, c) in self.vrt_con.keys():
            constraint = self.vrt_con[(r-1, c)]
>>>>>>> 7dbb449 (first local commit)
            if up != 0 and down != 0:
                if self.state[r-1][c] != 0:
                    if constraint == '^' and value <= self.state[r-1][c]:
                        return False
                    if constraint == 'v' and value >= self.state[r-1][c]:
                        return False
<<<<<<< HEAD

=======
>>>>>>> 7dbb449 (first local commit)
        return True

    def complete(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.state[i][j] == 0:
                    return False
<<<<<<< HEAD
        
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
=======
        return True

    def select_unassigned_variable(self):
        # Get the list of variables that have the
        # minimum remaining values (MRV)
        suv_result = mrv(self.domains)
        # If there is only one MRV, return it
        if len(suv_result) == 1:
            return suv_result[0]

        # Return the variable with the highest degree heuristic among the MRVs
        return list(max(map(lambda x: degree(self.state, x), suv_result)))[1]

    def get_domain_values(self, coord):
        (r, c) = coord

        if (r, c) not in self.domains.keys() or len(self.domains[(r, c)]) == 0:
            return []

        return self.domains[(r, c)]

    def assign(self, coord, value):
        (r, c) = coord
        self.state[r][c] = value
        del self.domains[(r, c)]
>>>>>>> 7dbb449 (first local commit)

    def print_all(self):
        print("STATE:", self.state, "\n",)
        print("Hrz Con:", self.hrz_con)
        print("Vrt Con:", self.vrt_con)
        print("GridSize:", self.grid_size)
        print("Domains:", self.domains)

<<<<<<< HEAD
def mrv(domains):
    minlen = min(list(map(len, domains.values())))
    return list(filter(lambda x: len(domains[x])==minlen, domains))

def degree(state, point):
    N = len(state)
    (r,c) = point
=======

def mrv(domains):
    # Get the minimum length of the values in the domains dictionary
    minlen = min(list(map(len, domains.values())))

    # Return a list of keys for which the
    # corresponding value has the minimum length
    return list(filter(lambda x: len(domains[x]) == minlen, domains))


def degree(state, point):
    N = len(state)
    (r, c) = point
>>>>>>> 7dbb449 (first local commit)
    value = 0

    # Check number of unassigned horizontal and vertical neighbors
    for j in range(N):
        if state[r][j] == 0 and j != c:
            value += 1
        if state[j][c] == 0 and j != r:
            value += 1

    # Return the total mumber along with the point
<<<<<<< HEAD
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
=======
    return (value, (r, c))


def solve_futoshiki(node: Futoshiki) -> Futoshiki:
    # If the current node represents a completed board, return it
    if node.complete():
        return node

    # Select an unassigned variable (coordinate) on the board
    coord = node.select_unassigned_variable()

    # Iterate over the possible values for the selected variable
    for value in node.get_domain_values(coord):
        # Check if assigning the value to the variable is
        # consistent with the constraints
        if node.check_consistent(coord, value):
            # Create a child node by assigning the value to the variable
            child = copy.deepcopy(node)
            child.assign(coord, value)

            # Recursively solve the child node
            result = solve_futoshiki(child)

            # If the child node has a solution, return it
            if result:
                return result
    # No Solution
    return False


def load_input():
    # Get a list of input files in the input directory
>>>>>>> 7dbb449 (first local commit)
    tests_dir = sorted([x for x in os.listdir(INPUT_PATH) if "Input" in x])

    # Holds all the boards to solve
    ftsk_boards = []

<<<<<<< HEAD
    for test in tests_dir:
        with open(INPUT_PATH + test, "r") as f:
            lines = f.readlines()
            line_length = len(lines)

=======
    # Iterate over the input files
    for test in tests_dir:
        # Open the current input file in read mode
        with open(INPUT_PATH + test, "r") as f:
            # Read the lines from the file
            lines = f.readlines()
            # Get the number of lines in the file
            line_length = len(lines)

            # Check if the file has the correct number of lines
>>>>>>> 7dbb449 (first local commit)
            if line_length != INPUT_SIZE:
                raise ValueError("Incorrect input formatting for",
                                 test, "refer to documentation")

<<<<<<< HEAD
=======
            # Initialize the board state, horizontal constraints,
            # and vertical constraints
>>>>>>> 7dbb449 (first local commit)
            initial_state = []
            horizontal_constraints = {}
            vertical_constraints = {}

            # Build the initial state board
            for i in range(0, GRID_N):
<<<<<<< HEAD
                initial_state.append(list(map(int, lines[i].strip().split(" "))))
=======
                initial_state.append(
                    list(map(int, lines[i].strip().split(" ")))
                )
>>>>>>> 7dbb449 (first local commit)

            # Build the dict of horizontal constraints
            for i in range(GRID_N+1, 2*GRID_N+1):
                ln = lines[i].strip().split(" ")
                for j in range(len(ln)):
                    if ln[j] in ['>', '<']:
                        horizontal_constraints[(i-GRID_N-1, j)] = ln[j]
<<<<<<< HEAD
            
=======

>>>>>>> 7dbb449 (first local commit)
            # Build the dict of vertical constraints
            for i in range(2*GRID_N+2, line_length):
                ln = lines[i].strip().split(" ")
                for j in range(len(ln)):
<<<<<<< HEAD
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
=======
                    if ln[j] in ['^', 'v']:
                        vertical_constraints[(i-2*GRID_N-2, j)] = ln[j]

            # Append the board data and input file name
            # to the list of boards to solve
            ftsk_boards.append(
                (Futoshiki(initial_state, horizontal_constraints,
                           vertical_constraints, GRID_N), test)
                )

    # Return the list of boards to solve
    return ftsk_boards


def write_and_print_output(state, output_suffix):
    # Open the output file in write mode
    with open(OUTPUT_PATH + "Output" + output_suffix, "w") as f:
        # Get the size of the state matrix
        N = len(state)

        # Iterate over the rows of the state matrix
        for i in range(N):
            # Print the current row
            print(*state[i])

            # Iterate over the elements in the current row
            for j in range(N):
                # Write the current element to the output file
                f.write(str(state[i][j]))

                # If the current element is not the last in the row
                if j != N-1:
                    f.write(' ')

            # If the current row is not the last
            if i != N-1:
                f.write('\n')


def main():
    # Load input data from files
    ftsk_boards = load_input()

    # Iterate over the loaded input data
    for (board, input_name) in ftsk_boards:
        # Print the name of the input file being processed
        print("\n***************************************************")
        print("Attempting to solve", input_name + "...")

        # Start the timer
        start_time = time.time()

        # Attempt to solve the Futoshiki puzzle
        solution = solve_futoshiki(board)

        # Stop the timer
        end_time = time.time()

        # Calculate the runtime
        runtime = str(end_time - start_time)
        print("***************************************************")

        # If no solution was found, print a message
        if not solution:
            print("No solution was found. took", runtime + "s")
        else:
            # If a solution was found, print a message and
            # write the solution to a file
            print("A solution was found! took", runtime + "s\n")
            output_suffix = input_name.split("Input")[1]
            write_and_print_output(solution.state, output_suffix)
            print("\nOutput written to", OUTPUT_PATH +
                  "Output" + output_suffix)

>>>>>>> 7dbb449 (first local commit)

if __name__ == "__main__":
    main()
