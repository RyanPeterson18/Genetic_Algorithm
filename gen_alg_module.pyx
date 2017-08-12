import random
import time
import pandas as pd


def calc_scores(expressions, target):
    """
    Calculates the fitness score based on it's proximity to the
    target

    NOTE: it also signals to end the program if it equals the target value
    """

    scores = []

    for expression in expressions:

        if round(eval(expression[:])) == target:
            return True, expression
        else:
            scores.append(1 / abs(target - eval(expression)))

    return scores, None


def mutate(expression, rt, score, operators, target):
    """
    Creates a list with len(list) <= len(expression) + 1 where a
    different character has been randomized each time from the
    original expression. There is a rate percent chance of any
    one character to be changed
    """

    # Optimize using static types
    cdef double rate = rt
    cdef double multiplier

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
            multiplier = 1 / score

        # decide whether to mutate or not
        if random.random() <= rate * multiplier:
            mutated = True

            if i % 2 == 0:
                alt_exp = (alt_exp[:i] +
                           str(random.randint(1, 9)) +
                           alt_exp[i + 1:])
            else:
                alt_exp = (alt_exp[:i] +
                           random.choice(operators) +
                           alt_exp[i + 1:])

            if round(eval(alt_exp)) == target:
                return mutation

    if mutated:
        mutation = [alt_exp]
        mutation.append(expression + ' = ' +
                        str(round(eval(expression))) + ' -> ' +
                        alt_exp + ' = ' + str(round(eval(alt_exp))))

    return mutation
