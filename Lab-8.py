import re

# --- Helper Functions ---
def isVariable(x):
    """Check if a symbol is a variable (lowercase single letter)."""
    return len(x) == 1 and x.islower() and x.isalpha()

def getAttributes(string):
    """Extract the list of attributes inside parentheses."""
    expr = r'\([^)]+\)'
    matches = re.findall(expr, string)
    return matches

def getPredicates(string):
    """Extract predicates (function names) from the expression."""
    expr = r'([a-z~]+)\([^&|]+\)'
    return re.findall(expr, string)


# --- Fact Class ---
class Fact:
    def __init__(self, expression):
        self.expression = expression.strip()
        predicate, params = self.splitExpression(expression)
        self.predicate = predicate
        self.params = params
        self.result = any(self.getConstants())

    def splitExpression(self, expression):
        predicate = getPredicates(expression)[0]
        params = getAttributes(expression)[0].strip('()').split(',')
        return [predicate, params]

    def getResult(self):
        return self.result

    def getConstants(self):
        """Return constants in the fact (None for variables)."""
        return [None if isVariable(c) else c for c in self.params]

    def getVariables(self):
        """Return variables in the fact (None for constants)."""
        return [v if isVariable(v) else None for v in self.params]

    def substitute(self, constants):
        """Substitute variables with constants."""
        c = constants.copy()
        f = f"{self.predicate}(" + ",".join(
            [c.pop(0) if isVariable(p) else p for p in self.params]
        ) + ")"
        return Fact(f)


# --- Implication Class ---
class Implication:
    def __init__(self, expression):
        self.expression = expression.strip()
        l = expression.split('=>')
        self.lhs = [Fact(f.strip()) for f in l[0].split('&')]
        self.rhs = Fact(l[1].strip())

    def evaluate(self, facts):
        """Try to infer a new fact based on existing facts."""
        constants = {}
        new_lhs = []

        for fact in facts:
            for val in self.lhs:
                if val.predicate == fact.predicate:
                    for i, v in enumerate(val.getVariables()):
                        if v:
                            constants[v] = fact.getConstants()[i]
                    new_lhs.append(fact)

        predicate = getPredicates(self.rhs.expression)[0]
        attributes = str(getAttributes(self.rhs.expression)[0])

        # Apply constant substitutions
        for key in constants:
            if constants[key]:
                attributes = attributes.replace(key, constants[key])

        expr = f'{predicate}{attributes}'
        return Fact(expr) if len(new_lhs) and all([f.getResult() for f in new_lhs]) else None


# --- Knowledge Base Class ---
class KB:
    def __init__(self):
        self.facts = set()
        self.implications = set()

    def tell(self, e):
        """Add a new fact or rule to the KB."""
        if '=>' in e:
            self.implications.add(Implication(e))
        else:
            self.facts.add(Fact(e))

        # Forward chain: evaluate all implications with current facts
        for i in self.implications:
            res = i.evaluate(self.facts)
            if res:
                self.facts.add(res)

    def ask(self, e):
        """Query the KB for a predicate."""
        facts = set([f.expression for f in self.facts])
        i = 1
        print(f'\nQuerying {e}:')
        for f in facts:
            if Fact(f).predicate == Fact(e).predicate:
                print(f'\t{i}. {f}')
                i += 1
        if i == 1:
            print("\tNo matching facts found.")

    def display(self):
        """Display all facts in the KB."""
        print("\nAll facts in the KB:")
        for i, f in enumerate(set([f.expression for f in self.facts])):
            print(f'\t{i+1}. {f}')


# --- Main Function ---
def main():
    kb = KB()
    print("Enter the number of FOL expressions present in KB:")
    n = int(input().strip())

    print("Enter the expressions:")
    for i in range(n):
        fact = input().strip()
        kb.tell(fact)

    print("Enter the query:")
    query = input().strip()
    kb.ask(query)
    kb.display()


if __name__ == "__main__":
    main()
