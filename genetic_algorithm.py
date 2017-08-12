# First attempt at solving a genetic problem
import random
import math
import time
import pandas as pd
import os
import gen_alg_module

data_file = open("Data/genetic_algorithm_data.csv", 'a+')

# Create headers if not already made
if(os.stat("Data/genetic_algorithm_data.csv").st_size) == 0:
    data_file.write("Overall Time,random_exp_str (total),\
random_exp_str (avg),calc_scores (total),calc_scores (avg),\
calc_percents (total),calc_percents (avg),mutate (total),mutate (avg),\
cross_chromosomes (total),cross_chromosomes (avg),choose_two (total),\
choose_two (avg), print_generation (total),print_generation (avg),\
Expression,Raw Evaluation,Target Value,Number of Generations,Optimized\n")


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

    fout = open("Data/complete_data(BIG_FILE).txt", 'w')

    out_data["function_times"] = {
        "random_exp_str": {
            "total": 0,
            "indv_times": []
        },
        "calc_scores": {
            "total": 0,
            "indv_times": []
        },
        "calc_percents": {
            "total": 0,
            "indv_times": []
        },
        "mutate": {
            "total": 0,
            "indv_times": []
        },
        "cross_chromosomes": {
            "total": 0,
            "indv_times": []
        },
        "choose_two": {
            "total": 0,
            "indv_times": []
        },
        "print_generation": {
            "total": 0,
            "indv_times": []
        }
    }

    def random_exp_str(length):
        """
        Create a random expression that alternates between a
        single decimal number and a binary operator (+,-,*,/)

        NOTE: expression must be odd

        example:
            "7-5/2*2+3"
        """
        func_start = time.time()

        x = ''

        for i in range(length):

            if i % 2 == 0:
                x += str(random.randint(1, 9))
            else:
                x += random.choice(operators)

        out_data["function_times"]["random_exp_str"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["random_exp_str"]["indv_times"].append(
            time.time() - func_start)
        return x

    def calc_scores(expressions, trg_val, generation_num, out_data):
        """
        Calculates the fitness score based on it's proximity to the
        target

        NOTE: it also signals to end the program if it equals the target value
        """

        func_start = time.time()

        scores = []

        for expression in expressions:

            if round(eval(expression)) == trg_val:

                # SIGNALS PROGRAM END

                # Prints runtime details and various data about the execution
                fout.write("Done\nGeneration - {0}\nExpression - \
                    {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
                    {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                    generation_num,
                    expression, eval(expression), round(eval(expression)),
                    target, (time.time() - start_time)
                ))

                temp_df = pd.DataFrame()

                # Stores the overall runtime
                temp_df["Overall Time"] = pd.Series(time.time() - start_time)

                # Stores the runtime averages and totals for each func
                for k, v in out_data["function_times"].items():
                    temp_df[str(k + " (total)")] = pd.Series(v["total"])

                    if len(v["indv_times"]) is not 0:
                        temp_df[str(k + " (avg)")] = pd.Series(sum(v["indv_times"])
                                                               / len(v["indv_times"]))
                    else:
                        temp_df[str(k + " (avg)")] = pd.Series(0)

                # Stores the count, final expression, evaluation, and trg_val
                temp_df["Expression"] = pd.Series(expression)
                temp_df["Raw Evaluation"] = pd.Series(eval(expression))
                temp_df["Target Value"] = pd.Series(trg_val)
                temp_df["Number of Generations"] = pd.Series(generation_num)
                temp_df["Optimized"] = pd.Series(str(out_data["optimize"]))

                temp_df.to_csv(out_data["data_file"],
                               header=False, index=False)

                print("Done\nGeneration - {0}\nExpression - \
                {1}\nRaw value - {2}\nRounded value - {3}\nTarget - \
                {4}\nRuntime - {5} seconds\n".replace('    ', '').format(
                    generation_num,
                    expression, eval(expression), round(eval(expression)),
                    target, (time.time() - start_time)
                ))

                return True

            else:
                scores.append(1 / abs(trg_val - eval(expression)))

        out_data["function_times"]["calc_scores"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["calc_scores"]["indv_times"].append(
            time.time() - func_start)
        return scores

    def calc_percents(list_of_scores):
        """
        Calculates the percentage chance that an expression in
        list_of_exps will be chosen for the next generation
        """

        func_start = time.time()

        percents = []
        total = sum(list_of_scores)

        for i in list_of_scores:
            percents.append(i / total)

        out_data["function_times"]["calc_percents"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["calc_percents"]["indv_times"].append(
            time.time() - func_start)
        return percents

    # def mutate(expression, rate, score, operators, target, data):
    #     """
    #     Creates a list with len(list) <= len(expression) + 1 where a
    #     different character has been randomized each time from the
    #     original expression. There is a rate percent chance of any
    #     one character to be changed
    #     """
    #
    #     func_start = time.time()
    #
    #     mutation = [expression]
    #     mutated = False
    #     alt_exp = expression
    #
    #     for i in range(len(expression)):
    #
    #         # determine a multiplier to accelerate or muffle the mutation
    #         # multiplier<1 and the rate will be divided by it
    #         if score > 1:
    #             multiplier = 1
    #         elif score < .1:
    #             multiplier = 10
    #         else:
    #             multiplier = 1 / score
    #
    #         if random.random() <= rate * multiplier:
    #             mutated = True
    #
    #             if i % 2 == 0:
    #                 alt_exp = (alt_exp[:i] +
    #                            str(random.randint(1, 9)) +
    #                            alt_exp[i + 1:])
    #             else:
    #                 alt_exp = (alt_exp[:i] +
    #                            random.choice(operators) +
    #                            alt_exp[i + 1:])
    #
    #             if round(eval(alt_exp)) == target:
    #                 out_data["function_times"]["mutate"]["total"] += time.time() - \
    #                     func_start
    #                 out_data["function_times"]["mutate"]["indv_times"].append(
    #                     time.time() - func_start)
    #                 return mutation
    #
    #     if mutated:
    #         mutation = [alt_exp]
    #         mutation.append(expression + ' = ' +
    #                         str(round(eval(expression))) + ' -> ' +
    #                         alt_exp + ' = ' + str(round(eval(alt_exp))))
    #
    #     out_data["function_times"]["mutate"]["total"] += time.time() - \
    #         func_start
    #     out_data["function_times"]["mutate"]["indv_times"].append(
    #         time.time() - func_start)
    #     return mutation

    def cross_chromosomes(exp1, exp2, rate):
        """
        Perfoms the crossover between two chomosomes where it swaps
        the rest of the chromosomes after a random number
        """

        func_start = time.time()

        if random.random() <= rate:
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
            return [exp1, exp2]

        else:
            out_data["function_times"]["cross_chromosomes"]["total"] += time.time() - \
                func_start
            out_data["function_times"]["cross_chromosomes"]["indv_times"].append(
                time.time() - func_start)
            return [exp1, exp2]

    def choose_two(num_of_pairs, expressions, percents):
        """
        Returns two expressions. The expressions are chosen based on
        the percents.
        """

        func_start = time.time()

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

        out_data["function_times"]["choose_two"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["choose_two"]["indv_times"].append(
            time.time() - func_start)
        return pairs

    def print_generation(generation, gen_count):
        func_start = time.time()

        fout.write('\nGeneration: ' + str(gen_count) + '\n')

        for i in range(len(generation)):

            if i == 0:
                fout.write("Expressions:\n")
            elif i == 1:
                fout.write("Scores:\n")
            elif i == 2:
                fout.write("Percentages:\n")
            else:
                fout.write("Mutations:\n")

            for j in range(len(generation[i])):
                if i == 0:
                    fout.write(str(j + 1) + '\t' + str(generation[i][j]) + ' = ' +
                               str(eval(generation[i][j])) + ' ~= ' +
                               str(round(eval(generation[i][j]))) + '\n')
                else:
                    fout.write(str(j + 1) + '\t' +
                               str(generation[i][j]) + '\n')

        out_data["function_times"]["print_generation"]["total"] += time.time() - \
            func_start
        out_data["function_times"]["print_generation"]["indv_times"].append(
            time.time() - func_start)

    """
    Algorithm Main
    """

    start_exps = [[]]
    done = False

    for i in range(40):
        start_exps[0].append(random_exp_str(chrom_len))

    start_exps.append(calc_scores(start_exps[0], target, count, out_data))

    if start_exps[1] == True:
        fout.close()
        return

    start_exps.append(calc_percents(start_exps[1]))
    new_gen = start_exps

    # Make sure lenght is odd
    if length % 2 == 0:
        print("Length not odd, rounding up")
        length += 1

    while not done:
        if count % 25 == 0:
            print(count)

        if out_data["optimize"] == False:
            print_generation(new_gen, count)
        mutation_count = 0
        # Make pairs to be crossed and sent to the new generation
        pairs = choose_two(len(new_gen[0]) // 2, new_gen[0], new_gen[2])
        new_gen = [[]]

        # Cross all the pairs and put them back into a 1D list
        for i in pairs:
            temp = cross_chromosomes(i[0], i[1], crossover_rate)

            for j in temp:
                new_gen[0].append(j)

        # Calculate the scores of this newly made generation
        # w/out mutations
        new_gen.append(calc_scores(new_gen[0], target, count, out_data))

        if new_gen[1] == True:
            fout.close()
            return

        # Make new layer for expression percentages
        #(made before mutation in order to reserve
        # index 2 for percentages)
        new_gen.append([])

        # Mutate the new generation
        for i in range(len(new_gen[0])):
            temp = gen_alg_module.mutate(new_gen[0][i], mutation_rate,
                                         new_gen[1][i], operators, target, out_data)

            if len(temp) > 1:
                mutation_count += 1
                if mutation_count == 1:
                    new_gen.append([])
                new_gen[3].append(temp[1])

            new_gen[0][i] = temp[0]

        # Recalc scores after mutations
        new_gen[1] = calc_scores(new_gen[0], target, count, out_data)

        if new_gen[1] == True:
            fout.close()
            return

        for i in new_gen[0]:
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
