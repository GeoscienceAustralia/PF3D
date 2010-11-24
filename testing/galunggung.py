"""Configuration file for eruption scenario                 

Scenario Name: Mount Galunggung                                        
This scenario is based on the observed eruptive characteristics of the 1982 Mount Galunggung eruption in West Java, Indonesia. The eruption date is present day and the wind profile is extracted from NCEP global meterological data Jan 31 2009 - Feb 2 2009.     

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'galunggung test temporal'

# Temporal parameters (hours)
eruption_start = 12
eruption_duration = 6 
post_eruptive_settling_duration = 6

# Location (Volcanological input file)
x_coordinate_of_vent = 176267                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9197056                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 10000
z_increment = 1000

# Meteorological input: Either path to profile or web site with forecast data
wind_profile = 'galunggung_wind_013100-020218.profile'

# Terrain model for model domain (pathway to topography data)
topography_grid = 'galunggung_topography.txt'   # Specify ASCII topography grid to use. 

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
vent_height = 2168
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 'estimate'                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 9000 # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 5                                           # (suzuki only)
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
thickness_contours = True                       
load_contours = True                            

thickness_units = 'cm'                          # mm/cm/m


# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    
    run_scenario(__file__)


 





