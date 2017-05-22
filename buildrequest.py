'''
input: two dictionaries with plinfo and route info
output:a dictionary with the biggest box and total volume of the pl object, origin and destination.
'''

def buildrequest(plinfo, routeinfo, extradistance, productline):
    request = {}
    request["biggest_box"] = plinfo["biggest_case"]
    request["total_weight"] = plinfo["total_weight"]
    request["total_volume"] =  plinfo["total_volume"]
    request["origin"]=routeinfo["origin"]
    request["destination"]=routeinfo["destination"]
    request["extradistance"]= extradistance
    request["productline"]=productline

    return request