'''
input: two dictionaries with plinfo and route info
output:a dictionary with the biggest box and total volume of the pl object, origin and destination.
'''

from readpl import readpl

def buildrequest(pl):
    request = {"origin":None,
               "destination":None,
               "biggest_box":None,
               "weight":None}



    #

    request["weight"] = maxweight