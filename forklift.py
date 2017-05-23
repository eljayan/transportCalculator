import math

def calculate(total_weight, biggest_case_weight, destination):
    MAXLOADJOURNEY = 200.00
    MAXBOXWEIGHT = 300.00

    manpower_per_kilograms = int(math.ceil(total_weight / MAXLOADJOURNEY))

    if destination == "guayaquil" or destination == "quito":
        if manpower_per_kilograms > 10:
            # use a forklift
            return 300.00
        elif biggest_case_weight > MAXBOXWEIGHT:
            # use a forklift
            return 300.00
        else:
            return 0
    else:
        return 0

