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

def calculator(basic_data):

    #read the pl
    plinfo = readpl(basic_data["path"])

    #build the request
    request = buildrequest(basic_data, plinfo)

    #send the request to flexnet calculator
    flexnet_cost = flexnetprice.calculate(request)

    print flexnet_cost
    return flexnet_cost

if __name__ == '__main__':
    calculator({})
