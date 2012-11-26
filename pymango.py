import re
import sys
import inspect
import logging
from collections import namedtuple
Var = namedtuple('Var', ['name', 'value'])

class Mango(object):
    WHITESPACE = re.compile('\s{1}')

    """docstring for Programm"""
    def __init__(self, f):
        self.tokens = []
        self.label = {}

        self.pc = 0
        self.stack = []
        self.vars_ = {}
        self.array = {}

        self.instructions = {}
        self.generate_instruction()
        self.parse_token(f)
        while 1:
            self.run()

    def generate_instruction(self):
        for i in filter(lambda f: f[0].startswith("in_"), inspect.getmembers(self, predicate=inspect.ismethod)):
            self.instructions[i[0][3:]]= i[1]

    def parse_token(self, file):
        with open(file) as fp:
            commented = False
            for i in fp.read().split():
                if i.startswith("/*"):
                    commented += 1
                    continue
                if commented:
                    if i.endswith("*/"):
                        commented -= 1
                    continue
                if i:
                    if i[-1] == ':':
                        self.label[i.rstrip(':').strip()] = len(self.tokens)
                    else:
                        self.tokens.append(i.strip())

    def op(self, f):
        self.stack.append(f(self.pop(), self.pop()))

    def in_mod(self):
        self.op(lambda a, b: b % a)

    def in_add(self):
        self.op(lambda a, b: a + b)

    def in_sub(self):
        self.op(lambda a, b: b - a)

    def in_xor(self):
        self.op(lambda a, b: b ^ a)

    def in_exit(self):
        exit(0)

    def in_call(self):
        next_pc = self.stack.pop()
        self.stack.append(self.pc)
        self.pc = next_pc

    def in_vstore(self):
        self.array[self.pop()] = self.pop()

    def in_vload(self):
        self.stack.append(self.array[self.pop()])

    def in_store(self):
        name = self.stack.pop()
        value = self.pop()
        self.vars_[name.name] = value

    def in_load(self):
        self.stack.append(self.vars_[self.stack.pop()])

    def in_jump(self):
        self.pc = self.pop()

    def branch(self, f):
        false_j = self.pop()
        true_j = self.pop()
        cond = self.pop()
        if f(cond):
            #true we take the upper one
            self.pc = true_j
        else:
            #false we take the lower one
            self.pc = false_j

    def in_ifz(self):
        self.branch(lambda a: a == 0)

    def in_ifg(self):
        self.branch(lambda a: a > 0)

    def in_print_num(self):
        sys.stdout.write(str(self.pop()))

    def in_print_byte(self):
        sys.stdout.write(chr(self.stack.pop()))

    def in_dup(self):
        value = self.stack.pop()
        self.stack.append(value)
        self.stack.append(value)

    def in_read_num(self):
        self.stack.append(int(input()))

    def in_read_byte(self):
        self.in_read_num()

    def pop(self):
        top_token = self.stack.pop()
        try:
            return int(top_token)
        except (ValueError, TypeError):
            return top_token.value

    def next_token(self):
       actual_token = self.tokens[self.pc]
       self.pc = self.pc + 1
       return actual_token

    def run(self):
       logging.debug("stack is")
       logging.debug(self.stack)
       logging.debug("vars are")
       logging.debug(self.vars_.keys())
       logging.debug(self.vars_)
       logging.debug("array is ")
       logging.debug(self.array)
       logging.debug("+" * 60)
       logging.debug("pp : " +  str(self.pc))
       #token is an instruction
       tok = self.next_token()
       instruction = self.instructions.get(tok)
       label = self.label.get(tok)
       if instruction:
           logging.debug("found instruction " + str(instruction))
           instruction()
       elif label:
           logging.debug("found label " + str(label))
           self.stack.append(label)
       else:
           logging.debug("found a int " + str(tok))
           #just push it goddammit
           try:
            self.stack.append(int(tok))
           except ValueError:
            self.stack.append(Var(tok, self.vars_.get(tok)))

if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.DEBUG)
    Mango(sys.argv[1])
