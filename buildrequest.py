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
    if isinstance(extradistance, basestring):
        try:
            request["extradistance"]= float(extradistance)
        except:
            request["extradistance"] = 0
    else:
        request["extradistance"] = extradistance

    request["productline"]=productline

    return request


if __name__ == '__main__':
    r = buildrequest({
        "biggest_case":60,
        "total_weight":100,
        "total_volume":0.98},
        {"origin":"guayaquil",
        "destination":"quito"},
        "1200",
        "wireless")

    print r