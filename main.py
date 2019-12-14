"""Artificial Intelligence and Decision Systems (IASD)
Mini-projects, 2019/2020
Assignment #2 - The museum is on fire!
MEAer

André Oliveira  - 83663
Gonçalo Raposo  - 83682
João Bernardino - 83696
"""

import probability

# Flag for debug prints
debug = False

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
    get_parents(R, C)
        Returns a dictionary where the keys are the rooms names and the values are lists of connections (including a connection with itself).
        This facilitates the generation of the Bayes network.
    get_conditional_probabilities(R, P, parents)
        Returns a dictionary where the keys are the rooms names and the values are dictionaries of a truth table and the conditional probabilities
        (of fire propagation) for the rooms nodes. It is used to create the Bayes network.
    get_sensor_probabilities(S)
        Creates a dictionary containing the sensors nodes conditional probabilities of TPR and FPR. 
        This facilitates the generation of the Bayes network.
    get_evidence(S, M)
        Returns a dictionary containing the measurements/evidences in the format used by elimination_ask().
    create_bayes_net(R, S, M, parents, cond_prob, sensor_prob, P_F)
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

        # Get a dictionary containing the conditional probabilities tables from the sensor nodes
        sensor_prob = self.get_sensor_probabilities(S)

        # Get a dictiionary containing the evidence/measurements in the format used by the elimination_ask()
        self.evidence = self.get_evidence(S, M)

        # Name of the room nodes at the last instant
        n = len(M)-1
        self.last_nodes = [room+f'@{n}' for room in R]

        # Probability of fire. Since there's no information which rooms are on fire, it's like flipping a coin - 50/50 probability
        P_F = 0.5

        # Create Bayesian Network
        self.bayes_net = self.create_bayes_net(R, S, M, parents, cond_prob, sensor_prob, P_F)

        if debug:
            # Print the created variables
            print('Rooms', '\n', R, '\n')
            print('Connections', '\n', C, '\n')
            print('Sensors', '\n', S, '\n')
            print('Probability', '\n', P, '\n')
            print('Measurement', '\n', M, '\n')
            print('Connections2', '\n', parents, '\n')
            print('Bayesian Network', '\n', self.bayes_net, '\n');

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
        
        if debug:
            # Print all the rooms probabilities
            print('Results')
            for room in results:
                print(room, '\t', results[room].show_approx())
        
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
        """Creates a dictionary where the keys are the rooms names and the values are lists of connections (including a connection with itself).
        This facilitates the generation of the Bayes network, since the parents of the room nodes are always their connections

        Parameters
        ----------
        R : list
            List containing the room names.
        C : list of lists
            List containing the pairs of connections. Each connection is represented by a list of two room names.

        Returns
        -------
        parents : dictionary of lists
            A dictionary containing the parents of each room node. The key is the room name and the value is a lists of its connections plus itself.
        """
        # Initialize dictionary with all the rooms and a list containg its name
        parents = {room: [room] for room in R}

        # Loop through all the pairs of connections
        for connection in C:
            # Append the connection from first to second in the first room list
            parents[connection[0]].append(connection[1])
            # Append the connection from second to first in the second room list
            parents[connection[1]].append(connection[0])

        return parents

    def get_conditional_probabilities(self, R, P, parents):
        """Creates a dictionary containing the room nodes conditional probabilities of fire propagation.
        This is useful when generating the Bayes net because all the room nodes (except the ones at the first time instant) have these conditional probabilities.

        Parameters
        ----------
        R : list
            List containing the room names.
        P : float
            Propagation probability
        parents : dictionary of lists
            A dictionary containing the parents of each room node. The key is the room name and the value is a lists of its connections plus itself.

        Returns
        -------
        cond_prob : dictionary of dictinaries
            A dictionary containing the the conditional probabilities of the room nodes.
            The keys are the room names and the values are another dictionary containing the conditional probabilities.
            The keys of this other dictionary are the entries of the truth table as boolean lists and the values are the (conditional) probabilities of that truth table.
        """

        from itertools import product

        # Initialize dictionary
        cond_prob = {room: 0 for room in R}

        for room in R:
            # Number of columns of the truth table
            n = len(parents[room])
            # Generate the truth table input
            table = list(product([False, True], repeat=n))
            
            # The first column corresponds to the same room in the previous time instant.
            # The second half of that table has that column as True, which means the room was on fire and, therefore, the probability of being on fire is 1.
            # For the other cases, the probability of being on fire is the probability of fire propagation (except the first row)
            half = 2**(n-1)
            prob = [P if i<half else 1 for i in range(len(table))]

            # For the first row, since no room was on fire, the probability of being on fire is 0
            prob[0] = 0

            cond_prob[room] = dict(zip(table, prob))
    
        return cond_prob

    def get_sensor_probabilities(self, S):
        """Creates a dictionary containing the sensors nodes conditional probabilities of TPR and FPR. 
        This is useful when generating the Bayes net because all the sensors nodes have these conditional probabilities.

        Parameters
        ----------
        S : dictionary of dictionaries
            Dictionary where the keys are the sensors names. The values are dictionaries containing the keys 'room', 'TPR', and 'FPR'.

        Returns
        -------
        sensor_prob : dictionary of dictinaries
            A dictionary containing the the conditional probabilities of the sensor nodes.
            The keys are the sensors' names and the values are another dictionary containing the FPR for False and TPR for True.
        """

        sensor_prob = {sensor : {False: S[sensor]['FPR'], True: S[sensor]['TPR']} for sensor in S}

        return sensor_prob

    def get_evidence(self, S, M):
        """Returns a dictionary containing the measurements/evidences in the format used by elimination_ask().

        Parameters
        ----------
        S : dictionary of dictionaries
            Dictionary where the keys are the sensors name. The values are dictionaries containing the keys 'room', 'TPR', and 'FPR'.
        M : list of lists of dictionaries
            Each dictionary is a measurement at a given time instant where the key is the sensor name and the value the measurement.
            All the measurements of that time (dictionaries) are stored in a list.
            The lists of measurements at given time instants are stored in a list.

        Returns
        -------
        evidence : dictionary
            The keys of the dictionary are the names of the measurement nodes. The values are the measurements.
        """

        evidence = {m['sensor']+f'@{i}': m['measurement'] for i, measurements in enumerate(M) for m in measurements}

        return evidence

    def create_bayes_net(self, R, S, M, parents, cond_prob, sensor_prob, P_F):
        """Creates the Bayesian network for the museum fire problem, as implemented in the AIMA repository.
        Each node has a unique name, where the time instant is explicited by the ending '@<time instant>'.
        For example, the room 'history' at time instant 0 will have a node named 'history@0'.
        Each 'level' of the Bayes net corresponds to a time instant.
        Suppose two connected rooms 'artificial' and 'intelligence'. The room intelligence has a sensor 's1'. There are measurements for two time instants
        The Bayesian network would be:
             ______________      ________________
            | artificial@0 |    | intelligence@0 |       ______
            |______________|    |________________|----->| s1@0 |
                    | \_______         / |              |______|
                    |   ______\_______/  |        
                    |  /       \_______  |
                    | /                \ |
             _______v_v____      ______v_v_______
            | artificial@1 |    | intelligence@1 |       ______
            |______________|    |________________|----->| s1@1 |
                                                        |______|

        Parameters
        ----------
        R : list
            List containing the room names.
        S : dictionary of dictionaries
            Dictionary where the keys are the sensors name. The values are dictionaries containing the keys 'room', 'TPR', and 'FPR'.
        M : list of lists of dictionaries
            Each dictionary is a measurement at a given time instant where the key is the sensor name and the value the measurement.
            All the measurements of that time (dictionaries) are stored in a list.
            The lists of measurements at given time instants are stored in a list.
        parents : dictionary of lists
            A dictionary containing the parents of each room node. The key is the room name and the value is a lists of its connections plus itself.
        cond_prob : dictionary of dictinaries
            A dictionary containing the the conditional probabilities of the room nodes.
            The keys are the room names and the values are another dictionary containing the conditional probabilities.
            The keys of this other dictionary are the entries of the truth table as boolean lists and the values are the (conditional) probabilities of that truth table.
        sensor_prob : dictionary of dictinaries
            A dictionary containing the the conditional probabilities of the sensor nodes.
            The keys are the sensors' names and the values are another dictionary containing the FPR for False and TPR for True.
        P_F : float
            Fire propagation probability

        Returns
        -------
        bayes_net : probability.BayesNet
            A Bayesian network as implemented in the AIMA repository.
            This network will represent the museum fire problem (as illustrated above).
        """

        # Initialize Bayes net
        bayes_net = probability.BayesNet()

        # Add nodes of rooms at time instant 0 (and probability of fire of 50%)
        for room in R:
            bayes_net.add((room+'@0', '', P_F))

        # Add nodes of rooms at the following time steps (the amount of time steps correspond to the number of instants of the measurements)
        for i in range(1, len(M)):
            for room in R:
                # Getting parents name at step i-1
                parents_i = [parent+f'@{i-1}' for parent in parents[room]]

                # Adding node to the net. Name is the name of the room plus @<time instant>, parents is a string of all
                # the parents_i separated by spaces, and the conditional probability depends on the fire propagation law
                bayes_net.add((room+f'@{i}', ' '.join(parents_i), cond_prob[room]))

        # Add measurements nodes at all time steps
        for i, measurements in enumerate(M):
            for m in measurements:
                # Sensor name
                sensor = m['sensor']

                # Adding node to the net. Name is the sensor name plus @<time instant>, parent is the room where
                # it is installed plus @<time instant> and conditional probability corresponds to the FPR and TPR.
                bayes_net.add((sensor+f'@{i}', S[sensor]['room']+f'@{i}', sensor_prob[sensor]))
        
        return bayes_net

