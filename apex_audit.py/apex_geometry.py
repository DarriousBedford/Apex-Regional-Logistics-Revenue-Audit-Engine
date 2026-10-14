import math


PALLET_CAPACITY = 48 # cartons per pallet
# finds the straight line route distance with the hypot anddouble checks with sqrt
def route_distance(dx, dy):
    distance = math.hypot(dx, dy)
    check = math.sqrt(dx**2 + dy**2)
    return distance, check
# finds the compass angle of a route from its x and y distances
def route_bearing(dx, dy):
    return math.degrees( math.atan(dy / dx))
# finds a loading ramp's angles from its height and the length
def ramp_angles(rise, run, length):
    angle1 = math.degrees( math.asin(rise / length))
    angle2 = math.degrees( math.acos(run / length))
    return angle1, angle2
# breaks a ramp angle into its sine cosine and tangent parts
def ramp_components(length, incline_degrees):
    radians = math.radians(incline_degrees)
    rise = length * math.sin(radians)
    run = length * math.cos(radians)
    slope = math.tan(radians)
    return rise, run, slope
# finds the floor area of a round turntable
def turntable_area(radius):
    return math.pi * radius**2
# finds how many pallets a carton count is going to need rounding up so nothing is left out and gets clean numbers
def pallets_needed(cartons):
    return math.ceil( cartons / PALLET_CAPACITY)
# Finds how many completly full trucksloads the pallets make
def full_truckloads(pallets):
    return math.floor( pallets / 26)
# projects growth that compounds over time
def continuous_growth(value, rate, years):
    return value * math.exp(rate * years)
# finds how long it takes an amount to double its growth rate
def doubling_time(rate):
    return math.log(2) / rate
# finds the order of magnitude
def revenue_magnitude(value):
    return math.log10(value)
    # runs every function
def self_test():
    print(f'Module name: {__name__}')
    print('route_distance(3, 4):', route_distance(3, 4))
    print('route_bearing(1, 1):', route_bearing(1, 1))
    print('ramp_angles(3, 4, 5):', ramp_angles(3, 4, 5))
    print('ramp_components(10, 30):', ramp_components(10, 30))
    print('turntable_area(10):', turntable_area(10))
    print('pallets_needed(100):', pallets_needed(100))
    print('full_truckloads(60):', full_truckloads(60))
    print('continuous_growth(100, 0.05, 2):', continuous_growth(100, 0.05, 2))
    print('doubling_time(0.07):', doubling_time(0.07))
    print('revenue_magnitude(1000):', revenue_magnitude(1000))


if __name__ == '__main__':
    self_test()
