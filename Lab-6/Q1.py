from itertools import product

# --- Helper logical functions ---
def implies(a, b): return (not a) or b
def neg(a): return not a
def disj(a, b): return a or b     # OR (∨)
def conj(a, b): return a and b    # AND (∧)

# --- Evaluate KB sentences for given model ---
def evaluate_KB(P, Q, R):
    # KB sentences
    s1 = implies(conj(P, Q), R)     # (P ∧ Q) → R
    s2 = disj(P, Q)                 # (P ∨ Q)
    s3 = neg(conj(P, neg(R)))       # ¬(P ∧ ¬R)
    KB_true = s1 and s2 and s3
    return s1, s2, s3, KB_true

# --- Entailment checker ---
def entails(KB_eval_func, query_func):
    symbols = ['P', 'Q', 'R']
    print("Truth Table for KB and Query\n")
    print(f"{'P':<3}{'Q':<3}{'R':<3}| {'(P∧Q)→R':<8}|{'P∨Q':<5}|{'¬(P∧¬R)':<9}| {'KB':<3}| {'Query':<8}")
    print("-" * 65)

    entailment_holds = True
    valid_models = []

    for P, Q, R in product([False, True], repeat=3):
        s1, s2, s3, KB_true = KB_eval_func(P, Q, R)
        query_val = query_func(P, Q, R)

        if KB_true:
            valid_models.append((P, Q, R, query_val))
            if not query_val:
                entailment_holds = False

        print(f"{int(P):<3}{int(Q):<3}{int(R):<3}| {int(s1):<8}|{int(s2):<5}|{int(s3):<9}| {int(KB_true):<3}| {int(query_val):<8}")

    print("\nModels where KB is True:")
    for m in valid_models:
        print(f"P={int(m[0])}, Q={int(m[1])}, R={int(m[2])}, Query={int(m[3])}")

    print("\nResult:")
    if entailment_holds:
        print(" KB entails the Query.")
    else:
        print(" KB does NOT entail the Query.")
    print("-" * 65)

# --- Query functions ---
def query_R(P, Q, R):
    return R

def query_P_implies_R(P, Q, R):
    return implies(P, R)

def query_Q_implies_R(P, Q, R):
    return implies(Q, R)

def query_P_and_Q(P, Q, R):
    return conj(P, Q)

# --- Run entailment checks ---
print("\nChecking Entailment for Query: R")
entails(evaluate_KB, query_R)

print("\nChecking Entailment for Query: P → R")
entails(evaluate_KB, query_P_implies_R)

print("\nChecking Entailment for Query: Q → R")
entails(evaluate_KB, query_Q_implies_R)

print("\nChecking Entailment for Query: P ∧ Q")
entails(evaluate_KB, query_P_and_Q)

