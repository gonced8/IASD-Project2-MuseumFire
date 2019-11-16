#!env/bin/python3

import probability


class Problem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        pass

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)

    def load_file(f):
        R = []
        C = []
        S = {}
        P = 0
        M = []

        '''
        for line in f.readlines():
            splitted = line.split()
            if not splitted:
                continue

            code = splitted[0]
            arg = splitted[1:]

            if code == 'A':
                d = {'start': arg[1], 'end': arg[2]}
                A[arg[0]] = d

            elif code == 'C':
                C[arg[0]] = arg[1]

            elif code == 'P':
                d = {"airplane": arg[0], "class": arg[1]}
                P.append(d)

            elif code == 'L':
                d = {"dep": arg[0], "arr": arg[1], "dl": arg[2]}
                d.update({ arg[i]: float(arg[i+1]) for i in range(3, len(arg), 2) })
                L.append(d)

        return A, C, P, L
        '''

def solver(input_file):
    return Problem(input_file).solve()

def read_argv():
    from sys import argv, exit
    if len(argv)==1:
        print(argv[0]+" <input file>")
        exit(0)
    else:
        return argv[1]


if __name__ == '__main__':
    in_filename = read_argv()
    
    with open(in_filename, 'r') as f:
        solver(f)
