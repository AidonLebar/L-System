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
                        self.p_rules[rule[0]] = rule[1]
                else: # i rules
                    rule = l.split("=")
                    if(len(rule) == 2):
                        self.i_rules[rule[0]] = rule[1]
                    
    def step(self, count = 1):
        for i in range(count):
            s = ""
            for c in self.l_string:
                identity = True
                for k in self.p_rules.keys():
                    if c == k:
                        s += self.p_rules[k]
                        identity = False
                if(identity):
                    s += c                       
            self.l_string = s
