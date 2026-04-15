
import copy
import time

class SudokuCSPSolver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.board = self._parse_file(file_path)
        self.positions = [(r, c) for r in range(9) for c in range(9)]
        self.adj_list = self._map_adjacencies()
        self.domains = self._init_domains()
        self.backtrack_calls = 0
        self.backtrack_failures = 0

    def _parse_file(self, filepath):
        """Reads the 9x9 grid from the given text file."""
        grid = []
        with open(filepath, 'r') as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    grid.append([int(char) for char in cleaned_line])
        return grid

    def _map_adjacencies(self):
        """Maps each cell to its row, column, and 3x3 box peers."""
        adj = {}
        for r, c in self.positions:
            peers = set()
            # Row and Column peers
            for i in range(9):
                peers.add((r, i))
                peers.add((i, c))
            
            # 3x3 Box peers
            box_r, box_c = (r // 3) * 3, (c // 3) * 3
            for i in range(3):
                for j in range(3):
                    peers.add((box_r + i, box_c + j))
            
            # Remove self from peers
            peers.remove((r, c))
            adj[(r, c)] = peers
        return adj

    def _init_domains(self):
        """Sets domain to {value} if filled, or {1-9} if empty."""
        doms = {}
        for r, c in self.positions:
            val = self.board[r][c]
            if val != 0:
                doms[(r, c)] = {val}
            else:
                doms[(r, c)] = set(range(1, 10))
        return doms

    def enforce_ac3(self, doms):
        """Arc Consistency 3 (AC-3) algorithm."""
        queue = [(pos, peer) for pos in self.positions for peer in self.adj_list[pos]]
        
        while queue:
            node_i, node_j = queue.pop(0)
            
            if self._revise(doms, node_i, node_j):
                if not doms[node_i]:
                    return False # Contradiction found
                
                for neighbor in self.adj_list[node_i]:
                    if neighbor != node_j:
                        queue.append((neighbor, node_i))
        return True

    def _revise(self, doms, node_i, node_j):
        """Removes illegal values from node_i's domain based on node_j."""
        modified = False
        for val in list(doms[node_i]):
            if len(doms[node_j]) == 1 and val in doms[node_j]:
                doms[node_i].remove(val)
                modified = True
        return modified

    def select_mrv_variable(self, assigned, doms):
        """Minimum Remaining Values heuristic for variable selection."""
        unassigned_vars = [p for p in self.positions if p not in assigned]
        return min(unassigned_vars, key=lambda p: (len(doms[p]), p))

    def forward_check(self, doms, pos, val):
        """Prunes domains of peers after a hypothetical assignment."""
        cloned_doms = copy.deepcopy(doms)
        cloned_doms[pos] = {val}
        
        for peer in self.adj_list[pos]:
            if val in cloned_doms[peer]:
                cloned_doms[peer].remove(val)
                if not cloned_doms[peer]:
                    return None # Domain wiped out
        return cloned_doms

    def backtrack(self, assigned, doms):
        """Recursive backtracking search with forward checking."""
        self.backtrack_calls += 1
        
        if len(assigned) == 81:
            return assigned # Solution found
            
        current_var = self.select_mrv_variable(assigned, doms)
        
        for val in sorted(list(doms[current_var])):
            updated_domains = self.forward_check(doms, current_var, val)
            
            if updated_domains:
                assigned[current_var] = val
                
                if self.enforce_ac3(updated_domains):
                    result = self.backtrack(assigned, updated_domains)
                    if result:
                        return result
                        
                del assigned[current_var]
                
        self.backtrack_failures += 1
        return None

    def execute(self):
        """Main execution flow for the solver."""
        if not self.enforce_ac3(self.domains):
            print("Unsolvable puzzle at AC-3 phase.")
            return
            
        initial_assignment = {pos: list(self.domains[pos])[0] 
                              for pos in self.positions if len(self.domains[pos]) == 1}
                              
        start_time = time.time()
        solution = self.backtrack(initial_assignment, self.domains)
        time_taken = time.time() - start_time
        
        return solution, self.backtrack_calls, self.backtrack_failures, time_taken


# --- Execution Script ---
if __name__ == '__main__':
    files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
    
    for f in files:
        try:
            solver = SudokuCSPSolver(f)
            sol, calls, fails, duration = solver.execute()
            print(f"--- Results for {f} ---")
            print(f"Calls: {calls} | Failures: {fails} | Time: {duration:.4f}s\n")
        except FileNotFoundError:
            print(f"File {f} not found in directory.")