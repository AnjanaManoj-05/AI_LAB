import math

# Recursive function for Alpha–Beta Pruning
def alpha_beta_pruning(depth, node_index, is_maximizing, values, alpha, beta, max_depth):
    indent = "   " * depth  # for visual indentation
    if depth == max_depth:
        print(f"{indent}Reached leaf node[{node_index}] = {values[node_index]}")
        return values[node_index]

    if is_maximizing:
        best = -math.inf
        print(f"{indent}Maximizer at depth {depth}, Alpha={alpha}, Beta={beta}")
        for i in range(2):  # each node has 2 children
            val = alpha_beta_pruning(depth + 1, node_index * 2 + i, False, values, alpha, beta, max_depth)
            best = max(best, val)
            alpha = max(alpha, best)
            print(f"{indent}Max node[{node_index}] updated Best={best}, Alpha={alpha}, Beta={beta}")
            if beta <= alpha:
                print(f"{indent}-- Pruning remaining branches at Max node[{node_index}] (Beta <= Alpha) --")
                break
        return best

    else:  # Minimizer's turn
        best = math.inf
        print(f"{indent}Minimizer at depth {depth}, Alpha={alpha}, Beta={beta}")
        for i in range(2):
            val = alpha_beta_pruning(depth + 1, node_index * 2 + i, True, values, alpha, beta, max_depth)
            best = min(best, val)
            beta = min(beta, best)
            print(f"{indent}Min node[{node_index}] updated Best={best}, Alpha={alpha}, Beta={beta}")
            if beta <= alpha:
                print(f"{indent}-- Pruning remaining branches at Min node[{node_index}] (Beta <= Alpha) --")
                break
        return best


# ------------------------------------------
# Main Program
# ------------------------------------------
if __name__ == "__main__":
    print("=== Alpha–Beta Pruning (Cutoff) Search Algorithm ===\n")

    # Input: leaf node values
    n = int(input("Enter number of leaf nodes (power of 2): "))
    values = []
    for i in range(n):
        val = int(input(f"Enter value for leaf node[{i}]: "))
        values.append(val)

    print("\nLeaf Nodes (Terminal Values):", values)
    max_depth = int(math.log2(n))  # since binary tree

    print("\n========== Search Trace ==========\n")
    best_value = alpha_beta_pruning(0, 0, True, values, -math.inf, math.inf, max_depth)

    print("\n========== RESULT ==========")
    print(f"Optimal Value (Best for Maximizer): {best_value}")
