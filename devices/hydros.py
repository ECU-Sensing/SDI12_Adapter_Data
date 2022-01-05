    """ Main class for the Hydros 21 / Decagon CDT-10 water sensors

        Intended to be used with the LoRa transmission driver code

        Author: Colby Sawyer 1-5-2022

    """
class Hydros:
    water_depth = 0
    temperature = 0
    electrical_conductivity = 0

    def __init__(self, water_depth, temperature, conductivity):
        self.water_depth = water_depth
        self.temperature = temperature
        self.electrical_conductivity = conductivity

    def get_data(self):
        sensor_data = bytearray(7)
        FEATHER_ID = 1

        depth_val = int(self.water_depth)
        print("Water Depth: %0.1f %%" % depth_val)

        temp_val = int(self.temperature)
        print("Temperature: %0.1f %%" % depth_val)

        conduc_val = int(self.electrical_conductivity)
        print("Conductivity: %0.1f %%" % depth_val)

        sensor_data[0] = FEATHER_ID
        # Water Depth
        sensor_data[1] = (depth_val >> 8) & 0xff
        sensor_data[2]= depth_val & 0xff
        # Temperature
        sensor_data[3] = (temp_val >> 8) & 0xff
        sensor_data[4] = temp_val & 0xff
        #Conductivity
        sensor_data[5] = (conduc_val >> 8) & 0xff
        sensor_data[6] = conduc_val & 0xff

        return sensor_data
