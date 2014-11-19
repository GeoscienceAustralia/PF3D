"""

volcano (foreast) template                                                                    
                                                                                   
This template is for running single scenarios using wind profiles converted from the Australian Bureau of Meteorology's ACCESS-R regional wind data model. Copy this template script into the modelling area, rename and edit as needed. 

Important: BEFORE RUNNING THIS SCRIPT YOU MUST:

	1. Manually download ACCESS-R data (in netCDF4 format) for the forecast period required (up to 72 hours). Refer to manual for instructions. 
	2. Convert ACCESS-R data (from netCDF4) to fall3d wind profile using /pf3d/fall3d_v6/source/auxilliary_scripts/convert_access_2_windprofile.py. Refer 		to manual for instructions.    

To run:

python volcano_forecast.py 

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'volcano forecast'

# Temporal parameters (hours)
eruption_start = 2
eruption_duration = 2 
post_eruptive_settling_duration = 4

# Location (Volcanological input file)
x_coordinate_of_vent = 439423                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9167213                  # UTM zone implied by topography projection

# Vertical discretisation for model domain
z_min = 0.0
z_max = 50000
z_increment = 10000

# Meteorological input
wind_profile = '/path/to/forecast/wind/profile'	# Path to forecast wind profile (e.g. /tephra/wind/IDY25300.YYYYMMDD.HHH.proifle)

# Terrain model 
topography_grid = '/path/to/topography'		# Path to topography file (e.g. /tephra/dems/guntur_topography.txt)

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 6
mean_grainsize = 2.5                            # phi
sorting = 1.5
minimum_grainsize = 4                           # phi
maximum_grainsize = -4                           # phi
density_minimum = 1200                          # kg/m3
density_maximum = 2300                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 2968
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 'estimate'                 # kg/s (if point, if suzuki or if plume where height_or_mfr = mfr)
height_above_vent = [20000] 			# m (if point, if suzuki or if plume where height_or_MFR = Height)            
A = 3                                       	# (suzuki only)            
L = 1                                       	# (suzuki only)
height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e7                               # kg/s (plume only)
MFR_maximum = 1e9                               # kg/s (plume only) 
exit_velocity = 100                             # m/s (plume only)
exit_temperature = 1073                         # K (plume only)
exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
vertical_turbulence_model = 'similarity'        # Possibilites are CONSTANT/SIMILARITY
horizontal_turbulence_model = 'rams'            # Possbilities are CONSTANT/RAMS
vertical_diffusion_coefficient = 100            # m2/s
horizontal_diffusion_coefficient = 1000         # m2/s
value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
thickness_contours = [1, 2, 5, 10, 20, 50, 100] # Options: 'True', 'False' or [1, 2] (a list of contour values)         
load_contours = [0.1, 90, 150, 300]             # Options: 'True', 'False' or [1, 2] (a list of contour values)         

thickness_units = 'cm'                          # mm/cm/m


# Run model using specified parameters
if __name__ == '__main__':

    import time, random
    from aim import run_scenario
    
    run_scenario(__file__, 
                 timestamp_output=True)    



 



