from itertools import combinations

def get_literals(clause):
    """Split a clause into literals (handles OR operator)."""
    return [literal.strip() for literal in clause.split("OR")]

def negate_literal(literal):
    """Return the negation of a literal."""
    literal = literal.strip()
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal

def resolve(ci, cj):
    """Try to resolve two clauses and return resolvents."""
    resolvents = set()
    lits_i = get_literals(ci)
    lits_j = get_literals(cj)
   
    for li in lits_i:
        for lj in lits_j:
            if li == negate_literal(lj):
                new_clause = set(lits_i + lits_j)
                new_clause.discard(li)
                new_clause.discard(lj)
                if not new_clause:
                    resolvents.add("NIL")
                else:
                    resolvents.add(" OR ".join(sorted(new_clause)))
    return resolvents


def resolution_algorithm(kb, query):
    print("\n========== RESOLUTION IN FIRST ORDER LOGIC ==========\n")
   
    # Negate the query and add it to KB
    negated_query = negate_literal(query)
    print(f"Original Query     : {query}")
    print(f"Negated Query      : {negated_query}")
    clauses = kb + [negated_query]
    print("\nInitial Knowledge Base:")
    for i, c in enumerate(clauses, 1):
        print(f"  Clause {i}: {c}")

    print("\n========== Resolution Steps ==========\n")
    new = set()
    step = 1
    while True:
        pairs = list(combinations(clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for res in resolvents:
                if res == "NIL":
                    print(f"Step {step}: Resolving [{ci}] and [{cj}] gives NIL ⇒ Contradiction found!")
                    print("\n✅ Query is PROVED by Resolution.\n")
                    return True
                if res not in clauses and res not in new:
                    print(f"Step {step}: Resolving [{ci}] and [{cj}] ⇒ New clause: {res}")
                    new.add(res)
                    step += 1
        if new.issubset(set(clauses)):
            print("\n❌ No new clauses can be generated.")
            print("Query CANNOT be proved by Resolution.\n")
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)


# -------------------------
# Main Program (User Input)
# -------------------------

if __name__ == "__main__":
    print("=== Resolution in First Order Logic (Simplified) ===")
    n = int(input("Enter number of clauses in Knowledge Base: "))
    kb = []
    for i in range(n):
        clause = input(f"Enter clause {i+1}: ").strip()
        kb.append(clause)

    query = input("Enter the query to prove: ").strip()

    # Run Resolution Algorithm
    resolution_algorithm(kb, query)
