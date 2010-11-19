"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Pinatubo 1991                                                                    
Run Date: 1991_06_15           
Run number:1                                                                                   

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'vertical wind test'

# Time (Volcanological input file)
#Eruption_Year = 1991                            # YYYY  
#Eruption_Month = 6                              # MM  
#Eruption_Day = 15                               # DD 
#Start_time_of_meteo_data = 0                    # Hours after 00
#Meteo_time_step = 60                            # Mins       
#End_time_of_meteo_data = 12                     # Hours after 00
#Start_time_of_eruption = 0                      # Hours after 00
#End_time_of_eruption = 12                       # Hours after 00 
#End_time_of_run = 12                            # Hours after 00  

# Temporal parameters (hours)
eruption_start = 0
eruption_duration = 12 
post_eruptive_settling_duration = 0

# Location (Volcanological input file)
X_coordinate_of_vent = 215212                   # UTM zone implied by topography projection 
Y_coordinate_of_vent = 1676536                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
Z_min = 0.0
Z_max = 40000
Z_increment = 10000

# Meteorological input: Either pathway to profile (single file or directory with multiple files in case of hazard maps) or web site with forecast data)
wind_profile = 'pinatubo_wind.profile'

# Terrain model for model domain (pathway to topography data)
Topography_grid = 'pinatubo_topography.txt'   # Specify ASCII topography grid to use. 
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)   

# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 6
Mean_grainsize = 1.5                            # phi
Sorting = 2
Minimum_grainsize = 1                           # phi
Maximum_grainsize = 6                           # phi
Density_minimum = 1000                          # kg/m3
Density_maximum = 2500                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 1486
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 1e9                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = [30000, 20000, 10000, 5000, 2000, 1000] # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 5                                           # (suzuki only)
Height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e7                               # kg/s (plume only)
MFR_maximum = 1e9                               # kg/s (plume only) 
Exit_velocity = 100                             # m/s (plume only)
Exit_temperature = 1073                         # K (plume only)
Exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
Terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
Vertical_turbulence_model = 'similarity'        # Possibilites are CONSTANT/SIMILARITY
Horizontal_turbulence_model = 'rams'            # Possbilities are CONSTANT/RAMS
Vertical_diffusion_coefficient = 100            # m2/s
Horizontal_diffusion_coefficient = 1000         # m2/s
Value_of_CS = 0.1                               # RAMS only 

# Contouring: True, False, number or list of numbers    
Thickness_contours = True                       
Load_contours = True                            

Thickness_units = 'cm'                          # mm/cm/m

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=True,    
                 dircomment=Eruption_comment)


