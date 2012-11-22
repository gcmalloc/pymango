class Program(object):
    WHITESPACE = re.compile('\s')

    """docstring for Programm"""
    def __init__(self, f):
        super(Programm, self).__init__()
        self.tokens = []
        self.label = {}

        self.pc= 0
        self.stack = []

        self.instructions = {}
        self.parse_token(f)

   def parse_token(self, file):
        with file.open() as fp:
            for i in fp.read().split(WHITESPACE):
                if i:
                    if i.endWith(':'):
                        self.label[i.rstrip(':')] = len(self.tokens) - 1
                    else:
                        self.tokens.push(i)

   def next(self):
       actual_token = self.token[self.pc]
       self.pc += 1
       return actual_token

   def execute(self, token):
       #token is an instruction
       self.instructions.get(token)]



def main():
    Program(sys.argv[1])

if __name__ == '__main__':
    main()
