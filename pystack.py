import re
import sys

class Program(object):
    WHITESPACE = re.compile('\s{1}')

    """docstring for Programm"""
    def __init__(self, f):
        super(Program, self).__init__()
        self.tokens = []
        self.label = {}

        self.pc= 0
        self.stack = []

        self.instructions = {}
        self.parse_token(f)
        print(self.tokens)
        print(self.label)

    def add(self):
        self.stack.append(self.stack.pop() + self.stack.pop())

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

    def next(self):
       actual_token = self.token[self.pc]
       self.pc += 1
       return actual_token

    def execute(self, token):
       #token is an instruction
       self.instructions.get(token)



def main():
    Program(sys.argv[1])

if __name__ == '__main__':
    main()
