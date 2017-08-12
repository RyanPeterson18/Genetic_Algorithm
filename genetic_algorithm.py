# First attempt at solving a genetic problem
import random
import math
import time
import pandas as pd
import os
import gen_alg_module

data_file = open("Data/genetic_algorithm_data.csv", 'a+')

functions = [
    "random_exp_str",
    "check_and_score",
    "calc_percents",
    "mutate",
    "cross_chromosomes",
    "choose_two",
    "print_generation"
]

# Create headers if not already made
if(os.stat("Data/genetic_algorithm_data.csv").st_size) == 0:
    function_time_headers = []
    for i in functions:
        function_time_headers.extend([i + " (total)", i + " (avg)"])

    data_file.write("Overall Time,{0},Expression,Raw Evaluation,Target Value,\
        Number of Generations,Optimized\n".replace("    ", '').format(
        ','.join(function_time_headers))
    )


def find_target(trg, length, data):
    """
    This function is just for finding the average time it takes to
    find a specific value for any given setup
    """
    start_time = time.time()

    # Make a standard length to use for the expression
    chrom_len = length
    # Target number for expression to reach
    target = trg
    # Set crossover rate for creating new generations
    crossover_rate = .7
    # Set mutation rate for random mutations to any character in an expression
    mutation_rate = 0.01
    count = 1
    operators = ['+', '-', '*', '/']

    out_data["fout"] = open("Data/complete_data(BIG_FILE).txt", 'w')

    out_data["function_times"] = {}
    for i in functions:
        out_data["function_times"][i] = {
            "total": 0,
            "indv_times": []
        }

    def random_exp_str(length):
        """
        Create a random expression that alternates between a
        single decimal number and a binary operator (+,-,*,/)

        NOTE: expression must be odd

        example:
            "7-5/2*2+3"
        """

        x = ''

        for i in range(length):

            if i % 2 == 0:
                x += str(random.randint(1, 9))
            else:
                x += random.choice(operators)

        return x

    def check_and_score(expressions, target, gen_count, start_time, out_data):
        """
        Checks to see if program should end and calculates the expression scores
        if it doesn't signal a stop
        """

        scores = gen_alg_module.calc_scores(expressions, target)

        if scores[1] is not None:

            # SIGNALS PROGRAM END

            expression = str(scores[1])

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

            # Stores the count, final expression, evaluation, and target
            temp_df["Expression"] = pd.Series(expression)
            temp_df["Raw Evaluation"] = pd.Series(eval(expression))
            temp_df["Target Value"] = pd.Series(target)
            temp_df["Number of Generations"] = pd.Series(gen_count)
            temp_df["Optimized"] = pd.Series(str(out_data["optimize"]))

            temp_df.to_csv(out_data["data_file"],
                           header=False, index=False)

            # Prints runtime details and various data about the execution to
            # file and console
            out_data["fout"].write("Done\nGeneration - {0}\nExpression - \
                {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
                {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                gen_count,
                expression, eval(expression), round(eval(expression)),
                target, (time.time() - start_time)
            ))

            print("Done\nGeneration - {0}\nExpression - \
            {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
            {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                gen_count,
                expression, eval(expression), round(eval(expression)),
                target, (time.time() - start_time)
            ))

            return True
        else:
            return scores[0]

    def calc_percents(list_of_scores):
        """
        Calculates the percentage chance that an expression in
        list_of_exps will be chosen for the next generation
        """

        percents = []
        total = sum(list_of_scores)

        for i in list_of_scores:
            percents.append(i / total)

        return percents

    def cross_chromosomes(exp1, exp2, rate):
        """
        Perfoms the crossover between two chomosomes where it swaps
        the rest of the chromosomes after a random number
        """

        if random.random() <= rate:
            # Find shortest expression
            short = len(exp1) if exp1 < exp2 else len(exp2)

            cross_index = random.randint(0, short)

            # Crossover
            temp = exp1
            exp1 = exp1[:cross_index] + exp2[cross_index:]
            exp2 = exp2[:cross_index] + temp[cross_index:]

            return [exp1, exp2]

        else:
            return [exp1, exp2]

    def choose_two(num_of_pairs, expressions, percents):
        """
        Returns two expressions. The expressions are chosen based on
        the percents.
        """

        # Sort expressions based off of increasing percents
        sorted_expressions = [expression for (percent, expression)
                              in sorted(zip(percents, expressions),
                                        key=lambda pair: pair[0])]
        # Sort percents
        sorted_percents = sorted(percents)
        pairs = []

        for i in range(num_of_pairs):
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

        return pairs

    def print_generation(generation, gen_count):

        out_data["fout"].write('\nGeneration: ' + str(gen_count) + '\n')

        for i in range(len(generation)):

            if i == 0:
                out_data["fout"].write("Expressions:\n")
            elif i == 1:
                out_data["fout"].write("Scores:\n")
            elif i == 2:
                out_data["fout"].write("Percentages:\n")
            else:
                out_data["fout"].write("Mutations:\n")

            for j in range(len(generation[i])):
                if i == 0:
                    out_data["fout"].write(str(j + 1) + '\t' + str(generation[i][j]) + ' = ' +
                                           str(eval(generation[i][j])) + ' ~= ' +
                                           str(round(eval(generation[i][j]))) + '\n')
                else:
                    out_data["fout"].write(str(j + 1) + '\t' +
                                           str(generation[i][j]) + '\n')

    """
    Algorithm Main
    """

    start_exps = [[]]
    done = False

    for i in range(40):
        func_start = time.time()
        start_exps[0].append(random_exp_str(chrom_len))
        out_data["function_times"]["random_exp_str"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["random_exp_str"]["indv_times"].append(
            time.time() - func_start)

    func_start = time.time()
    start_exps.append(check_and_score(
        start_exps[0], target, count, start_time, out_data))

    if start_exps[1] == True:
        out_data["fout"].close()
        return
    else:
        out_data["function_times"]["check_and_score"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["check_and_score"]["indv_times"].append(
            time.time() - func_start)

    func_start = time.time()
    start_exps.append(calc_percents(start_exps[1]))
    out_data["function_times"]["calc_percents"]["total"] += time.time() - \
        func_start
    out_data["function_times"]["calc_percents"]["indv_times"].append(
        time.time() - func_start)
    new_gen = start_exps

    # Make sure lenght is odd
    if length % 2 == 0:
        print("Length not odd, rounding up")
        length += 1

    while not done:
        if count % 25 == 0:
            print(count)

        if out_data["optimize"] == False:
            func_start = time.time()
            print_generation(new_gen, count)
            out_data["function_times"]["print_generation"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["print_generation"]["indv_times"].append(
                time.time() - func_start)
        mutation_count = 0
        # Make pairs to be crossed and sent to the new generation
        func_start = time.time()
        pairs = choose_two(len(new_gen[0]) // 2, new_gen[0], new_gen[2])
        out_data["function_times"]["choose_two"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["choose_two"]["indv_times"].append(
            time.time() - func_start)
        new_gen = [[]]

        # Cross all the pairs and put them back into a 1D list
        for i in pairs:
            func_start = time.time()
            temp = cross_chromosomes(i[0], i[1], crossover_rate)
            out_data["function_times"]["cross_chromosomes"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["cross_chromosomes"]["indv_times"].append(
                time.time() - func_start)

            for j in temp:
                new_gen[0].append(j)

        # Calculate the scores of this newly made generation
        # w/out mutations
        func_start = time.time()
        new_gen.append(check_and_score(
            new_gen[0], target, count, start_time, out_data))

        if new_gen[1] == True:
            out_data["fout"].close()
            return
        else:
            out_data["function_times"]["check_and_score"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["check_and_score"]["indv_times"].append(
                time.time() - func_start)

        # Make new layer for expression percentages
        # (made before mutation in order to reserve
        # index 2 for percentages)
        new_gen.append([])

        # Mutate the new generation
        for i in range(len(new_gen[0])):
            func_start = time.time()
            temp = gen_alg_module.mutate(new_gen[0][i], mutation_rate,
                                         new_gen[1][i], operators, target)
            out_data["function_times"]["mutate"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["mutate"]["indv_times"].append(
                time.time() - func_start)

            if len(temp) > 1:
                mutation_count += 1
                if mutation_count == 1:
                    new_gen.append([])
                new_gen[3].append(temp[1])

            new_gen[0][i] = temp[0]

        # Recalc scores after mutations
        func_start = time.time()
        new_gen[1] = check_and_score(
            new_gen[0], target, count, start_time, out_data)

        if new_gen[1] == True:
            out_data["fout"].close()
            return
        else:
            out_data["function_times"]["check_and_score"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["check_and_score"]["indv_times"].append(
                time.time() - func_start)

        for i in new_gen[0]:
            func_start = time.time()
            new_gen[2] = calc_percents(new_gen[1])

        count += 1


"""
Main Main

This is just here to make the Algorithm repeat multiple times to
judge efficiency
"""

repititions = input("Repititions [100]: ")
target_value = input("Target [9235]: ")
chromosome_length = input("Expression length (odd) [75]: ")
speed = input("Optimize speed [y]/n?")

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

valid = False
while not valid:
    if speed == '':
        speed = True
        valid = True
    elif speed == 'n' or speed == 'N':
        speed = False
        valid = True
    else:
        speed = input("Please enter 'y' or 'n' to optimize speed or not [y]: ")

out_data = {
    "data_file": data_file,
    "optimize": speed
}

for i in range(repititions):
    print("Repitition:", i + 1)
    find_target(target_value, chromosome_length, out_data)

data_file.close()
