"""Configuration file for eruption scenario

Scenario Name: Tavurvur Volcano 1994 (Validation scenario)                                                                    

This scenario was developed in August 2010 to validate AIM/Fall3d-6.2 against observed ash thicknesses from the 1994 eruption of Tavurvur Volcano, 
East New Britain, Papaua New Guinea by

James Goodwin
Adele Bear-Crozier

at Geoscience Australia, Canberra.

The ash thickness observations were collected within the nearby township of Rabaul (destroyed during the eruption). #FIXME - add reference to literature used 

Running the scenario and comparing model outputs produced with the stored model outputs serves to verify that the installation of AIM/FALL3D-6.2 works as intended.
To run:

python tavurvur.py

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'tavurvur_1994_validation_estimate'

# Temporal parameters (hours)
eruption_start = 0
eruption_duration = 24 
post_eruptive_settling_duration = 2

# Location (Volcanological input file)
x_coordinate_of_vent = 412400                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9531460                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 7000
z_increment = 1000

# Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'tavurvur.profile'

# Terrain model for model domain (pathway to topography data)
topography_grid = 'tavurvur_topography.txt'       # Specify ASCII topography grid to use. 

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 10
mean_grainsize = 0                            # phi
sorting = 2
minimum_grainsize = 3                           # phi
maximum_grainsize = -4                           # phi
density_minimum = 1600                          # kg/m3
density_maximum = 2000                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 688 
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 0.72e6                 # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 6000			# m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 2                                           # (suzuki only)            
L = 5                                           # (suzuki only)
height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e4                               # kg/s (plume only)
MFR_maximum = 1e6                               # kg/s (plume only) 
exit_velocity = 100                             # m/s (plume only)
exit_temperature = 1073                         # K (plume only)
exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
vertical_turbulence_model = 'constant'        # Possibilites are CONSTANT/SIMILARITY
horizontal_turbulence_model = 'constant'            # Possbilities are CONSTANT/RAMS
vertical_diffusion_coefficient = 50            # m2/s
horizontal_diffusion_coefficient = 2500         # m2/s
value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
thickness_contours = [5, 10, 20, 40, 80, 140]                       
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__)



    
 



