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
    filename = read_argv()

    print(filename)
