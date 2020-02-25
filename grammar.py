import re
import random

class PRule:
    symbol = ""
    rewrite1 = ""
    rewrite2 = ""
    prob = 0

    def error_out(self, reason):
        if self.prob != 1:
            print("Error in rule {}({})->{}:{}".format(self.symbol,
                                                       self.prob,
                                                       self.rewrite1,
                                                       self.rewrite2))
        else:
            print("Error in rule {}->{}".format(self.symbol, self.rewrite1))
        print("Reason: {}".format(reason))
        exit()

    def __str__(self):
        if self.prob != 1:
            return "{}({})->{}:{}".format(self.symbol,
                                          self.prob,
                                          self.rewrite1,
                                          self.rewrite2)
        else:
           return "{}->{}".format(self.symbol, self.rewrite1)

class IRule:
    symbol = ""
    action = ""
    param_count = 0
    params = []

    def __init__(self):
        self.params = []

    def error_out(self, reason):
        if self.param_count != 0:
            param_string = ", ".join([str(x) for x in self.params])
            print("Error in rule {}={}({})".format(self.symbol,
                                                   self.action,
                                                   param_string))
        else:
            print("Error in rule {}={}".format(self.symbol, self.action))
        print("Reason: {}".format(reason))
        exit()

    def __str__(self):
        if self.param_count != 0:
            param_string = ", ".join([str(x) for x in self.params])
            return "{}={}({})".format(self.symbol,
                                      self.action,
                                      param_string)
        else:
            return "{}={}".format(self.symbol, self.action)

class Grammar:
    axiom = ""
    l_string = ""
    generations = []
    #production and interpretation rules
    p_rules = []
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
                    p_rule = PRule()
                    rule = l.split("->") 
                    if(len(rule) == 2):
                        if re.search( "\(.*\)", rule[0]):
                            prob = re.search(r"\(.*\)", rule[0]).group()
                            prob = float(re.sub(r"[\(\)]", "", prob))
                            p_rule.prob = prob
                            p_rule.symbol =  re.sub(r"\(.*\)", "", rule[0])
                            if len(rule[1].split(":")) != 2:
                                print("Error in rule {}({})->{}".format(p_rule.symbol,
                                                                        p_rule.prob,
                                                                        rule[1]))
                                print("Reason: Incorrect # of outcomes provided.")
                                exit()
                            else:
                                rhs = rule[1].split(":")
                                p_rule.rewrite1 = rhs[0]
                                p_rule.rewrite2 = rhs[1]
                                if p_rule.prob < 0 or p_rule.prob > 1:
                                    p_rule.error_out("Probability must be between 0 and 1.")
                        else:
                            p_rule.prob = 1
                            p_rule.symbol = rule[0]
                            p_rule.rewrite1 = rule[1]
                        self.p_rules.append(p_rule)
                else: # i rules
                    i_rule = IRule()
                    rule = l.split("=")
                    if(len(rule) == 2):
                        if re.search( "\(.*\)", rule[1]):
                            r = rule[1].split("(")
                            i_rule.action = r[0]
                            s = ""
                            for c in r[1]:
                                if c == " ":
                                    continue
                                elif c == ")":
                                    i_rule.params.append(s)
                                    i_rule.param_count += 1
                                    break
                                elif c == ",":
                                    i_rule.params.append(s)
                                    i_rule.param_count += 1
                                    s = ""
                                else:
                                    s += c
                        else:
                            i_rule.action = rule[1]
                        i_rule.symbol = rule[0]
                        self.i_rules[i_rule.symbol] = i_rule
    def step(self, count = 1):
        for i in range(count):
            s = ""
            for c in self.l_string:
                identity = True
                for p in self.p_rules:
                    if c == p.symbol:
                        rand = random.uniform(0,1)
                        if rand < p.prob:
                            s += p.rewrite1
                        else:
                            s += p.rewrite2
                        identity = False
                if(identity):
                    s += c                       
            self.l_string = s

    def setup(self, count = 12):
        for i in range(count):
            self.step()
            self.generations.append(self.l_string)

    def set_gen(self, gen):
        if gen < 0:
            gen = 0
        if gen >= len(self.generations):
            gen = len(self.generations) - 1
        self.l_string = self.generations[gen]
            
