# coding: utf-8

from __future__ import print_function

def insertion_cost(base):
    return 1

def substitution_cost(base1, base2):
    return 1 if base1 != base2 else 0

def init_costs(len1, len2):
    return [ [ 0 for j in xrange(len2 + 1)] for i in xrange(len1 + 1)]

def phase1(adn1, adn2):
    len1 = len(adn1)
    len2 = len(adn2)
    costs = init_costs(len1, len2)

    for c in xrange(len1 + len2 + 1):
        for i in xrange(c + 1):
            j = c - i
            if 0 <= i <= len1 and 0 <= j <= len2:
#                print("i=", i, "j=", j)
                if i == 0 and j == 0:
                    costs[i][j] = 0
                elif j == 0:
                    costs[i][j] = costs[i-1][j] + insertion_cost(adn1[i-1])
                elif i == 0:
                    costs[i][j] = costs[i][j-1] + insertion_cost(adn2[j-1])
                else:
                    costs[i][j] = min(
                        costs[i-1][j-1] + substitution_cost(adn1[i-1], adn2[j-1]),
                        costs[i][j-1] + insertion_cost(adn2[j-1]),
                        costs[i-1][j] + insertion_cost(adn1[i-1]))
    return costs

def distance(adn1, adn2):
    return phase1(adn1, adn2)[-1][-1]

import sys
def main():
    if len(sys.argv) == 1:
        dimension = 2000
    else:
        dimension = int(sys.argv[1])
    a = dimension * 'a'
    b = dimension * 'b'
    print(distance(a, b))

main()
