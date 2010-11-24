"""Script for aim to generate hazard map from multiple Fall3D output files

This script is a template for  
"""

# Vent location in geographic coordinates (decimal degrees) of the Guntur crater
vent_easting = 439423
vent_northing = 9167213
vent_zone = 49
vent_hemisphere = 'S'

# Question for ADELE - should we do all possible variables or specify them here as in the inp file?

# Values
load_values = [0.1, 10, 20, 50, 90, 150, 300] 
fl_values = [0.0002, 0.002]

# Contours
ISOCHRON_contours = True
ISOCHRON_units = 'h'
PLOAD_contours = True
PLOAD_units = 'pct'

# Location of generated windprofiles, hazard map and contours
model_output_directory = '/model_area/sandpits/bearad/aim/testing/guntur_multiple_wind_template_outputs'

#--------------------------------------
if __name__ == '__main__':
    from aim import generate_hazardmap
    generate_hazardmap(__file__)
