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
        elif rule[index] != ' ':
            instruction.append(Module(rule[index]))
            index += 1
        else:
            index += 1
    return instruction

def replace(d, string):
    for k, v in d.items():
        string = string.replace(k, str(v))
    return string

class Rules(Turtle):

    def __init__(self, define, axiom, production, coord, basis):
        super(Rules, self).__init__(coord, basis)
        self.define = define
        axiom = replace(define, axiom)
        self.instruction = string_to_module(axiom)
        self.production = []
        for p in production:
            p = replace(define, p)
            a = p.split(':')
            module = a[0].strip()
            arguments = [item.strip() for item in module[module.find('(')+1:module.find(')')].split(',')]
            if arguments[0] == '':
              arguments = []
            m = Module(module[0], arguments)
            b = a[1].split('->')
            condition = b[0].strip()
            #if condition has = sign, change it to == for python evaluation
            if condition.find('=') != -1:
                condition = condition.replace('=', '==')
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
            elif (i.letter == 'G'):
                super(Rules, self).move_polygone(i.parameter[0])
            elif (i.letter == '{'):
                super(Rules, self).save_polygone()
            elif (i.letter == '}'):
                super(Rules, self).restore_polygone()
            elif (i.letter == '.'):
                super(Rules, self).new_vertex()
            elif (i.letter == '~'):
                super(Rules, self).save_leaf()
            elif (i.letter == '#'):
                super(Rules, self).save_flower()
            elif (i.letter == '@'):
                super(Rules, self).save_fruit()


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

'''
rules = Rules({'LA':5, 'RA':1.15, 'LB':1.3,
               'RB':1.25, 'LC':3, 'RC':1.19},
               '[{A(0,0).}][{A(0,1).}]',
               ['A(t,d) : d=0 -> .G(LA,RA).[+(60)B(t)G(LC,RC,t).}][+(60)B(t){.]A(t+1,d)',
                'A(t,d) : d=1 -> .G(LA,RA).[+(-60)B(t)G(LC,RC,t).}][+(-60)B(t){.]A(t+1,d)',
                'B(t) : t>0 -> G(LB,RB)B(t-1)',
                'G(s,r) : * -> G(s*r,r)',
                'G(s,r,t) : t>1 -> G(s*r,r,t-1)'])
rules.generate(5)

print(len(rules.polygones))
print(len(rules.lines))
li = []
for l in rules.polygones:
    li.extend(l)
print(rules.polygones)
for l in rules.lines:
    one = li.index(l[0])
    two = li.index(l[1])
'''
