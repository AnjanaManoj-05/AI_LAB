import heapq

# Goal state
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Possible moves: up, down, left, right
moves = {
    'U': -3, 'D': 3, 'L': -1, 'R': 1
}

# Manhattan distance heuristic
def manhattan(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_pos = goal_state.index(tile)
        distance += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
    return distance

# Get neighbors
def get_neighbors(state):
    neighbors = []
    zero_pos = state.index(0)
    row, col = divmod(zero_pos, 3)

    for move, pos_change in moves.items():
        new_pos = zero_pos + pos_change

        # Check move validity
        if move == 'L' and col == 0: 
            continue
        if move == 'R' and col == 2: 
            continue
        if move == 'U' and row == 0: 
            continue
        if move == 'D' and row == 2: 
            continue

        new_state = list(state)
        new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
        neighbors.append(tuple(new_state))
    return neighbors

# A* algorithm
def a_star(start_state):
    pq = []
    heapq.heappush(pq, (manhattan(start_state), 0, start_state, [])) # (f, g, state, path)
    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if state in visited:
            continue
        visited.add(state)

        if state == goal_state:
            return path + [state]

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(pq, (g + 1 + manhattan(neighbor), g + 1, neighbor, path + [state]))
    return None

# Example usage
start_state = (0, 1, 2,
               3, 4, 6,
               7, 5, 8)

solution = a_star(start_state)
count=0
if solution:
    print("Steps to solve:")
    for step in solution:
        if(count==0):
            print("Start state")
        for i in range(0, 9, 3):
            print(step[i:i+3])
        count+=1
        print("===============")
    print("Goal state")
else:
    print("No solution found.")
