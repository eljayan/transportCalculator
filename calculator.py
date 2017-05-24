'''
input: a dictionary of arguments obtained from the GUI{
    path
    origin
    destination
    extradistance
    productline
    stops
}
output: a dictionary with the calculations result
'''

import view
from readpl import readpl
from buildrequest import buildrequest
import flexnetprice

def calculator(basic_data, status):
    results = {}

    #read the pl
    status.set("Reading Packing List...")
    plinfo = readpl(basic_data["path"])

    #build the request
    request = buildrequest(basic_data, plinfo)

    #send the request to flexnet calculator
    status.set("Calculating costs...")
    flexnet_cost = flexnetprice.calculate(request)

    #otro
    results['1'] = flexnet_cost

    print results
    return results

if __name__ == '__main__':
    calculator({})
