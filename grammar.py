import re
import random

class grammar:
    axiom = ""
    l_string = ""
    #production and interpretation rules
    p_rules = {}
    i_rules = {}

    def parse(self, filename):
        with open(filename) as f:
            data = f.readlines()
            data = [x.strip() for x in data] 
            self.axiom =  data[0]
            self.l_string = self.axiom
            data = data[2:]
            p = True
            for l in data:
                if l == "###":
                    p = False
                    continue
                if p: #p rules
                    rule = l.split("->") 
                    if(len(rule) == 2):
                        if re.search( "\(.*\)", rule[0]):
                            prob = re.search(r"\(.*\)", rule[0]).group()
                            prob = float(re.sub(r"[\(\)]", "", prob))
                            if prob < 0 or prob > 1:
                                print("Probability must be between 0 and 1.")
                                exit()
                            lhs = re.sub(r"\(.*\)", "", rule[0])
                            if len(rule[1].split(":")) != 2:
                                print("Incorrect # of oucomes for binary stochastic production rule.")
                                exit()
                            rhs = [prob] + (rule[1].split(":"))
                            self.p_rules[lhs] = rhs
                        else:
                            self.p_rules[rule[0]] = [1.0, rule[1], ""] #apply with 100% prob
                else: # i rules
                    rule = l.split("=")
                    if(len(rule) == 2):
                        instr = ""
                        params = []
                        if re.search( "\(.*\)", rule[1]):
                            r = rule[1].split("(")
                            instr = r[0]
                            s = ""
                            for c in r[1]:
                                if c == " ":
                                    continue
                                elif c == ")":
                                    params.append(s)
                                    break
                                elif c == ",":
                                    params.append(s)
                                    s = ""
                                else:
                                    s += c
                        else:
                            instr = rule[1]
                        self.i_rules[rule[0]] = [instr, params]
                    
    def step(self, count = 1):
        for i in range(count):
            s = ""
            for c in self.l_string:
                identity = True
                for k in self.p_rules.keys():
                    if c == k:
                        rand = random.uniform(0,1)
                        if rand < self.p_rules[k][0]:
                            s += self.p_rules[k][1]
                        else:
                            s += self.p_rules[k][2]
                        identity = False
                if(identity):
                    s += c                       
            self.l_string = s
