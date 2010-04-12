"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Mayon 2000 (Actual eruption - VEI3)                                                                    
Run Date:             
Run number:R1                                                                                   

Eruption observation details:
"""

# Short eruption comment to appear in output directory.
Eruption_comment = ''

# Time (Volcanological input file)
Eruption_Year = 2000                            # YYYY  
Eruption_Month = 2                              # MM  
Eruption_Day = 28                               # DD 
Start_time_of_run = 0                           # Hours after 00
End_time_of_eruption = 6                       # Hours after 00 
End_time_of_run = 6                            # Hours after 00  

# Fall3D (Volcanological input file)
Terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
Vertical_turbulence_model = 'similarity'        # Possibilites are CONSTANT/SIMILARITY
Horizontal_turbulence_model = 'rams'            # Possbilities are CONSTANT/RAMS
Vertical_diffusion_coefficient = 100            # m2/s
Horizontal_diffusion_coefficient = 1000         # m2/s
Post_process_time_interval = 1                  # Hours

# Granulometry (Volcanological input file)
Number_of_grainsize_classes = 6
Mean_grainsize = 1.0                            # phi
Minimum_grainsize = -4                          # phi
Maximum_grainsize = 4                           # phi
Sorting = 1.0
Density_minimum = 2350                          # kg/m3
Density_maximum = 3300                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Meteorological database (Volcanological input file)
Year = 2000                                     # Of meteo data
Month = 2                                       # Of meteo data
Day = 28                                        # Of meteo data
Start_time_of_meteo_data = 0                    # Hours after 00
End_time_of_meteo_data = 6                      # Hours after 00
Hours_between_meteo_data_blocks = 1             # Hours

Z_layers = [100, 250, 500, 5000, 1000, 5000, 7500, 12000] # List Z layers in increasing height order (meters; i.e.[100, 500, 1000, 5000, etc])

# Source (Volcanological input file)  
Vent_location_X_coordinate =  574207                  # UTM refer to GoogleEarth (convert to UTM)
Vent_location_Y_coordinate =  1465567                  # UTM refer to GoogleEarth (convert to UTM)
Mass_eruption_rate = 1e6                        # kg/s
Source_type = 'plume'                           # Options are 'plume', 'suzuki', 'point'
Height_above_vent = 0                           # m (suzuki and point only)            
A = 0                                           # (suzuki only)            
L = 0                                           # (suzuki only)            
Exit_velocity = 100                             # m/s (plume only)
Exit_temperature = 1073                         # K (plume only)
Exit_volatile_fraction = 0                      # % (plume only)

# Post-Processing (Volcanological input file)
Output_results_in_GRD_format = 'No'                                # Yes/No                                                        
Output_results_in_PS_format = 'Yes'                                 # Yes/No                                                        

Map_total_load = 'Yes'                                               # Yes/No (mass per unit area)                                                      
Load_contours = [0.1, 0.25, 0.5, 1, 5, 10, 50]                      # List contour intervals (PS format only)

Map_class_load = 'No'                                               # Yes/No (mass per unit area for each grainsize)                                
Class_load_contours = [0.1, 0.25, 0.5, 1, 5, 10, 50]                # List contour intervals (PS format only)

Map_deposit_thickness = 'Yes'                                       # Yes/No                                        
Map_thickness_units = 'cm'                                          # Possibilities (mm, cm, m)
Map_thickness_compaction_factor = 0.7                               # Degree of compaction (i.e. 0.7)
Thickness_contours = [0.1, 1, 5, 10, 50, 100, 500]                  # List contour intervals (PS format only)

Map_total_concentration = 'No'                                      # Yes/No                                
Map_total_concentration_z_cuts = [1000, 2000]                       # List height in meters of each z-cut required (i.e. 1000 2000)
Total_concentration_contours = [1e-5, 1e-4]                         # List contour intervals (PS format only)

Map_z_cummulative_concentration = 'No'                              # Yes/No                        
Cummulative_concentration_contours = [0.01, 0.1, 1, 10]             # List contour intervals (PS format only)
 
Map_Z_maximum_concentration = 'No'                                  # Yes/No                                                
Maximum_concentration_contours = [1e-4, 1e-3]                       # List contour intervals (Ps format only)


Fixed_contour_interval = 1                                          # Contour interval for kml and shp files
Topography_grid = ''                                                # Specify ASCII topography grid to use. 
                                                                    # If empty, AIM will look for a topography grid named
                                                                    # <scenario_name>_topography.txt         

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario, get_scenario_parameters
    
      
    # Get parameters specified in scenario_file
    params = get_scenario_parameters(__file__)    
    
    # Run scenario
    run_scenario(params, dircomment=Eruption_comment)


 



