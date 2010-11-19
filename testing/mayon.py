"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Mayon 2000 (VEI3_eruption)                                                                    
Run Date: 2010_05_18           
Run number:1                                                                                   

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'vertical wind test'

# Time (Volcanological input file)
#Eruption_Year = 2000                            # YYYY  
#Eruption_Month = 2                              # MM  
#Eruption_Day = 24                               # DD 
#Start_time_of_meteo_data = 0                    # Hours after 00
#Meteo_time_step = 60                            # Mins       
#End_time_of_meteo_data = 10                      # Hours after 00
#Start_time_of_eruption = [0.5, 1.75, 2, 2.20]                  # Hours after 00
#End_time_of_eruption = 2.5                        # Hours after 00 
#End_time_of_run = 10                             # Hours after 00  

# Temporal parameters (hours)
eruption_start = 0.5
eruption_duration = 2 
post_eruptive_settling_duration = 7.5


# Location (Volcanological input file)
X_coordinate_of_vent = 574207                   # UTM zone implied by topography projection 
Y_coordinate_of_vent = 1465567                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
Z_min = 0.0
Z_max = 10000
Z_increment = 1000

# Select meteorological input
wind_profile = 'mayon_wind.profile'

# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 7
Mean_grainsize = 2.5                              # phi
Sorting = 1
Minimum_grainsize = -1                          # phi
Maximum_grainsize = 6                           # phi
Density_minimum = 1000                          # kg/m3
Density_maximum = 2600                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 2462
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 'estimate'                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = [3000, 7000, 2000, 7000] # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
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
Vertical_turbulence_model = 'constant'        # Possibilites are CONSTANT/SIMILARITY
Horizontal_turbulence_model = 'constant'            # Possbilities are CONSTANT/RAMS
Vertical_diffusion_coefficient = 100            # m2/s
Horizontal_diffusion_coefficient = 1000         # m2/s
Value_of_CS = 0.1                               # RAMS only

# Output (Volcanological input file)
Postprocess_time_interval = 0.5                   # Hours
Postprocess_3D_variables = 'No'                 # Yes/No
Postprocess_classes = 'No'                      # Yes/No
Track_points = 'No'                             # Yes/No

Topography_grid = 'mayon_topography.txt'        # Specify ASCII topography grid to use. 
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)         

# Contouring:
#   False: Disabled
#   True: Provide a fixed number of contours covering entire range
#   Number: Fixed (vertical) interval between contours
#   List of numbers: Exact contour levels
Thickness_contours = True   # True, False, number or list of numbers
Thickness_units = 'cm'                          # mm/cm/m

Load_contours = True                            # True, False, number or list of numbers                                                 


                                                
# Run model using specified parameters
if __name__ == '__main__':

    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=True,    
                 dircomment=Eruption_comment)

                
                     


 



