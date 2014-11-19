"""                 

volcano (single wind) template                                                                    
                                                                                   
This template is for running single wind scenarios. Copy this template script into the modelling area, rename and edit as needed. 
The user must point to a single wind profile (i.e. 'guntur_wind_013000-020218.profile'). If the profile does not sit locally with the script the path must be provided.

To run:

python volcano.py

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'single wind template'

# Temporal parameters (hours)
eruption_start = 0
eruption_duration = 6 
post_eruptive_settling_duration = 0

# Location (Volcanological input file)
x_coordinate_of_vent = 439423                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9167213                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 10000
z_increment = 1000

# Meteorological input
wind_profile = '/path/to/wind/profile'		# Path to wind profile (e.g. /tephra/wind/guntur_2014/guntur.profile)

# Terrain model 
topography_grid = '/path/to/topography'      	# Path to topography file (e.g. /tephra/dems/guntur/guntur_topography.txt)  

# Granulometry 
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 6
mean_grainsize = 2.5                            # phi
sorting = 1.5
minimum_grainsize = 0                           # phi
maximum_grainsize = 5                           # phi
density_minimum = 1000                          # kg/m3
density_maximum = 2500                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source 
vent_height = 2249 
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 'estimate'                 # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 9000			# m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 5                                           # (suzuki only)
height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e7                               # kg/s (plume only)
MFR_maximum = 1e9                               # kg/s (plume only) 
exit_velocity = 100                             # m/s (plume only)
exit_temperature = 1073                         # K (plume only)
exit_volatile_fraction = 0                      # % (plume only)

# Fall3D 
terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
vertical_turbulence_model = 'similarity'        # Possibilites are CONSTANT/SIMILARITY
horizontal_turbulence_model = 'rams'            # Possbilities are CONSTANT/RAMS
vertical_diffusion_coefficient = 100            # m2/s
horizontal_diffusion_coefficient = 1000         # m2/s
value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
thickness_contours = True                       # Options: 'True', 'False' or [1, 2] (a list of contour values)  
load_contours = True                            # Options: 'True', 'False' or [1, 2] (a list of contour values)

thickness_units = 'cm'                          # mm/cm/m

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__)



    
 



