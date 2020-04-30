from graphviz import Digraph


class Automata:

    def __init__(self, states, symbols, states_list, symbols_list, start_state, end_states, lambda_closures, lnfa):
        self.states = states
        self.symbols = symbols
        self.states_list = states_list
        self.symbols_list = symbols_list
        self.start_state = start_state
        self.end_states = end_states
        self.lambda_closures = lambda_closures
        self.lnfa = lnfa

    def closure(self, i, a):
        if self.lnfa[a][symbols - 1] != "-" and len(self.lambda_closures[states_list[i]]) < states:
            for x in self.lnfa[a][symbols - 1]:
                if x not in self.lambda_closures[states_list[i]]:
                    self.lambda_closures[states_list[i]].add(x)
                    self.closure(i, states_list.index(x))
                else:
                    continue
        return

    def lnfa_to_dfa(self):
        print("The lambda-NFA statements: ")
        print(states_list)
        print(" \n The symbols: ")
        print(symbols_list)

        self.lnfa = []
        for i in range(states):
            self.lnfa.append(f.readline().split())

        # ----------------------------------------

        # AFISARE
        print("\nThe lambda-NFA table: \n")
        print("States |", *symbols_list, sep='\t')
        print("--------------------------------")
        for i in range(states):
            print(states_list[i] + "      | ", *self.lnfa[i], sep='\t')
        print()
        print("=========================================================")
        # -------------------------------------------------------------

        # lambda closures

        for i in range(states):
            lambda_closures[states_list[i]] = set()
            lambda_closures[states_list[i]].add(states_list[i])

        for i in range(states):
            self.closure(i, i)

        print("\n The lambda-closures: ")
        print(lambda_closures)

        # ---------------------------------------------------------

        # primele n linii ale tabelului

        table = [[set() for j in range(symbols - 1)] for i in range(states)]

        for i in range(states):
            for j in range(symbols - 1):
                adiacent = set()
                for x in lambda_closures[states_list[i]]:
                    if self.lnfa[states_list.index(x)][j] != "-":
                        for k in self.lnfa[states_list.index(x)][j]:
                            adiacent.add(k)
                # print(adiacent)
                new = set()
                for x in adiacent:
                    new = new.union(lambda_closures[x])
                # print(new)
                # print("\n")
                for x in new:
                    table[i][j].add(x)

        symbols_list.pop()
        print()
        print("The intermediate table:")
        print("States |", *symbols_list, sep='                   ')
        print("-------------------------------------------------------------------------------------------")
        for i in range(states):
            print(states_list[i] + "      | ", *table[i], sep='\t')
        print()
        # ------------------------------------------

        # dfa

        dfa = [[]]
        new_states = []
        new_start_state = lambda_closures[start_state]
        new_end_states = []
        current = []

        # print(start_state)
        # print(lambda_closures[start_state])

        new_states.append(lambda_closures[start_state])  # nodul de start

        for i in range(symbols - 1):
            aux = set()
            for x in lambda_closures[start_state]:
                aux = aux.union(table[states_list.index(x)][i])
            if aux != lambda_closures[start_state]:
                dfa[0].append(aux)
                if len(aux) > 0:
                    current.append(aux)
                    new_states.append(aux)
                    # print(aux)

        print("=======================")

        j = 0
        while len(current) > 0:
            j += 1
            dfa.append([])
            for i in range(symbols - 1):
                aux = set()
                # print(current[0])
                for x in current[0]:
                    aux = aux.union(table[states_list.index(x)][i])
                dfa[j].append(aux)
                if aux not in new_states and len(aux) > 0:
                    new_states.append(aux)
                    current.append(aux)
            current.pop(0)

        for x in new_states:
            for y in x:
                if y in end_states:
                    new_end_states.append(x)

        # ----------------------------------------------------------------------



        # Afisare

        print()

        print("THE DFA IS:  ")
        print("New States                       |", *symbols_list, sep='                   ')
        print("-------------------------------------------------------------------------------------------")

        for i in range(j + 1):
            print(new_states[i], "  ->  ", end="")
            print(*dfa[i], sep="      ")

        print()
        print("The start state:  ", new_start_state)
        print("The end states:   ", *new_end_states)
        print()
        print(new_states)
        print(end_states)
        # Grafica

        g = Digraph('DFA', filename='fsm.gv')
        g.attr(rankdir='LR', size='10')
        if new_start_state not in new_end_states:
            g.attr('node', shape='circle', fillcolor="green", style="filled")
            g.node(str(new_states.index(new_start_state)))
        else:
            g.attr('node', shape='doublecircle', fillcolor="green", style="filled")
            g.node(str(new_states.index(new_start_state)))

        g.attr('node', shape='doublecircle', fillcolor="red", style="filled")
        for o in new_end_states:
            g.node(str(new_states.index(o)))

        g.attr('node', shape='circle', fillcolor="white", style="filled")
        for x in new_states:
            if x not in new_end_states and x != new_start_state:
                g.node(str(new_states.index(x)))

        for i in range(j + 1):
            for x in range(len(symbols_list)):
                if dfa[i][x] != set():
                    g.edge(str(i), str(new_states.index(dfa[i][x])), label=symbols_list[x], color="blue", style="filled")

        g.view()

        # -----------------------------------------------------------------------------

# citire


f = open("ex3.txt")

states = int(f.readline())
symbols = int(f.readline())

states_list = f.readline().split()
symbols_list = f.readline().split()


start_state = f.readline()[0]
end_states = f.readline().split()

lambda_closures = dict()
lnfa = []

automat = Automata(states, symbols, states_list, symbols_list, start_state, end_states, lambda_closures, lnfa)

automat.lnfa_to_dfa()
