'''returns the number of manpower needed to handle one box weight'''
import math

def calculate(biggest_case_weight, total_weight, destination):
    '''
    weight_float is the weight of the biggest box
    cases_int is the number of boxes in the shipment
    '''

    #constraints
    MAXLOADPERSON = 35.00
    MAXLOADJOURNEY = 200.00
    MAXBOXWEIGHT = 300.00

    manpower_per_kilograms = int(math.ceil(total_weight / MAXLOADJOURNEY))

    if biggest_case_weight > total_weight:
        raise ValueError ("Box weight can't be higher than total weigth.")

    if manpower_per_kilograms > 10:
        #use a forklift
        return 0
    elif biggest_case_weight > MAXBOXWEIGHT:
        if destination == "guayaquil" or destination == "quito":
        #use a forklift
            return 2
        else:
            peopleneeded = int(math.ceil(biggest_case_weight/MAXLOADPERSON))
            load_per_journey = total_weight/peopleneeded
            if load_per_journey > MAXLOADJOURNEY:
                return int(math.ceil(total_weight/MAXLOADJOURNEY))
            else:
                return peopleneeded

    elif total_weight <= MAXLOADPERSON:
        #if the cases are to small, no manpower
        return 0
    elif biggest_case_weight > MAXLOADPERSON:
        #how many people needed to lift the biggest box
        manpower_per_box = int(math.ceil(biggest_case_weight/MAXLOADPERSON))
        if manpower_per_box > manpower_per_kilograms:
            return manpower_per_box
        else:
            return manpower_per_kilograms
    elif total_weight > MAXLOADJOURNEY:
        #if ther are to many boxes
        return manpower_per_kilograms
    else:
        #one man is enough
        return 1


if __name__ == '__main__':
    print calculate(biggest_case_weight= 450, total_weight= 1200, destination="guayaquil")
