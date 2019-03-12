from dataclasses import dataclass
from turtle import *
from typing import NamedTuple


class Module(NamedTuple):
    letter: str = ''
    parameter: list = []

class Production(NamedTuple):
    before: str = ''
    after: str = ''
    predecessor: Module = Module()
    condition: str = ''
    successor: str = ''

def match(p, m2):
    m1 = p.predecessor
    if m1.letter != m2.letter or len(m1.parameter) != len(m2.parameter):
        return False
    if len(m1.parameter) == 0 or p.condition == '*':
        return True
    return eval(p.condition, dict(zip(m1.parameter, [float(x) for x in m2.parameter])))

def string_to_module(rule):
    index = 0
    instruction = []
    while index < len(rule):
        if index + 1 != len(rule) and rule[index + 1] == '(':
            until = rule[index:].index(')') + index
            arguments = [item.strip() for item in rule[index + 2:until].split(',')]
            instruction.append(Module(rule[index], arguments))
            index = until + 1
        else:
            instruction.append(Module(rule[index]))
            index += 1
    return instruction

def replace(d, string):
    for k, v in d.items():
        string = string.replace(k, str(v))
    return string

class Rules(Turtle):

    def __init__(self, define, axiom, production):
        super(Rules, self).__init__()
        self.define = define
        axiom = replace(define, axiom)
        self.instruction = string_to_module(axiom)
        self.production = []
        for p in production:
            p = replace(define, p)
            a = p.split(':')
            module = a[0].strip()
            arguments = [item.strip() for item in module[module.find('(')+1:module.find(')')].split(',')]
            m = Module(module[0], arguments)
            b = a[1].split('->')
            condition = b[0].strip()
            succ = b[1].strip()
            p = Production(predecessor=m, condition=condition, successor=succ)
            self.production.append(p)

    def interpret(self):
        for i in self.instruction:
            if (i.letter == 'F'):
                super(Rules, self).set_pen(True)
                super(Rules, self).move(i.parameter[0])
            elif (i.letter == 'f'):
                super(Rules, self).set_pen(False)
                super(Rules, self).move(i.paramter[0])
            elif (i.letter == '+'):
                super(Rules, self).turn(i.parameter[0])
            elif (i.letter == '&'):
                super(Rules, self).pitch(i.parameter[0])
            elif (i.letter == '/'):
                super(Rules, self).roll(i.parameter[0])
            elif (i.letter == '['):
                super(Rules, self).save();
            elif (i.letter == ']'):
                super(Rules, self).restore();
            elif (i.letter == '!'):
                super(Rules, self).set_width(i.parameter[0])

    def generate(self, iteration):
        for i in range (iteration):
            final_instruct = [];
            for instruct in self.instruction:
                value = [x for x in self.production if match(x, instruct)]
                if (len(value) == 0):
                    final_instruct.append(instruct)
                else:
                    d = dict(zip(value[0].predecessor.parameter, [float(x) for x in instruct.parameter]))
                    module = string_to_module(value[0].successor)

                    for m in range(len(module)):
                        for p in range(len(module[m].parameter)):
                            module[m].parameter[p] = eval(module[m].parameter[p], d)
                    final_instruct.extend(module)

            self.instruction = final_instruct
        self.interpret()
