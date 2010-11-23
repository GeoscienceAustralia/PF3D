"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Tambora 1815 (VEI 6 eruption)                                                                   
Run Date: 2010_05_06           
Run number:1                                                                                   

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'tambora test temporal'

# Temporal parameters (hours)
eruption_start = 12
eruption_duration = 6 
post_eruptive_settling_duration = 6

# Location (Volcanological input file)
x_coordinate_of_vent = 609511                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9088892                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 50000
z_increment = 10000

#Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'tambora_wind_013100-020218.profile'

# Terrain model for model domain (pathway to topography data)
topography_grid = 'tambora_topography.txt'   # Specify ASCII topography grid to use. 

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 6
mean_grainsize = 2.5                            # phi
sorting = 1.5
minimum_grainsize = 0                           # phi
maximum_grainsize = 5                           # phi
density_minimum = 1200                          # kg/m3
density_maximum = 2300                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 1554.6
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 'estimate'                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 40000			# m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 5                                           # (suzuki only)
height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e7                               # kg/s (plume only)
MFR_maximum = 1e9                               # kg/s (plume only) 
exit_velocity = 100                             # m/s (plume only)
exit_temperature = 1073                         # K (plume only)
exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
terminal_velocity_model = 'ganser'              # Possibilites are arastoopor/ganser/wilson/dellino
vertical_turbulence_model = 'similarity'        # Possibilites are constant/similarity
horizontal_turbulence_model = 'rams'            # Possbilities are constant/rams
vertical_diffusion_coefficient = 100            # m2/s
horizontal_diffusion_coefficient = 1000         # m2/s
value_of_CS = 0.1                               # rams only

# Contouring: True, False, number or list of numbers    
thickness_contours = True                       
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m                                               

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=True,    
                 dircomment=eruption_comment)


 



