#!/usr/bin/python

"""
Referenced from: http://d.hatena.ne.jp/fuyumi3/20110910/1315659503
"""
import sys

class Brainfuck():
    class ProgramError(StandardError): pass
    def __init__(self, src):
        self._tokens = src
        self._jumps = self._analyze_jumps(self._tokens)

    def run(self):
        tape = []
        pc = 0
        cur = 0

        while pc < len(self._tokens):
            if cur >= len(tape):
                tape.append(0)
            if self._tokens[pc] == '+':
                tape[cur] += 1      # (*ptr)++;
            elif self._tokens[pc] == '-':
                tape[cur] -= 1      # (*ptr)--;
            elif self._tokens[pc] == '>':
                cur += 1            # ptr++;
            elif self._tokens[pc] == '<':
                cur -= 1            # ptr--;
                if cur < 0: raise self.ProgramError("ptr can't be decremented anymore")
            elif self._tokens[pc] == '.':
                #print chr(tape[cur]),   # putchar(*ptr);
                sys.stdout.write(chr(tape[cur]))
            elif self._tokens[pc] == ',':
                tape[cur] = ord(raw_input().strip())    # *ptr = getchar();
            elif self._tokens[pc] == '[':
                if tape[cur]== 0:
                    pc = self._jumps[pc]        #while(*ptr){
            elif self._tokens[pc] == ']':
                if tape[cur] != 0:
                    pc = self._jumps[pc]        #}
            pc += 1

    def _analyze_jumps(self, tokens):
        jumps = {}
        starts = []

        for i, c in enumerate(tokens):
            if c == '[':
                starts.append(i)
            elif c == ']':
                if not starts: raise self.ProgramError("too much ']'")
                frm = starts.pop()
                to = i

                jumps[frm] = to
                jumps[to] = frm
        if starts: raise ProgramError("too much '['")
        return jumps


try:
    src = open(sys.argv[1]).read()
except IOError:
    src = sys.argv[1]
except IndexError:
    src = raw_input()

try:
    Brainfuck(src).run()
except Brainfuck.ProgramError:
    print "Failed to run"
