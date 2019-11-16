#!env/bin/python3

import probability


class Problem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        R, C, S, P, M = self.load_file(fh)
        print('Rooms', '\n', R, '\n')
        print('Connections', '\n', C, '\n')
        print('Sensors', '\n', S, '\n')
        print('Probability', '\n', P, '\n')
        print('Measurement', '\n', M, '\n')

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        #return (room, likelihood)
        return

    def load_file(self, f):
        R = []
        C = []
        S = {}
        P = 0
        M = []

        for line in f.readlines():
            splitted = line.split()
            if not splitted:
                continue

            code = splitted[0]
            args = splitted[1:]

            if code == 'R':
                R.extend(args)

            elif code == 'C':
                C.extend([elem.split(',') for elem in args])

            elif code == 'S':
                for sensor in args:
                    data = sensor.split(':')
                    S[data[0]] = {'room': data[1], 'TPR': float(data[2]), 'FPR': float(data[3])}

            elif code == 'P':
                P = float(args[0])

            elif code == 'M':
                measurement = [{'sensor': sensor[0], 'measurement': str2bool(sensor[1])} for sensor in [elem.split(':') for elem in args]]
                M.append(measurement)

            else:
                print("Unrecognized line:", line)

        return R, C, S, P, M


def solver(input_file):
    return Problem(input_file).solve()

def read_argv():
    from sys import argv, exit
    if len(argv)==1:
        print(argv[0]+" <input file>")
        exit(0)
    else:
        return argv[1]

def str2bool(string):
    """Converts a string to a boolean

    Parameters:
    -----------
    string : string
    """
    return string.lower() in ("yes", "y", "true", "t", "1")


if __name__ == '__main__':
    in_filename = read_argv()
    
    with open(in_filename, 'r') as f:
        solver(f)
