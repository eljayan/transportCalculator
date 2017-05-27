'''
input: a dictionary with the service request (biggest box, weight, volume
origin and destination point)
outpt: a dictionary representing the cost of transportation
'''
import trucktype
import manpower
import forklift
from sqlite3 import connect

def calculate(request):
    transport_cost = 0
    db = connect("db.db")

    origin = request["origin"]
    destination = request["destination"]
    region = request["region"]
    volume = request["total_volume"]
    biggest_case =  request["biggest_case"]
    weight = request["total_weight"]
    extradistance = request.get("extradistance", 0)
    productline = request.get("productline", "")
    stops = request.get("stops", 0)
    if not stops:
        stops = 0

    ttype = trucktype.select(volume)
    mpower = manpower.calculate(biggest_case_weight=biggest_case, total_weight=weight, destination=destination)
    forklift_cost = forklift.calculate(weight,biggest_case, destination)

    distance = db.execute("select distance from distances where origin=? and destination=?", (origin, destination))
    distance = distance.fetchone()[0]

    if extradistance:
        q = db.execute("select price from flexnet_km where ? >= min and ? <= max", (extradistance, extradistance))
        q_price =  q.fetchone()
        extradistance_price = q_price[0]
    else:
        extradistance_price = 0

    for t in ttype:
        query = db.execute("select %s from flexnet where origin = ? and destination = ?" %(t[1].lower()), (origin, destination))
        transport_cost += t[0] * float(query.fetchone()[0])

    mpower_cost = mpower * 55
    stops_cost = int(stops)*0.5*transport_cost

    return {
        "supplier":"flexnet",
        "origin":origin,
        'destination':destination,
        "distance":distance,
        "product line": productline,
        "region": region,
        "extra km": extradistance,
        "stops":stops,
        "truck type":ttype,
        "base transport":transport_cost,
        "add transport":extradistance_price,
        "manpower cost":mpower_cost,
        "forklift":forklift_cost,
        "stops cost": stops_cost,
        "total cost":transport_cost+extradistance_price+mpower_cost+forklift_cost+stops_cost
    }

if __name__ == '__main__':
    r = calculate({"origin":"guayaquil",
               "destination":"quito",
                "region":2,
               "total_volume":3.25,
               "biggest_case":84.3,
               "total_weight":256.38,
               "extradistance" : 100,
                "productline":"wireless",
                "stops": 1
                })

    # print r