# First attempt at making a semi-neural network to solve a
#genetic problem
import random
import math
import time


def doIt(trg,length):
    """
    This function is just so I can get the average time it takes to
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
    fout = open("expressions(BIG_FILE).txt",'w')
    times = open("time.txt",'a')
    counts = open("generations.txt",'a')
    final_exps = open("final_exps.txt",'a')
    operators = ['+', '-', '*', '/']


    def random_exp_str(length):
        """
        Create a random expression that alternates between a
        single decimal number and a binary operator (+,-,*,/)

        example:
            7-5/2*2+3
        """

        if length%2==0:
            print("Not an odd number")
            exit(1)

        x=''

        for i in range(length):

            if i%2 == 0:
                x+=str(random.randint(1,9))
            else:
                x+=random.choice(operators)

        return x


    def calc_scores(expressions, trg_val, generation_num):
        """
        Calculates the fitness score based on it's proximity to the
        target

        IMPORTANT: it also signals to end the program if it equals the target value
        """

        scores = []

        for expression in expressions:

            if round(eval(expression)) == trg_val:

                fout.write("Done\nGeneration - {0}\nExpression - {1}\nRaw value - {2}\nRounded value - {3}\nTarget - {4}\nRuntime - {5} seconds\n".format(generation_num,
                expression,eval(expression),round(eval(expression)),
                target,(time.time()-start_time)))

                times.write(str(time.time() - start_time)+'\n')
                counts.write(str(generation_num)+'\n')
                final_exps.write(str(expression) + ' = ' +
                 str(round(eval(expression))) + '\n')

                print("Done\nGeneration - {0}\nExpression - {1}\nRaw value - {2}\nRounded value - {3}\nTarget - {4}\nRuntime - {5} seconds\n".format(generation_num,
                expression,eval(expression),round(eval(expression)),
                target,(time.time()-start_time)))

                return True
            else:
                scores.append(1/abs(trg_val-eval(expression)))

        return scores

    def calc_percents(list_of_scores):
        """
        Calculates the percentage chance that an expression in
        list_of_exps will be chosen for the next generation
        """

        percents = []
        total = sum(list_of_scores)

        for i in list_of_scores:
            percents.append(i/total)

        return percents


    def mutate(expression, rate, score, gen_count):
        """
        Creates a list with len(list) <= len(expression) + 1 where a
        different character has been randomized each time from the
        original expression. There is a rate percent chance of any
        one character to be changed
        """

        mutation = [expression]
        mutated = False
        alt_exp = expression

        for i in range(len(expression)):

            # determine a multiplier to accelerate or muffle the mutation
            # multiplier<1 and the rate will be divided by it
            if score > 1:
                multiplier = 1
            elif score < .1:
                multiplier = 10
            else:
                multiplier = 1/score

            if random.random() <= rate*multiplier:
                mutated = True

                if i%2 == 0:
                    alt_exp = (alt_exp[:i] +
                        str(random.randint(1,9)) +
                        alt_exp[i+1:])
                else:
                    alt_exp = (alt_exp[:i] +
                        random.choice(operators) +
                        alt_exp[i+1:])

                if round(eval(alt_exp)) == target:
                    return mutation

        if mutated:
            mutation = [alt_exp]
            mutation.append(expression+' = '+
             str(round(eval(expression)))+' -> '+
             alt_exp+' = '+str(round(eval(alt_exp))))

        return mutation


    def cross_chromosomes(exp1,exp2,rate):
        """
        Perfoms the crossover between two chomosomes where it swaps
        the rest of the chromosomes after a random number
        """

        if random.random() <= rate:
            # Find shortest expression
            short = len(exp1) if exp1 < exp2 else len(exp2)

            cross_index = random.randint(0,short)

            # Crossover
            temp = exp1
            exp1 = exp1[:cross_index]+exp2[cross_index:]
            exp2 = exp2[:cross_index]+temp[cross_index:]
            return [exp1,exp2]

        else:
            return [exp1,exp2]


    def choose_two(num_of_pairs,expressions,percents):
        """
        Returns two expressions. The expressions are chosen based on
        the percents.
        """

        # Sort expressions based off of increasing percents
        sorted_expressions = [expression for (percent,expression)
            in sorted(zip(percents,expressions),
            key = lambda pair: pair[0])]
        # Sort percents
        sorted_percents = sorted(percents)
        pairs = []

        for i in range(num_of_pairs):
            two = []

            for j in range(2):
                # Random number to be used for determining which
                #expression to choose
                rand_num = random.random()
                current_percent = 0

                for k in range(len(sorted_percents)):
                    current_percent += sorted_percents[k]

                    if current_percent > rand_num:
                        two.append(sorted_expressions[k])
                        break

            pairs.append(two)

        return pairs

    def print_generation(generation,gen_count):
        fout.write('\nGeneration: '+str(gen_count)+'\n')

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
                    fout.write(str(j+1)+'\t'+str(generation[i][j])+' = '+
                     str(eval(generation[i][j]))+' ~= '+
                     str(round(eval(generation[i][j])))+'\n')
                else:
                    fout.write(str(j+1)+'\t'+str(generation[i][j])+'\n')


    """
    Algorithm Main
    """


    start_exps = [[]]
    done = False

    for i in range(40):
        start_exps[0].append(random_exp_str(chrom_len))

    start_exps.append(calc_scores(start_exps[0],target,count))

    if start_exps[1] == True:
        return

    start_exps.append(calc_percents(start_exps[1]))
    new_gen = start_exps

    while not done:
        if count % 25 == 0:
            print(count)
        print_generation(new_gen,count)
        mutation_count = 0
        # Make pairs to be crossed and sent to the new generation
        pairs = choose_two(len(new_gen[0])//2,new_gen[0],new_gen[2])
        new_gen = [[]]

        # Cross all the pairs and put them back into a 1D list
        for i in pairs:
            temp = cross_chromosomes(i[0],i[1],crossover_rate)

            for j in temp:
                new_gen[0].append(j)

        # Calculate the scores of this newly made generation
        #w/out mutations
        new_gen.append(calc_scores(new_gen[0],target,count))

        if new_gen[1] == True:
            return

        # Make new layer for expression percentages
        #(made before mutation in order to reserve
        #index 2 for percentages)
        new_gen.append([])

        # Mutate the new generation
        for i in range(len(new_gen[0])):
            temp = mutate(new_gen[0][i],mutation_rate,new_gen[1][i],count)

            if len(temp)>1:
                mutation_count+=1
                if mutation_count == 1:
                    new_gen.append([])
                new_gen[3].append(temp[1])

            new_gen[0][i] = temp[0]

        # Recalc scores after mutations
        new_gen[1] = calc_scores(new_gen[0],target,count)

        if new_gen[1] == True:
            return


        for i in new_gen[0]:
            new_gen[2] = calc_percents(new_gen[1])

        count += 1

    fout.close()
    times.close()
    counts.close()
    final_exps.close()

"""
Main Main

This is just here to make the Algorithm repeat multiple times to judge efficiency
"""

repititions = eval(input("Repititions: "))
target_value = eval(input("Target: "))
chromosome_length =  eval(input("Expression length: "))

for i in range(repititions):
    print("Repitition:",i+1)
    doIt(target_value, chromosome_length)
