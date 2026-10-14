FUEL_SURCHARGE = 2.75 # surcharge per trip



class FleetVehicle:
# sets up a new vehicle with a hidden Id capacit and status with 0 miles
    def __init__(self, unit_id, capacity):
        self.__unit_id = unit_id
        self.capacity = capacity
        self.status = 'Available'
        self.miles = 0.0
# hands back the hidden ID 
    def get_unit_id(self):
        return self.__unit_id
# adds a trips miles to the total
    def add_trip(self, miles):
        self.miles += miles
# calculates the mileage pay
    def reimbursement(self):
        return self.miles * 0.58
# controls what print shows
    def __str__(self):
        return f'{self.__unit_id} ({self.status}) {self.miles} mi'
#smaller class to fleet vehicle that has a lift gate
class BoxTruck(FleetVehicle):
# runs the setup
    def __init__(self, unit_id, capacity):
        FleetVehicle.__init__(self, unit_id, capacity)
        self.liftgate = True
        self.trips = []
#record the parent mileageand remebers the length of trip
    def add_trip(self, miles):
        FleetVehicle.add_trip(self, miles)
        self.trips.append(miles)
# shows the liftgate is working
    def operate_liftgate(self):
        print(f'{self.get_unit_id()} liftgate operating')
# overrides the parents pay
    def reimbursement(self):
        total = FleetVehicle.reimbursement(self)
        for trip in self.trips:
            if trip > 150:
                total += FUEL_SURCHARGE
        return total

class CargoVan(FleetVehicle):
    def __init__(self, unit_id, capacity):
        FleetVehicle.__init__(self, unit_id, capacity)
# creates one box truck and cargo van
def build_fleet():
    truck = BoxTruck('BT-101', 26000)
    van = CargoVan('CV-220', 3500)
    truck.add_trip(212.5)
    truck.add_trip(100.0)
    van.add_trip(180.0)
    return [truck, van]
# totals every vehicles pay
def settle_fleet(fleet):
    total_pay = 0.0
    for vehicle in fleet:
        total_pay += vehicle.reimbursement()
        if isinstance(vehicle, BoxTruck):
            print(f'Liftgate inspection scheduled: {vehicle.get_unit_id()}')
        try:
            vehicle.operate_liftgate()
        except AttributeError:
            print(f'{vehicle.get_unit_id()} has no liftgate')
        print(vehicle)
    return total_pay
                   


        
