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
        """Reads the opened file object fh and creates a Bayesian network accordingly to the museum fire problem.
        The Bayesian network with the class probability.BayesNet from the AIMA repository.
        Initializes the attributes: last_nodes, evidence and bayes_net.

        ...

        Parameters
        ----------
        fh : file
            Opened file object to be used as input for the museum fire problem.
        """

        # Reads the file and loads its data into variables
        R, C, S, P, M = self.load_file(fh)

        # Get a dictionary containing the parents of each node
        parents = self.get_parents(R, C)

        # Get a dictionary containing the conditional probabilities tables from the room nodes
        cond_prob = self.get_conditional_probabilities(R, P, parents)

        # Get a dictiionary containing the evidence/measurements in the format used by the elimination_ask()
        self.evidence = self.get_evidence(S, M)

        # Name of the room nodes at the last instant
        n = len(M)-1
        self.last_nodes = [room+f'@{n}' for room in R]

        # Probability of fire
        P_F = 0.5

        # Create Bayesian Network
        self.bayes_net = self.create_bayes_net(R, S, M, parents, cond_prob, P_F)

        '''
        # Print the created variables
        print('Rooms', '\n', R, '\n')
        print('Connections', '\n', C, '\n')
        print('Sensors', '\n', S, '\n')
        print('Probability', '\n', P, '\n')
        print('Measurement', '\n', M, '\n')
        print('Connections2', '\n', parents, '\n')
        print('Bayesian Network', '\n', self.bayes_net, '\n');
        '''

    def solve(self):
        """Solve the museum fire problem, that is, which room at the last time instant is more likely to be on fire.
        The solution if obtained using the algorithm probability.elimination_ask() from the AIMA repository.

        Returns
        -------
        (room, likelihood) : tuple
            The element room is a string containing the room name.
            The element likelihood is a a float which value is the probablity to be on fire.
        """
        
        # Calculate the probability of fire for each room in the final time instant. Store the results in a dictionary with the room name and its probability.
        results = {room.rsplit('@', 1)[0]: probability.elimination_ask(room, self.evidence, self.bayes_net) for room in self.last_nodes}
        
        '''
        # Print all the rooms probabilities
        print('Results')
        for room in results:
            print(room, '\t', results[room].show_approx())
        '''
        
        # Get the room with maximum probability of fire and its probability
        room = max(results.keys(), key=(lambda room: results[room][True]))
        likelihood = results[room][True]

        return (room, likelihood)

    def load_file(self, f):
        """Loads a opened file object fh. This file has the structure given in the project statement.

        Parameters
        ----------
        f : file object
            Opened file object to be used as input for the museum fire problem.

        Returns
        -------
        R : list
            List containing the room names.
        C : list of lists
            List containing the pairs of connections. Each connection is represented by a list of two room names.
        S : dictionary of dictionaries
            Dictionary where the keys are the sensors name. The values are dictionaries containing the keys 'room', 'TPR', and 'FPR'.
        P : float
            Propagation probability
        M : list of lists of dictionaries
            Each dictionary is a measurement at a given time instant where the key is the sensor name and the value the measurement.
            All the measurements of that time (dictionaries) are stored in a list.
            The lists of measurements at given time instants are stored in a list.
        """
        
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

            # Room
            if code == 'R':
                R.extend(args)
            
            # Connection
            elif code == 'C':
                C.extend([elem.split(',') for elem in args])

            # Sensor
            elif code == 'S':
                for sensor in args:
                    data = sensor.split(':')
                    S[data[0]] = {'room': data[1], 'TPR': float(data[2]), 'FPR': float(data[3])}

            # Propagation probability
            elif code == 'P':
                P = float(args[0])

            # Measurements
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
