import random
import math

# Heuristic: number of pairs of queens attacking each other
def calculate_cost(state):
    """Calculates the number of attacking queen pairs (cost)."""
    cost = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for same row or diagonal attack
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                cost += 1
    return cost

# Generate all neighbors of the current state (used by Hill Climb)
def get_neighbors(state):
    """Generates all possible neighbor states by moving one queen in one column."""
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if state[col] != row: # move queen in col to new row
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

# Hill climbing algorithm
def hill_climb(initial_state, max_steps=15):
    """Implements the standard steepest-ascent hill climbing algorithm."""
    current = initial_state
    current_cost = calculate_cost(current)
    
    print("\n" + "=" * 50)
    print("--- Hill Climbing Steps ---")
    print(f"Initial State (Step 0): {current}, Cost = {current_cost}")

    for step in range(1, max_steps + 1):
        if current_cost == 0:
            print(f"Goal state reached at step {step - 1}!")
            return current, current_cost
            
        neighbors = get_neighbors(current)
        best_neighbor = None
        best_cost = current_cost

        # Find the best neighbor (steepest ascent)
        for neighbor in neighbors:
            cost = calculate_cost(neighbor)
            if cost < best_cost:
                best_cost = cost
                best_neighbor = neighbor
                
        # If no better neighbor is found (local minimum or goal) → stop
        if best_neighbor is None:
            print(f"Stuck at local minimum/plateau at step {step}. Final state: {current}, Cost = {current_cost}")
            return current, current_cost

        # Move to the better neighbor
        current, current_cost = best_neighbor, best_cost
        print(f"Step {step}: Move to: {current}, Cost = {current_cost}")
        
    print(f"Max steps reached ({max_steps}). Final state: {current}, Cost = {current_cost}")
    return current, current_cost

# ----------------------------------------------------------------------

# Simulated annealing algorithm
def simulated_annealing(initial_state, initial_temp=2.0, cooling_rate=0.9, max_iterations=15):
    """Solves the N-Queens problem using Simulated Annealing."""
    current = initial_state
    current_cost = calculate_cost(current)
    temperature = initial_temp
    n = len(current)

    print("\n" + "=" * 50)
    print("--- Simulated Annealing Steps ---")
    print(f"Initial State (Step 0): {current}, Cost = {current_cost}, Temp = {temperature:.2f}")

    for step in range(1, max_iterations + 1):
        if current_cost == 0:
            print(f"Goal state reached at step {step - 1}!")
            return current, current_cost

        # Update temperature
        temperature *= cooling_rate

        if temperature <= 0.01:
             print(f"Temperature too low. Stopping at step {step}.")
             break

        # Generate a random neighbor
        col = random.randrange(n)
        new_row = random.randrange(n) 
        neighbor = current.copy()
        neighbor[col] = new_row
        neighbor_cost = calculate_cost(neighbor)

        delta_e = neighbor_cost - current_cost

        move_description = ""
        # Accept better state
        if delta_e < 0:
            current, current_cost = neighbor, neighbor_cost
            move_description = "BETTER (Accepted)"
        # Accept worse state probabilistically
        else:
            try:
                # Acceptance probability: P = e^(-ΔE / T)
                acceptance_prob = math.exp(-delta_e / temperature)
            except OverflowError:
                acceptance_prob = 0.0

            if random.random() < acceptance_prob:
                current, current_cost = neighbor, neighbor_cost
                move_description = f"WORSE (P={acceptance_prob:.2f} Accepted)"
            else:
                move_description = f"WORSE (P={acceptance_prob:.2f} Rejected)"
        
        print(f"Step {step}: {current}, Cost = {current_cost}, Temp = {temperature:.2f}, Move: {move_description}")

    print(f"Max steps reached ({max_iterations}). Final state: {current}, Cost = {current_cost}")
    return current, current_cost

# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    # 1. User Input for N (restricted to 4-7)
    while True:
        try:
            n = int(input("Enter number of queens (N, between 4 and 7): "))
            if 4 <= n <= 7:
                 break
            else:
                 print("N must be between 4 and 7, inclusive.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
    # 2. Generate Random Initial State
    # A list of length N where each element is a random row index (0 to N-1)
    initial_state = [4 ,3 ,2, 1, 2]
    
    # Optional: Set a seed for reproducibility if running multiple times
    # random.seed(42) 
    
    print("-" * 50)
    print(f"N = {n} queens.")
    print(f"**Generated Random Initial State: {initial_state}**")
    print("-" * 50)

    # Use max_steps = 15 for the demonstration
    MAX_STEPS = 15
    
    # 3. Hill Climbing (needs a copy of the state)
    hc_solution, hc_cost = hill_climb(initial_state.copy(), max_steps=MAX_STEPS)

    # 4. Simulated Annealing (needs a fresh copy of the state)
    # Adjust initial temperature based on N
    sa_solution, sa_cost = simulated_annealing(initial_state.copy(), max_iterations=MAX_STEPS, 
                                               initial_temp=2.0 * (n/4), cooling_rate=0.9)
    
    print("\n" + "=" * 50)
    print("--- Final Results Summary ---")
    print(f"N-Queens: N = {n}")
    print(f"Initial State: {initial_state}")
    print(f"Hill Climbing Final Cost: {hc_cost} ({'GOAL' if hc_cost == 0 else 'LOCAL MIN'})")
    print(f"Simulated Annealing Final Cost: {sa_cost} ")
    print("=" * 50)
