"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Merapi 2010 (probabilistic_scenario)                                                                    
Run Date: 2010_11_01           
Run number:1                                                                                   

Eruption observation details: 

This is to simulate a VEI 2 eruption of Mount Merapi using a strong easterly wind field. The eruption column height will be 9km, a generalised grainsize profile for Vulcanican style eruptions will be used and the underlyig DEM will be 150x150 @ 1342resolution radial around the vent. Seasonal wind conditions for November-December will be used for the period 2000-2009. The output will be used to generate a hazard maps for probability of exceedence of volcanic ash load (0.1, 90, 150 and 300kg/m2).  
"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'VEI2_9km_nov_dec'

# Time (Volcanological input file)
Eruption_Year = 2010                            # YYYY  
Eruption_Month = 11                             # MM  
Eruption_Day = 1                               # DD 
Start_time_of_meteo_data = 6                    # Hours after 00
Meteo_time_step = 360                            # Mins       
End_time_of_meteo_data = 36                      # Hours after 00
Start_time_of_eruption = 12              # Hours after 00
End_time_of_eruption = 18                        # Hours after 00 
End_time_of_run = 30                             # Hours after 00  

# Location (Volcanological input file)
X_coordinate_of_vent = 439423                   # UTM zone implied by topography projection 
Y_coordinate_of_vent = 9167213                  # UTM zone implied by topography projection

# Vertical discretisation for model domain
Z_min = 0.0
Z_max = 15000
Z_increment = 1000

# Select meteorological parameters
wind_profile = '/model_area/tephra/3D_wind/NCEP1/merapi_single_scenario/merapi_single_scenario_021100-021400.profile'
#wind_altitudes = [0, 100, 500, 1000, 5000, 10000, 20000, 30000, 50000] # List Z layers in increasing height order (meters; i.e.[100, 500, 1000, 5000, etc])

# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 6
Mean_grainsize = -2                            # phi
Sorting = 1.5
Minimum_grainsize = 4                           # phi
Maximum_grainsize = -4                           # phi
Density_minimum = 1200                          # kg/m3
Density_maximum = 2300                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 2968
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 'estimate'                 # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = 9000			 # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                       # (suzuki only)            
L = 1                                       # (suzuki only)
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

# Output (Volcanological input file)
Postprocess_time_interval = 1                   # Hours
Postprocess_3D_variables = 'No'                 # Yes/No
Postprocess_classes = 'No'                      # Yes/No
Track_points = 'No'                             # Yes/No

Topography_grid = 'merapi_topography.txt'       # Specify ASCII topography grid to use. 
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)         
                                                
# Contouring:
#   False: Disabled
#   True: Provide a fixed number of contours covering entire range
#   Number: Fixed (vertical) interval between contours
#   List of numbers: Exact contour levels
Thickness_contours = True         # True, False, number or list of numbers
Thickness_units = 'cm'                          # mm/cm/m

Load_contours = True                            # True, False, number or list of numbers    
                                                
# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_multiple_windfields
    run_multiple_windfields(__file__, 
                            windfield_directory='/model_area/tephra/3D_wind/NCEP1/merapi_multiple_wind_2000_2009_VEI2_Nov_Dec',
                            hazard_output_folder='/model_area/tephra/3D_wind/NCEP1/VEI2_9km_outputs',
                            dircomment=Eruption_comment)



 



