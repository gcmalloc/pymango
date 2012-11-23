import re
import sys
import inspect

class Program(object):
    WHITESPACE = re.compile('\s{1}')

    """docstring for Programm"""
    def __init__(self, f):
        super(Program, self).__init__()
        self.tokens = []
        self.label = {}

        self.pc = 0
        self.stack = []
        self.vars = {}
        self.array = []

        self.instructions = {}
        self.generate_instruction()
        self.parse_token(f)
        self.run()

    def generate_instruction(self):
        for i in filter(lambda f: f[0].startswith("in_"), inspect.getmembers(self, predicate=inspect.ismethod)):
            self.instructions[i[0][3:]]= i[1]

    def parse_token(self, file):
        with open(file) as fp:
            commented = False
            for i in fp.read().split():
                if i.startswith("/*"):
                    commented = True
                    continue
                if commented:
                    if i.endswith("*/"):
                        commented = False
                    continue
                if i:
                    if i[-1] == ':':
                        self.label[i.rstrip(':')] = len(self.tokens)
                    else:
                        self.tokens.append(i)

    def op(self, f):
        self.stack.append(f(self.stack.pop(), self.stack.pop()))

    def in_add(self):
        self.op(lambda a, b: a + b)

    def in_sub(self):
        self.op(lambda a, b: a - b)

    def in_xor(self):
        self.op(lambda a, b: a ^ b)

    def in_exit(self):
        exit(0)

    def in_call(self):
        next_pc = self.stack.pop()
        self.stack.append(self.pc)
        self.pc = next_pc

    def in_vstore(self):
        self.array[self.stack.pop()] = self.stack.pop()

    def in_vload(self):
        self.stack.append(self.array[self.stack.pop()])

    def in_store(self):
        self.vars[self.stack.pop()] = self.stack.pop()

    def in_load(self):
        self.stack.append(self.vars[self.stack.pop()])

    def in_jump(self):
        self.pc = self.stack.pop()

    def in_ifz(self):
        cond = self.stack.pop()
        true_j = self.stack.pop()
        false_j = self.stack.pop()
        if cond == 0:
            self.pc = true_j
        else:
            self.pc = false_j

    def in_ifg(self):
        cond = self.stack.pop()
        true = self.stack.pop()
        false = self.stack.pop()
        if cond > 0:
            self.pc = true
        else:
            self.pc = false

    def in_print_num(self):
        sys.stdout.write(self.stack.pop())

    def in_print_byte(self):
        self.print_num()

    def in_dup(self):
        value = self.stack.pop()
        self.stack.append(value)
        self.stack.append(value)

    def in_read_num(self):
        self.stack.append(int(input()))

    def next_token(self):
       actual_token = self.tokens[self.pc]
       self.pc = self.pc + 1
       return actual_token

    def run(self):
       #token is an instruction
       tok = self.next_token()
       instruction = self.instructions.get(tok)
       label = self.label.get(tok)
       variable = self.vars.get(tok)
       if instruction:
           print("found instruction " + str(instruction))
           instruction()
           print("pp : " +  str(self.pc))
       elif label:
           print("found label " + str(label))
           self.stack.append(label)
       elif variable:
           print("found variable " + str(variable))
           self.stack.append(vars[tok])
       else:
           print("found a int " + str(tok))
           #just push it goddammit
           try:
            self.stack.append(int(tok))
           except ValueError:
            self.stack.append(tok)
       self.run()



def main():
    Program(sys.argv[1])

if __name__ == '__main__':
    main()
