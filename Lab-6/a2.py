# Truth Table Entailment Checker
# KB = { Q → P, P → ¬Q, Q ∨ R }

from itertools import product

# --- Helper logical functions ---
def implies(a, b):
    return (not a) or b

def neg(a):
    return not a

def disj(a, b):
    return a or b

def conj(a, b):
    return a and b


# --- Evaluate KB sentences for a given model ---
def evaluate_KB(Q, P, R):
    s1 = implies(Q, P) # Q → P
    s2 = implies(P, neg(Q)) # P → ¬Q
    s3 = disj(Q, R) # Q ∨ R
    KB_true = s1 and s2 and s3
    return s1, s2, s3, KB_true


# --- Main Entailment Checker ---
def entails(KB_eval_func, query_func):
    symbols = ['Q', 'P', 'R']
    print("Truth Table for KB and Query\n")
    print(f"{'Q':<3}{'P':<3}{'R':<3} | {'Q→P':<5} | {'P→¬Q':<6} | {'Q∨R':<5} | {'KB':<3} | {'Query':<8}")
    print("-" * 45)

    entailment_holds = True
    valid_models = []

    for Q, P, R in product([False, True], repeat=3):
        s1, s2, s3, KB_true = KB_eval_func(Q, P, R)
        query_val = query_func(Q, P, R)

        # Record models where KB is true
        if KB_true:
            valid_models.append((Q, P, R, query_val))
            if not query_val:
                entailment_holds = False

        print(f"{int(Q):<3}{int(P):<3}{int(R):<3}| {int(s1):<5} |{int(s2):<6} | {int(s3):<5} | {int(KB_true):<3}| {int(query_val):<8}")

    print("\nModels where KB is True:")
    for m in valid_models:
        print(f"Q={int(m[0])}, P={int(m[1])}, R={int(m[2])}, Query={int(m[3])}")

    print("\nResult:")
    if entailment_holds:
        print(" KB entails the Query.")
    else:
        print(" KB does NOT entail the Query.")
    print("-" * 45)


# --- Define Query Functions ---
def query_R(Q, P, R):
    return R

def query_R_implies_P(Q, P, R):
    return implies(R, P)

def query_Q_implies_R(Q, P, R):
    return implies(Q, R)


# --- Run all tests ---
print("\nChecking Entailment for Query: R")
entails(evaluate_KB, query_R)

print("\nChecking Entailment for Query: R → P")
entails(evaluate_KB, query_R_implies_P)

print("\nChecking Entailment for Query: Q → R")
entails(evaluate_KB, query_Q_implies_R)
