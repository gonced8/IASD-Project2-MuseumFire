import probability


class Problem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        R, C, S, P, M = self.load_file(fh)

        parents = self.get_parents(R, C)
        cond_prob = self.get_conditional_probabilities(R, P, parents)

        # Probability of fire
        P_F = 0.5
        self.bayes_net = self.create_bayes_net(R, S, M, parents, cond_prob, P_F)

        print('Rooms', '\n', R, '\n')
        print('Connections', '\n', C, '\n')
        print('Sensors', '\n', S, '\n')
        print('Probability', '\n', P, '\n')
        print('Measurement', '\n', M, '\n')
        print('Connections2', '\n', parents, '\n')
        print('Bayesian Network', '\n', self.bayes_net, '\n');

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        room = 'test'
        likelihood = 0
        return (room, likelihood)

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

    def get_parents(self, R, C):
        parents = {}

        for room in R:
            parents[room] = [room]

        for connection in C:
            parents[connection[0]].append(connection[1])
            parents[connection[1]].append(connection[0])

        return parents

    def get_conditional_probabilities(self, R, P, parents):
        from itertools import product

        cond_prob = {}

        for room in R:
            n = len(parents[room])
            table = list(product([False, True], repeat=n))
            
            half = 2**(n-1)
            prob = [P if i<half else 0 for i in range(len(table))]
            prob[0] = 0

            cond_prob[room] = dict(zip(table, prob))
    
        return cond_prob

    def create_bayes_net(self, R, S, M, parents, cond_prob, P_F):
        bayes_net = probability.BayesNet()

        # Initial nodes
        for room in R:
            bayes_net.add((room+'_0', '', P_F))

        # Add nodes of following timesteps
        for i in range(1, len(M)):
            # Add rooms nodes
            for room in R:
                # Getting parents name at step i-1
                parents_i = [parent+ f'_{i-1}' for parent in parents[room]]
                bayes_net.add((room, ' '.join(parents_i), cond_prob[room]))
                print((room, ' '.join(parents_i), cond_prob[room]))


        # Add measurements nodes
        for i, measurements in enumerate(M):
            for m in measurements:
                sensor = m['sensor']
                bayes_net.add((sensor+f'_{i}', \
                                S[sensor]['room']+f'_{i}', \
                                {False: S[sensor]['FPR'], True: S[sensor]['TPR']}))
        
        return bayes_net

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
