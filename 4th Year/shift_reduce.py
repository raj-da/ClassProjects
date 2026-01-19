# Representation:
# Grammar:
#...... a grammar is represented using a dictionary where keys are left hand side and values are list of right hand side
#....... Example:
#............ E -> E + E
#............ E -> E * E
#............ E -> id
#....... Representation: {'E': [['E', '+', 'E'], ['id']]}




class ShiftReduceParser:
    def __init__(self, grammar, startSymbole):
        
        self.grammar = grammar
        self.startSymbole = startSymbole
        self.stack = []
        self.inputBuffer = []

    def print_status(self, action):
        """Helper to print the current state in a tabular format."""
        stack_str = "".join(self.stack)
        input_str = "".join(self.inputBuffer)
        print(f"{stack_str:<15} | {input_str:<15} | {action}")

    def can_reduce(self):
        """
        Checks if the top of the stack matches any RHS in the grammar.
        Returns the (LHS, RHS) tuple if a match is found, otherwise None.
        """
        # Iterate through every rule in the grammar
        for lhs, rhs_list in self.grammar.items():
            for rhs in rhs_list:
                # Check if the stack ends with this RHS
                # We slice the stack to the length of the RHS
                if len(self.stack) >= len(rhs) and self.stack[-len(rhs):] == rhs:
                    return lhs, rhs

    def parse(self, input_string):
        """
        Main parsing loop.
        input_string: A list of tokens, e.g., ['id', '+', 'id']
        """
        print(f"{'STACK':<15} | {'INPUT':<15} | {'ACTION'}")
        print("-" * 50)
        
        # Initialize buffer
        self.inputBuffer = list(input_string)
        self.stack = []
        
        while True:
            # 1. Try to REDUCE first
            # We prioritize reduce to see if we can collapse the stack
            reduce_rule = self.can_reduce()
            
            if reduce_rule:
                lhs, rhs = reduce_rule
                # Pop the RHS from the stack
                for _ in range(len(rhs)):
                    self.stack.pop()
                # Push the LHS onto the stack
                self.stack.append(lhs)
                self.print_status(f"Reduce: {lhs} -> {''.join(rhs)}")
                
                # Check for Success: 
                # Stack has only start symbol AND input is empty
                if self.stack == [self.startSymbole] and not self.inputBuffer:
                    print("-" * 50)
                    print("ACCEPTED")
                    return True

            # 2. If we cannot reduce, try to SHIFT
            elif self.inputBuffer:
                token = self.inputBuffer.pop(0)
                self.stack.append(token)
                self.print_status(f"Shift")
                
            # 3. If we can neither shift nor reduce, and not accepted -> Error
            else:
                print("-" * 50)
                print("REJECTED (Syntax Error or Conflict)")
                return False

grammar = {
    "E": [["E", "+", "E"], ["E", "*", "E"], ["id"]]
}

_input = ["id", "+", "id", "*", "id"]

parser = ShiftReduceParser(grammar, startSymbole="E")
parser.parse(_input)
