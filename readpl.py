'''
input: a path to a packing list
output: dictionary with the biigest box weight, total volume and the total weight of the pl
'''
from PL import PL

def readpl(app, path):
    plinfo = {}
    pl = PL(path, app)

    # get the biggest box
    maxweight = 0
    for item in pl.items_list:
        if item.gross_weight > maxweight:
            maxweight = item.gross_weight

    plinfo["biggest_case"]=maxweight
    plinfo["total_volume"]=float(pl.volume)
    plinfo["total_weight"]=float(pl.gross_weight)
    pl.workbook.Close()
    return plinfo


if __name__ == '__main__':
    print readpl("D:/myScripts/transportCalculator/sample/0Y02181600010YHWA03K with price.xlsx")