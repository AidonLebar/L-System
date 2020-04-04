import re
import random

class PRule:
    symbol = ""
    rewrite1 = ""
    rewrite2 = ""
    pre = ""
    post = ""
    prob = 0

    def error_out(self, reason):
        print("Error in rule {}".format(self))
        print("Reason: {}".format(reason))
        exit()

    def match(self, str, index):
        pre = str[index - len(self.pre) : index]
        post = str[index + 1 : index + len(self.post) + 1]
        if pre == self.pre and post == self.post:
            return True
        else:
            return False

    def __str__(self):
        if self.prob != 1:
            return "{}({})->{}:{}".format(self.symbol,
                                          self.prob,
                                          self.rewrite1,
                                          self.rewrite2)
        elif self.pre or self.post:
            return "{}<{}>{}->{}".format(self.pre,
                                         self.symbol,
                                         self.post,
                                         self.rewrite1)
        else:
           return "{}->{}".format(self.symbol, self.rewrite1)
    def __repr__(self):
        return self.__str__()


class IRule:
    symbol = ""
    action = ""
    param_count = 0
    params = []

    def __init__(self):
        self.params = []

    def error_out(self, reason):
        print("Error in rule {}".format(self))
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
                    p_rule = PRule()
                    rule = l.split("->") 
                    if(len(rule) == 2):
                        if re.search(".*\<.*\>.*", rule[0]):
                            p_rule = self.parse_context_senstive_PRule(rule)
                        elif re.search( "\(.*\)", rule[0]):
                            p_rule = self.parse_stochastic_PRule(rule)
                        else:
                            p_rule.prob = 1
                            p_rule.symbol = rule[0]
                            p_rule.rewrite1 = rule[1]
                        if p_rule.symbol in self.p_rules:
                            self.p_rules[p_rule.symbol].append(p_rule)
                        else:
                            self.p_rules[p_rule.symbol] = [p_rule]
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
            for symbol in self.p_rules:
                self.p_rules[symbol].sort(key = lambda p_rule: len(p_rule.pre) + len(p_rule.post))

    def step(self, count = 1):
        for i in range(count):
            s = ""
            for n,c in enumerate(self.l_string):
                if c in self.p_rules:
                    p = self.p_rules[c]
                    rand = random.uniform(0,1)
                    r = PRule()
                    for rule in p: #use last longest matching context
                        if rule.match(self.l_string, n):
                            r = rule
                    if rand < r.prob:
                        s += r.rewrite1
                    else:
                        s += r.rewrite2
                else:
                    s += c
            self.l_string = s

    def setup(self, count = 12):
        self.generations.append(self.axiom)
        for i in range(count):
            self.step()
            self.generations.append(self.l_string)

    def set_gen(self, gen):
        if gen < 0:
            gen = 0
        if gen >= len(self.generations):
            gen = len(self.generations) - 1
        self.l_string = self.generations[gen]

    def parse_context_senstive_PRule(self, rule):
        p_rule = PRule()
        temp = rule[0].split("<")
        p_rule.pre = temp[0]
        temp2 = temp[1].split(">")
        p_rule.symbol = temp2[0]
        p_rule.post = temp2[1]
        p_rule.rewrite1 = rule[1]
        p_rule.prob = 1
        if len(temp2[0]) != 1:
            p_rule.error_out("Only one symbol allowed in < >")
        return p_rule

    def parse_stochastic_PRule(self, rule):
        p_rule = PRule()
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
        return p_rule
