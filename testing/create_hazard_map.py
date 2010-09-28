"""Test script for aim to generate hazard map from multiple Fall3D output files
"""

# Vent location in geographic coordinates (decimal degrees) of the Guntur crater
vent_easting = 814924
vent_northing = 9208168
vent_zone = 48
vent_hemisphere = 'S'

# Question for ADELE - should we do all possible variables or specify them here as in the inp file?

# Values
load_values = [1, 10, 100] 
fl_values = [0.0002, 0.002]

# Contours
ISOCHRON_contours = True
ISOCHRON_units = 'h'
PLOAD_contours = True
PLOAD_units = 'pct'

# Location of generated windprofiles, hazard map and contours
model_output_directory = 'guntur_hazard_outputs'

#--------------------------------------
if __name__ == '__main__':
    from aim import generate_hazardmap
    generate_hazardmap(__file__)
