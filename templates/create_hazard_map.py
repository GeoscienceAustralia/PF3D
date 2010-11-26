"""Script for aim to generate hazard map from multiple Fall3D output files

This template is for generating a volcanic ash hazard map using multiple FALL3D output files. The contours represent proabability (%) of exceeding a particular ash load threshold (i.e 1kg/m2). One hazard is produed for eah load threshold specified.
    
"""

# Vent location in geographic coordinates (decimal degrees)
vent_easting = 439423
vent_northing = 9167213
vent_zone = 49
vent_hemisphere = 'S'

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
