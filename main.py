import probability


class Problem:
    """A class used to represent the museum fire problem. It used a Baye network and the variable elimination algorithm of the AIMA repository (https://github.com/aimacode/aima-python)

    ...

    Attributes
    ----------
    bayes_net : probability.BayesNet
        A Bayesian network as implemented in the AIMA repository.
        This network will represent the museum fire problem.
    evidence: dictionary
        This dictionary will contain, the measurements/evidences in the format used by the AIMA repository.
        The keys are the sensor name and time instant and the values are the corresponding measurements.
    last_nodes: list
        A list containing the name of the last nodes.
        This is used when calling the elimination ask for the last nodes (corresponding to the last time instant).

    Methods
    -------
    __init__(fh)
        Initializes the problem using the file object fh. It creates the Bayes network.
    solve()
        Returns the solution room name and likelihood.
    load_file(f)
        From an open file f, reads each line and processes it, creating the problem input variables.
    get_parents(R, C).
        Returns a dictionary where the keys are the rooms names and the values are lists of connections (including a connection with itself). This facilitates the generation of the Bayes network.
    get_conditional_probabilities(R, P, parents).
        Returns a dictionary where the keys are the rooms names and the values are dictionaries of a truth table and the conditional probabilities of the rooms nodes. It is used to create the Bayes network.
    get_evidence(S, M)
        Returns a dictionary containing the measurements/evidences in the format used in solve().
    create_bayes_net(R, S, M, parents, cond_prob, P_F)
        Creates the Bayesian network for the museum fire problem, as implemented in the AIMA repository.
    """

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        R, C, S, P, M = self.load_file(fh)

        parents = self.get_parents(R, C)
        cond_prob = self.get_conditional_probabilities(R, P, parents)

        n = len(M)-1
        self.last_nodes = [room+f'@{n}' for room in R]
        self.evidence = self.get_evidence(S, M)

        # Probability of fire
        P_F = 0.5

        # Create Bayesian Network
        self.bayes_net = self.create_bayes_net(R, S, M, parents, cond_prob, P_F)

        '''
        print('Rooms', '\n', R, '\n')
        print('Connections', '\n', C, '\n')
        print('Sensors', '\n', S, '\n')
        print('Probability', '\n', P, '\n')
        print('Measurement', '\n', M, '\n')
        print('Connections2', '\n', parents, '\n')
        print('Bayesian Network', '\n', self.bayes_net, '\n');
        '''

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        '''
        results = {}

        for room in self.last_nodes:
            results[room] = probability.elimination_ask(room, self.evidence, self.bayes_net)
        '''

        results = {room.split('@')[0]: probability.elimination_ask(room, self.evidence, self.bayes_net) for room in self.last_nodes}
        
        '''
        print('Results')
        for room in results:
            room_name = room.split('@')[0]
            print(room_name, '\t', results[room].show_approx())
        '''
        
        room = max(results.keys(), key=(lambda room: results[room][True]))
        likelihood = results[room][True]
        #room = room.split('@')[0]

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
        # Initialize dictionary with room and list of connections (first connection is itself)
        parents = {room: [room] for room in R}

        for connection in C:
            parents[connection[0]].append(connection[1])
            parents[connection[1]].append(connection[0])

        return parents

    def get_conditional_probabilities(self, R, P, parents):
        from itertools import product

        # Initialize dictionary
        cond_prob = {room: 0 for room in R}

        for room in R:
            n = len(parents[room])
            table = list(product([False, True], repeat=n))
            
            half = 2**(n-1)
            prob = [P if i<half else 1 for i in range(len(table))]
            prob[0] = 0

            cond_prob[room] = dict(zip(table, prob))
    
        return cond_prob

    def get_evidence(self, S, M):
        '''
        evidence = {}
        
        for i, measurements in enumerate(M):
            for m in measurements:
                evidence[m['sensor']+f'@{i}'] = m['measurement']
        '''

        evidence = {m['sensor']+f'@{i}': m['measurement'] for i, measurements in enumerate(M) for m in measurements}

        return evidence

    def create_bayes_net(self, R, S, M, parents, cond_prob, P_F):
        bayes_net = probability.BayesNet()

        # Initial nodes
        for room in R:
            bayes_net.add((room+'@0', '', P_F))

        # Add nodes of following timesteps
        for i in range(1, len(M)):
            # Add rooms nodes
            for room in R:
                # Getting parents name at step i-1
                parents_i = [parent+f'@{i-1}' for parent in parents[room]]
                bayes_net.add((room+f'@{i}', ' '.join(parents_i), cond_prob[room]))

        # Add measurements nodes
        for i, measurements in enumerate(M):
            for m in measurements:
                sensor = m['sensor']
                bayes_net.add((sensor+f'@{i}', \
                               S[sensor]['room']+f'@{i}', \
                               {False: S[sensor]['FPR'], True: S[sensor]['TPR']}))
        
        return bayes_net

def solver(input_file):
    return Problem(input_file).solve()

def read_argv():
    from sys import argv, exit
    
    l = len(argv)

    if l==1:
        print(argv[0]+" <input file> <print>")
        exit(0)
    elif l==2:
        show = False
    else:
        show = str2bool(argv[2])

    in_filename = argv[1]

    return in_filename, show 

def get_out_filename(in_filename):
    """Receives a filename and returns the string "output/filename". Works in every operating system
    Parameters:
    -----------
    in_filename : string
        Filename to use
    Returns:
    --------
    out_filename : string
        Filename inside directory output
    """

    import os.path
    out_filename = os.path.basename(in_filename)
    out_filename = os.path.join('output', out_filename)
    return out_filename

def str2bool(string):
    """Converts a string to a boolean

    Parameters:
    -----------
    string : string
    """
    return string.lower() in ("yes", "y", "true", "t", "1")


if __name__ == '__main__':
    in_filename, show = read_argv()
    
    with open(in_filename, 'r') as f:
        sol = solver(f)

        if show:
            print('Solution', '\n', sol)

    out_filename = get_out_filename(in_filename)
    with open(out_filename, 'w') as f:
        f.write(f'{sol[0]} {sol[1]}')
        f.write('\n')
