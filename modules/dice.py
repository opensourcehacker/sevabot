#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A dice roll module
"""
import sys
import random

progname = 'dice'


def to_int(s):
    """Convert string to integer safely."""

    try:
        v = int(s)
    except ValueError:
        print '{} is not an integer.'.format(s)
        sys.exit(1)

    return v


def to_float(s):
    """Convert string to float safely."""

    try:
        v = float(s)
    except ValueError:
        print '{} is not a number.'.format(s)
        sys.exit(1)

    return v


def main(args):
    """The program entry point."""

    random.seed()

    if len(args) <= 0:
        # Roll a six-sided dice
        print random.randint(1, 6)
        return

    cmd = args[0]

    if cmd == 'help':
        print 'Usage:'
        print '       !dice [sides]'
        print '       !dice [min] [max]'
        print '       !dice uniform [min] [max]'
        print '       !dice gauss [mu] [sigma]'
        return
    elif cmd == 'uniform':

        # Roll a uniform-random-floating-point-numbered dice

        if len(args) <= 1:
            min_val, max_val = 0.0, 1.0
        elif len(args) == 2:
            min_val = 0.0
            max_val = to_float(args[1])
        else:
            min_val = to_float(args[1])
            max_val = to_float(args[2])

        print '{:.4f}'.format(random.uniform(min_val, max_val))

        return
    elif cmd == 'gauss':

        # Roll a Gaussian-distributed dice

        if len(args) <= 1:
            mu, sigma = 0.0, 1.0
        elif len(args) == 2:
            mu = 0.0
            sigma = to_float(args[1])
        else:
            mu = to_float(args[1])
            sigma = to_float(args[2])

        print '{:.4f}'.format(random.gauss(mu, sigma))

        return
    else:

        if len(args) <= 1:
            # Roll an N-sided dice
            sides = to_int(args[0])
            if sides < 1:
                print 'The number of sides must be greater than 0.'
                sys.exit(1)

            print random.randint(1, sides)
            return
        else:

            # Roll an integer dice
            min_val = to_int(args[0])
            max_val = to_int(args[1])
            if min_val > max_val:
                temp_val = min_val
                min_val = max_val
                max_val = temp_val

            print random.randint(min_val, max_val)
            return


if __name__ == '__main__':
    main(sys.argv[1:])
