'''
input: a path to a packing list
output: dictionary with the biigest box weight and the total weight of the pl
'''
from PL import PL

def readpl(path):
    plinfo = {}
    pl = PL(path)

    # get the biggest box
    maxweight = 0
    for item in pl.items_list:
        if item.gross_weight > maxweight:
            maxweight = item.gross_weight

    plinfo["biggest_case"]=maxweight
    plinfo["total_volume"]=pl.volume

    return plinfo


if __name__ == '__main__':
    print readpl("D:/myScripts/transportCalculator/sample/0Y02181600010YHWA03K with price.xlsx")