# First attempt at solving a genetic problem
import random
import math
import time
import pandas as pd
import os
from sys import maxsize
import gen_alg_module


class Generation():
    """
    Contains the data and methods involved with a generation of expressions
    """

    # Binary operators to use in expressions
    operators = ['+', '-', '*', '/']
    # Set crossover rate for creating new generations
    crossover_rate = .7

    def __init__(self, size, length, target):
        """
        Create a random expression that alternates between a
        single decimal number and a binary operator (+,-,*,/)

        NOTE: length must be odd

        example:
            "7-5/2*2+3"
        """

        func_start = time.time()

        self.size = size
        self.length = length
        self.target = target
        self.expressions = []
        self.scores = []
        self.percents = []
        self.values = []
        self.mutations = []
        self.count = 1
        self.mutation_count = 0

        if length % 2 == 0:
            raise RuntimeError("Improper expression length, must be odd")

        for i in range(size):
            expression = ''

            for i in range(length):

                if i % 2 == 0:
                    expression += str(random.randint(1, 9))
                else:
                    expression += random.choice(self.operators)
            self.expressions.append(expression)

        out_data["function_times"]["Generation.__init__"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["Generation.__init__"]["indv_times"].append(
            time.time() - func_start)

    def clear_data(self):
        self.expressions = []
        self.scores = []
        self.percents = []
        self.values = []
        self.mutations = []
        self.mutation_count = 0

    def __iadd__(self, other):
        self.count += other
        return self

    def get_count(self):
        return self.count

    def mutate(self, out_data):
        """
        Mutates the current generation
        """

        func_start = time.time()

        for i in range(len(self.expressions)):

            temp = gen_alg_module.mutate(self.expressions[i],
                                         out_data["mutation_constants"]["rate_cap"],
                                         out_data["mutation_constants"]["rate_constant"],
                                         self.values[i], out_data["mutation_constants"]["max_exponent"],
                                         self.operators, self.target, out_data)

            if len(temp) > 1:
                self.mutation_count += 1
                self.mutations.append(temp[1])

            self.expressions[i] = temp[0]

        out_data["function_times"]["mutate"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["mutate"]["indv_times"].append(
            time.time() - func_start)

    def check_and_score(self, start_time, out_data):
        """
        Checks to see if program should end and calculates the expression scores
        if it doesn't signal a stop

        NOTE: this function triggers the program end
        """

        func_start = time.time()

        scores_and_values = gen_alg_module.calc_scores(
            self.expressions, self.target)

        # If the first index is True, the target has been reached
        if scores_and_values[0] is True:

            # SIGNALS PROGRAM END

            expression = str(scores_and_values[1])

            temp_df = pd.DataFrame()

            # Stores the overall runtime
            temp_df["Overall Time"] = pd.Series(time.time() - start_time)

            # Stores the runtime averages and totals for each func
            for i in functions:
                temp_df[str(i + " (total)")
                        ] = pd.Series(out_data["function_times"][i]["total"])

                if len(out_data["function_times"][i]["indv_times"]) is not 0:
                    temp_df[str(i + " (avg)")] = pd.Series(sum(out_data["function_times"][i]["indv_times"])
                                                           / len(out_data["function_times"][i]["indv_times"]))
                else:
                    temp_df[str(i + " (avg)")] = pd.Series(0)

            # Stores the generation.count, final expression, evaluation, and target
            temp_df["Expression"] = pd.Series(expression)
            temp_df["Raw Evaluation"] = pd.Series(eval(expression))
            temp_df["Target Value"] = pd.Series(self.target)
            temp_df["Number of Generations"] = pd.Series(self.count)
            temp_df["Optimized"] = pd.Series(str(out_data["optimize"]))
            temp_df["rate_cap"] = pd.Series(
                str(out_data["mutation_constants"]["rate_cap"]))
            temp_df["rate_constant"] = pd.Series(
                str(out_data["mutation_constants"]["rate_constant"]))

            temp_df.to_csv(out_data["data_file"],
                           header=False, index=False)

            # Prints runtime details and various data about the execution to
            # file and console
            if out_data["optimize"] == False:
                out_data["fout"].write("Done\nGeneration - {0}\nExpression - \
                    {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
                    {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                    self.count,
                    expression, eval(expression), round(eval(expression)),
                    self.target, (time.time() - start_time)
                ))

            print("Done\nGeneration - {0}\nExpression - \
            {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
            {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                self.count,
                expression, eval(expression), round(eval(expression)),
                self.target, (time.time() - start_time)
            ))

            return True
        else:
            out_data["function_times"]["check_and_score"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["check_and_score"]["indv_times"].append(
                time.time() - func_start)

            self.scores, self.values = scores_and_values

            return False

    def calc_percents(self):
        """
        Calculates the percentage chance that an expression in
        list_of_exps will be chosen for the next generation
        """

        func_start = time.time()

        total = sum(self.scores)

        for i in self.scores:
            self.percents.append(i / total)

        out_data["function_times"]["calc_percents"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["calc_percents"]["indv_times"].append(
            time.time() - func_start)

    def cross_chromosomes(self, pairs):
        """
        Perfoms the crossover between two chomosomes where it swaps
        the rest of the chromosomes after a random number
        """

        func_start = time.time()

        for exp1, exp2 in pairs:
            if random.random() <= self.crossover_rate:
                # Find shortest expression
                short = len(exp1) if exp1 < exp2 else len(exp2)

                cross_index = random.randint(0, short)

                # Crossover
                temp = exp1
                exp1 = exp1[:cross_index] + exp2[cross_index:]
                exp2 = exp2[:cross_index] + temp[cross_index:]

                out_data["function_times"]["cross_chromosomes"]["total"] += time.time() - \
                    func_start
                out_data["function_times"]["cross_chromosomes"]["indv_times"].append(
                    time.time() - func_start)

                self.expressions.extend([exp1, exp2])
            else:
                self.expressions.extend([exp1, exp2])

        out_data["function_times"]["cross_chromosomes"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["cross_chromosomes"]["indv_times"].append(
            time.time() - func_start)

    def choose_two(self):
        """
        Returns a list of pairs. The expressions are chosen based on
        the percents.
        """

        func_start = time.time()

        # Sort expressions based off of increasing percents
        sorted_expressions = [expression for (percent, expression)
                              in sorted(zip(self.percents, self.expressions),
                                        key=lambda pair: pair[0])]
        # Sort percents
        sorted_percents = sorted(self.percents)

        pairs = []

        for i in range(self.size // 2):
            two = []

            for j in range(2):
                # Random number to be used for determining which
                # expression to choose
                rand_num = random.random()
                current_percent = 0

                for k in range(len(sorted_percents)):
                    current_percent += sorted_percents[k]

                    if current_percent > rand_num:
                        two.append(sorted_expressions[k])
                        break

            pairs.append(two)

        out_data["function_times"]["choose_two"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["choose_two"]["indv_times"].append(
            time.time() - func_start)

        return pairs

    def print_generation(self, out_data):
        """
        Logs the generation to fout
        """

        func_start = time.time()

        out_data["fout"].write('\nGeneration: ' + str(self.count) + '\n')

        out_data["fout"].write("Expressions:\n")
        for j in range(len(self.expressions)):
            out_data["fout"].write(str(j + 1) + '\t' + str(self.expressions[j]) + ' = ' +
                                   str(eval(self.expressions[j])) + ' ~= ' +
                                   str(round(eval(self.expressions[j]))) + '\n')

        out_data["fout"].write("Scores:\n")
        for j in range(len(self.scores)):
            out_data["fout"].write(str(j + 1) + '\t' +
                                   str(self.scores[j]) + '\n')

        out_data["fout"].write("Percentages:\n")
        for j in range(len(self.percents)):
            out_data["fout"].write(str(j + 1) + '\t' +
                                   str(self.percents[j]) + '\n')

        out_data["fout"].write("Mutations:\n")
        for j in range(len(self.mutations)):
            out_data["fout"].write(str(j + 1) + '\t' +
                                   str(self.mutations[j]) + '\n')

        out_data["function_times"]["print_generation"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["print_generation"]["indv_times"].append(
            time.time() - func_start)

    """
    Algorithm Main
    """


def algorithm_main(target, out_data, length=None):
    """
    This function is just for finding the average time it takes to
    find a specific value for any given setup

    TODO: find mutation constants edge cases
    """
    start_time = time.time()

    # Set mutation constants
    if out_data["training"] is True:
        out_data["mutation_constants"] = {
            "rate_cap": random.randrange(100, 500) / 1000,
            "rate_constant": random.randrange(0, 500) / 100,
            "max_exponent": math.log(maxsize)
        }
    else:
        out_data["mutation_constants"] = {
            "rate_cap": .4,
            "rate_constant": 2.5,
            "max_exponent": math.log(maxsize)
        }

    # Make a standard length to use for the expression
    chrom_len = length

    if out_data["optimize"] == False:
        out_data["fout"] = open("complete_data(BIG_FILE).dat", 'w')

    out_data["function_times"] = {}
    for i in functions:
        out_data["function_times"][i] = {
            "total": 0,
            "indv_times": []
        }

    done = False

    # Randomly generate a starting population
    Gen = Generation(40, 75, target)

    # Score the starting population
    finished = Gen.check_and_score(start_time, out_data)

    # check_and_score returns None if the target has been reached
    if finished:
        if out_data["optimize"] == False:
            out_data["fout"].close()
        return

    # Calculate the pecent chance that the expression is going to "reproduce"
    Gen.calc_percents()

    while not done:
        if Gen.get_count() % 25 == 0:
            print(Gen.get_count())

        # Verbose logging if speed is not optimized
        if out_data["optimize"] == False:
            Gen.print_generation(out_data)

        # Make pairs to be crossed and sent to the new generation
        pairs = Gen.choose_two()

        # clear the current generation data
        Gen.clear_data()

        # Cross all the pairs
        Gen.cross_chromosomes(pairs)
        # Calculate the scores of this newly made generation
        # w/out mutations
        finished = Gen.check_and_score(start_time, out_data)

        if finished:
            if out_data["optimize"] == False:
                out_data["fout"].close()
            return

        # Mutate the new generation
        Gen.mutate(out_data)

        # Recalc scores after mutations
        finished = Gen.check_and_score(start_time, out_data)

        if finished:
            if out_data["optimize"] == False:
                out_data["fout"].close()
            return

        # Calculate the percent chance that any given expression will "reproduce"
        Gen.calc_percents()

        Gen += 1


"""
Main Main

This is just here to make the Algorithm repeat multiple times to
judge efficiency
"""

# Open data file for final output
data_file = open("genetic_algorithm_data.csv", 'a+')

# Used for time logging, changes to this will be implemented throughout the code
functions = [
    "Generation.__init__",
    "check_and_score",
    "calc_percents",
    "mutate",
    "cross_chromosomes",
    "choose_two",
    "print_generation"
]

# Create headers if not already made
if(os.stat("genetic_algorithm_data.csv").st_size) == 0:
    function_time_headers = []
    for i in functions:
        function_time_headers.extend([i + " (total)", i + " (avg)"])

    data_file.write("Overall Time,{0},Expression,Raw Evaluation,Target Value,\
        Number of Generations,Optimized,rate_cap,rate_constant\n".replace("    ", '').format(
        ','.join(function_time_headers))
    )

# Read in data required for the program execution
data_generation = input("Run to generate training data y/[n]? ")

if data_generation is '' or data_generation is 'n':
    repititions = input("Repititions [100]: ")
    target_value = input("Target [9235]: ")
    chromosome_length = input("Expression length (odd) [75]: ")
    speed = input("Optimize speed [y]/n? ")

    if repititions == '':
        repititions = 100
    else:
        repititions = int(repititions)

    if target_value == '':
        target_value = 9235
    else:
        target_value = int(target_value)

    if chromosome_length == '':
        chromosome_length = 75
    else:
        chromosome_length = int(chromosome_length)
        # Make sure lenght is odd
        if chromosome_length % 2 == 0:
            print("Length not odd, rounding up")
            chromosome_length += 1

    valid = False
    while not valid:
        if speed == '':
            speed = True
            valid = True
        elif speed == 'n' or speed == 'N':
            speed = False
            valid = True
        else:
            speed = input(
                "Please enter 'y' or 'n' to optimize speed or not [y]: ")

    training = False
else:
    speed = True
    repititions = None
    target_value = 9235
    training = True


out_data = {
    "data_file": data_file,
    "optimize": speed,
    "training": training
}

if repititions is not None:
    for i in range(repititions):
        print("Repitition", i + 1, "of", repititions)
        algorithm_main(target_value, out_data, chromosome_length)
else:
    count = 0
    while True:
        print("Repitition", count + 1, "of INFINITY")
        algorithm_main(target_value, out_data)
        count += 1

data_file.close()
