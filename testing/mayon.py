"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Mayon 2000 (VEI3_eruption)                                                                    
Run Date: 2010_05_18           
Run number:1                                                                                   

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'mayon test temporal'

# Temporal parameters (hours)
eruption_start = 0.5
eruption_duration = 2 
post_eruptive_settling_duration = 7.5

# Location (Volcanological input file)
x_coordinate_of_vent = 574207                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 1465567                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 10000
z_increment = 1000

# Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'mayon_wind.profile'

# Terrain model for model domain (pathway to topography data)
topography_grid = 'mayon_topography.txt'   # Specify ASCII topography grid to use. 

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 7
mean_grainsize = 2.5                              # phi
sorting = 1
minimum_grainsize = -1                          # phi
maximum_grainsize = 6                           # phi
density_minimum = 1000                          # kg/m3
density_maximum = 2600                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 2462
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 'estimate'                 # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 7000 			# m (if point, if suzuki or if plume where Height_or_MFR = Height)            
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
vertical_turbulence_model = 'constant'        # Possibilites are CONSTANT/SIMILARITY
horizontal_turbulence_model = 'constant'            # Possbilities are CONSTANT/RAMS
vertical_diffusion_coefficient = 100            # m2/s
horizontal_diffusion_coefficient = 1000         # m2/s
value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
thickness_contours = True                       
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m

                                                
# Run model using specified parameters
if __name__ == '__main__':

    from aim import run_scenario
    run_scenario(__file__)

                
                     


 



