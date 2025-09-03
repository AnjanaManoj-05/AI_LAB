import heapq
from collections import deque

# Goal state
goal = [[1,2,3],[4,5,6],[7,8,0]]
goal_pos = {goal[i][j]:(i,j) for i in range(3) for j in range(3)}

# Flatten for hashing
def flatten(state):
    return tuple(x for row in state for x in row)

# Heuristic 1: Misplaced Tiles
def misplaced(state):
    cnt = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                cnt += 1
    return cnt

# Heuristic 2: Manhattan Distance
def manhattan(state):
    dist = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = goal_pos[state[i][j]]
                dist += abs(x - i) + abs(y - j)
    return dist

# Generate neighbors
def expand(state, path, g, heuristic):
    moves = [(1, 0, 'D'), (-1, 0, 'U'), (0, 1, 'R'), (0, -1, 'L')]
    zx, zy = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    children = []
    for dx, dy, m in moves:
        nx, ny = zx + dx, zy + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[zx][zy], new_state[nx][ny] = new_state[nx][ny], new_state[zx][zy]
            h = misplaced(new_state) if heuristic == 1 else manhattan(new_state)
            children.append((new_state, path + m, g + 1, g + 1 + h))
    return children

# A* Search
def astar(start, heuristic=1):
    h = misplaced(start) if heuristic == 1 else manhattan(start)
    pq = [(h, 0, start, "")]  # f, g, state, path
    visited = set()
    
    while pq:
        f, g, state, path = heapq.heappop(pq)
        
        # Display the current state
        print(f"Current State (f={f}, g={g}, h={h}):")
        for row in state:
            print(row)
        print()
        
        # Check if we've reached the goal
        if state == goal:
            print("Solved with", "Misplaced Tiles" if heuristic == 1 else "Manhattan Distance")
            print("Moves:", path)
            print("Steps:", g)
            return
        
        # Mark the current state as visited
        key = flatten(state)
        if key in visited:
            continue
        visited.add(key)
        
        # Expand the state and push new states to the priority queue
        for ns, p, gc, fc in expand(state, path, g, heuristic):
            if flatten(ns) not in visited:
                heapq.heappush(pq, (fc, gc, ns, p))

# Depth Limited Search (for IDDFS)
def dls(state, depth, path, visited):
    if state == goal:
        print("Solved with IDDFS")
        print("Moves:", path)
        print("Steps:", len(path))
        return True
    
    if depth == 0:
        return False
    
    visited.add(flatten(state))
    
    # Display the current state
    print(f"Current State (Depth {depth}):")
    for row in state:
        print(row)
    print()
    
    moves = [(1, 0, 'D'), (-1, 0, 'U'), (0, 1, 'R'), (0, -1, 'L')]
    zx, zy = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    
    for dx, dy, m in moves:
        nx, ny = zx + dx, zy + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[zx][zy], new_state[nx][ny] = new_state[nx][ny], new_state[zx][zy]
            if flatten(new_state) not in visited:
                if dls(new_state, depth - 1, path + m, visited):
                    return True
    return False

def iddfs(start, max_depth=30):
    for depth in range(max_depth + 1):
        visited = set()
        if dls(start, depth, "", visited):
            return
    print("Not solvable within depth", max_depth)

# Solvability check (inversions)
def is_solvable(state):
    arr = [x for row in state for x in row if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

# Example run
if __name__ == "__main__":
    start = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
    if not is_solvable(start):
        print("This puzzle is unsolvable!")
    else:
        astar(start, 1)  # Misplaced
        astar(start, 2)  # Manhattan
        iddfs(start, max_depth=20)
