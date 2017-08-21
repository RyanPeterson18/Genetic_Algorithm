import random
import math
import time
import pandas as pd


def calc_scores(expressions, target):
    """
    Calculates the fitness score based on it's proximity to the
    target

    NOTE: it also signals to end the program if it equals the target value
    """

    scores = []
    values = []

    for expression in expressions:

        value = eval(expression)

        if round(value) == target:
            return True, expression
        else:
            scores.append(1 / abs(target - value))
            values.append(value)

    return scores, values


def mutate(expression, double rate_cap, double rate_constant, double value, double max_exponent, operators, int target, out_data):
    """
    Creates a list with len(list) <= len(expression) + 1 where a
    different character has been randomized each time from the
    original expression. There is a rate percent chance of any
    one character to be changed
    """

    cdef double rate

    mutation = [expression]
    mutated = False
    alt_exp = expression

    for i in range(len(expression)):

        try:
            # prevent OverflowError by
            exponent = -(rate_constant / target) * (value)
            if exponent > max_exponent:
                exponent = max_exponent
            elif exponent < -max_exponent:
                exponent = -max_exponent
            # Calculate the actual mutation rate based on the expression's proximity
            # r = c - (c / (1 + c*e^(-(k/t)*x)))
            # math.exp(x) is e**x
            rate = rate_cap - (rate_cap / (1 + rate_cap *
                                           math.exp(exponent)))
        except OverflowError:
            print("rate_cap:", rate_cap, "\nrate_constant:",
                  rate_constant, "\ntarget:", target, "\nvalue:", value)
            raise OverflowError("math range error at gen_alg_module.pyx:50")

        # decide whether to mutate or not
        if random.random() <= rate:
            mutated = True

            # mutate
            if i % 2 == 0:
                alt_exp = (alt_exp[:i] +
                           str(random.randint(1, 9)) +
                           alt_exp[i + 1:])
            else:
                alt_exp = (alt_exp[:i] +
                           random.choice(operators) +
                           alt_exp[i + 1:])

            if round(eval(alt_exp)) == target:
                return [alt_exp]

    if mutated:
        mutation = [alt_exp]
        mutation.append(expression + ' = ' +
                        str(round(eval(expression))) + ' -> ' +
                        alt_exp + ' = ' + str(round(eval(alt_exp))))

    return mutation
