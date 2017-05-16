'''
determines the truck type based on cubic meters
returns a tuple with the qyt of trucks and the type
'''

import math

def select(cbm):

    if cbm <= 4.09:
        return [(1, "T1")]

    elif cbm <= 17.89:
        return [(1, "T2")]

    elif cbm <= 34.56:
        return [(1, "T3")]

    else:
        t3 = cbm/34.56
        remainder = (t3 - math.floor(t3))*34.56

        n_t3 = (int(math.floor(t3)), "T3")
        n_remainder = select(remainder)

        return  [n_t3, n_remainder]


if __name__ == '__main__':
    print select(80)
