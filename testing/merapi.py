"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Merapi 2010 (probabilistic_scenario)                                                                    
Run Date: 2010_11_01           
Run number:1                                                                                   

Eruption observation details: 

This is to simulate a VEI 2 eruption of Mount Merapi using a strong easterly wind field. The eruption column height will be 9km, a generalised grainsize profile for Vulcanican style eruptions will be used and the underlyig DEM will be 150x150 @ 1342resolution radial around the vent. Seasonal wind conditions for November-December will be used for the period 2000-2009. The output will be used to generate a hazard maps for probability of exceedence of volcanic ash load (0.1, 90, 150 and 300kg/m2).  
"""

# Short eruption comment to appear in output directory.
eruption_comment = 'merapi test temporal'

# Temporal parameters (hours)
eruption_start = 12
eruption_duration = 6 
post_eruptive_settling_duration = 12

# Location (Volcanological input file)
x_coordinate_of_vent = 439423                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9167213                  # UTM zone implied by topography projection

# Vertical discretisation for model domain
z_min = 0.0
z_max = 20000
z_increment = 5000

# Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'merapi_wind_102700-102918.profile'

# Terrain model for model domain (path to topography data)
topography_grid = 'merapi_topography.txt'   # Specify ASCII topography grid to use. 

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 6
mean_grainsize = -2                            # phi
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
mass_eruption_rate = 'estimate'                 # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 15000	     	        # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 1                                           # (suzuki only)
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
thickness_contours = [1, 2, 5, 10, 30, 50, 80, 100]                       
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__)





 