def solver(input_file):
    """Solve the museum fire problem given a open input file object.

    Parameters
    ----------
    fh : file
        Opened file object to be used as input for the museum fire problem.

    Returns
    -------
    tuple : tuple
        The first element is a string containing the room name.
        The second element is a a float which value is the probablity to be on fire.
    """

    return Problem(input_file).solve()

def read_argv():
    """Processes the arguments given through argv. If the input filename isn't given, the program exits.

    Returns:
    --------
    in_filename : string
        Input file name as given thorugh argv.
    show : boolean
        Boolean variable to show to print the result in stdout.
    """

    from sys import argv, exit
    
    l = len(argv)

    if l==1:
        print(argv[0]+" <input file> <print bool>")
        exit(0)
    elif l==2:
        show = False
    else:
        show = str2bool(argv[2])

    in_filename = argv[1]

    return in_filename, show 

def get_out_filename(in_filename):
    """Receives a filename and returns the string "output/<filename>". Works in every operating system

    Parameters:
    -----------
    in_filename : string
        Filename to use.

    Returns:
    --------
    out_filename : string
        Filename inside directory output.
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
    # Get input file name and show flag
    in_filename, show = read_argv()
    
    # Open file and solve museum fire problem
    with open(in_filename, 'r') as f:
        sol = solver(f)

        # Print solution
        if show:
            print('Solution', '\n', sol)

    # Get output file name
    out_filename = get_out_filename(in_filename)

    # Open output file and save solution as '<room> <likelihood>'
    with open(out_filename, 'w') as f:
        f.write(f'{sol[0]} {sol[1]}')
        f.write('\n')

