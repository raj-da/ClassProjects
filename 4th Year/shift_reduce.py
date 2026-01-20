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
        stack_str = "".join(self.stack)
        input_str = "".join(self.inputBuffer)
        print(f"{stack_str:<15} | {input_str:<15} | {action}")

    def can_reduce(self):
        for lhs, rhs_list in self.grammar.items():
            for rhs in rhs_list:
                if len(self.stack) >= len(rhs) and self.stack[-len(rhs):] == rhs:
                    return lhs, rhs

    def parse(self, inputString):
        print(f"{'STACK':<15} | {'INPUT':<15} | {'ACTION'}")
        print("-" * 50)
        
        self.inputBuffer = list(inputString)
        self.stack = []
        
        while True:
            reduce_rule = self.can_reduce()
            
            if reduce_rule:
                lhs, rhs = reduce_rule

                # pop from the stack
                for _ in range(len(rhs)):
                    self.stack.pop()

                self.stack.append(lhs)
                self.print_status(f"Reduce: {lhs} -> {''.join(rhs)}")
                
                # check for Success: 
                if self.stack == [self.startSymbole] and not self.inputBuffer:
                    print("-" * 50)
                    print("ACCEPTED")
                    return True

            # if we can't reduce try to SHIFT
            elif self.inputBuffer:
                token = self.inputBuffer.pop(0)
                self.stack.append(token)
                self.print_status(f"Shift")
                
            # if we can't shift nor reduce and not accepted then it's rejection
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
