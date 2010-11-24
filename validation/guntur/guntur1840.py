"""Configuration file for eruption scenario

Scenario Name: Mount Guntur 1840 (Validation scenario)                                                                    

This scenario was developed in July 2010 to validate AIM/Fall3d-6.2 against observed ash thicknesses from the Guntur 1840 eruption by

Adele Bear-Crozier
Anjar Heriwaseso
Nugraha Kartadinata
Antonio Costa
Arnau Folch
Ole Nielsen
Kristy Vanputten

at a workshop held at the Ausralia-Indonesia Facility for Disaster Reduction, Jakarta.

The ash thickness observations were collected by N. Kartadinata and published internally at PVMBG. 

Running the scenario and comparing model outputs produced with the stored model outputs serves to verify that the installation of AIM/FALL3D-6.2 works as intended.
To run:

python guntur1840.py

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'guntur_1840_validation'

# Temporal parameters (hours)
eruption_start = 0
eruption_duration = 5 
post_eruptive_settling_duration = 0

# Location (Volcanological input file)
x_coordinate_of_vent = 814924                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9208168                  # UTM zone implied by topography projection

# Vertical discretisation for model domain
z_min = 0.0
z_max = 10000
z_increment = 1000

# Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'guntur1840_wind.profile'

# Terrain model for model domain (pathway to topography data)
topography_grid = 'guntur1840_topography.txt'   # Specify ASCII topography grid to use. 

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 8
mean_grainsize = -1.5                           # phi
sorting = 2
minimum_grainsize = -4                          # phi
maximum_grainsize = 3                        	# phi
density_minimum = 1200                          # kg/m3
density_maximum = 2500                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 2250
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 3e6                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 8000                        # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 1                                           # (suzuki only)
height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e6                               # kg/s (plume only)
MFR_maximum = 2e6                               # kg/s (plume only) 
exit_velocity = 100                             # m/s (plume only)
exit_temperature = 1073                         # K (plume only)
exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
vertical_turbulence_model = 'constant'          # Possibilites are CONSTANT/SIMILARITY
horizontal_turbulence_model = 'constant'        # Possbilities are CONSTANT/RAMS
vertical_diffusion_coefficient = 100            # m2/s
horizontal_diffusion_coefficient = 1000         # m2/s
value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
thickness_contours = [1, 2, 5, 10, 25, 50, 75, 100]  
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m


# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=False,    
                 store_locally=True)




