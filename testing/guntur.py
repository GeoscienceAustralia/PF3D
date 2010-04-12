"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Guntur                                            
Run Date: 2010_01_14           
Runnumber:Test                                                                                  

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'testing'

# Time (Volcanological input file)
Eruption_Year = 2010                            # YYYY  
Eruption_Month = 1                              # MM  
Eruption_Day = 14                               # DD 
Start_time_of_run = 0                           # Hours after 00
End_time_of_eruption = 5                        # Hours after 00 
End_time_of_run = 5                             # Hours after 00  

# Fall3D (Volcanological input file)
Terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
Vertical_turbulence_model = 'similarity'        # Possibilites are CONSTANT/SIMILARITY
Horizontal_turbulence_model = 'rams'            # Possbilities are CONSTANT/RAMS
Vertical_diffusion_coefficient = 100            # m2/s
Horizontal_diffusion_coefficient = 1000         # m2/s
Post_process_time_interval = 1                  # Hours

# Granulometry (Volcanological input file)
Number_of_grainsize_classes = 6
Mean_grainsize = 2.5                            # phi
Minimum_grainsize = 0                           # phi
Maximum_grainsize = 5                           # phi
Sorting = 1.5
Density_minimum = 1200                          # kg/m3
Density_maximum = 2300                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Meteorological database (Volcanological input file)
Year = 1982                                     # Of meteo data
Month = 5                                       # Of meteo data
Day = 17                                        # Of meteo data
Start_time_of_meteo_data = 0                    # Hours after 00
End_time_of_meteo_data = 5                      # Hours after 00
Hours_between_meteo_data_blocks = 1             # Hours
Z_layers = [100, 250, 500, 1000, 2500, 5000, 10000] # List Z layers in increasing height order (meters; i.e.[100, 500, 1000, 5000, etc])

# Source (Volcanological input file)
Vent_location_X_coordinate = 813709             # UTM refer to GoogleEarth (convert to UTM)
Vent_location_Y_coordinate = 9209475            # UTM refer to GoogleEarth (convert to UTM)
Mass_eruption_rate = 1e4                        # kg/s
Source_type = 'plume'                           # Options are 'plume', 'suzuki', 'point'
Height_above_vent = 0                           # m (suzuki and point only)            
A = 0                                           # (suzuki only)            
L = 0                                           # (suzuki only)            
Exit_velocity = 100                             # m/s (plume only)
Exit_temperature = 1073                         # K (plume only)
Exit_volatile_fraction = 0                      # % (plume only)

# Post-Processing (Volcanological input file)
Output_results_in_GRD_format = 'Yes'            # Yes/No                                                        
Output_results_in_PS_format = 'Yes'             # Yes/No                                                        

Map_total_load = 'Yes'                          # Yes/No (mass per unit area)                                                      
Load_contours = [0.1, 0.25, 0.5, 1, 5, 10, 50]  # List contour intervals (PS format only)

Map_class_load = 'No'                           # Yes/No (mass per unit area for each grainsize)                                
Class_load_contours = [0.1, 0.25, 0.5, 1, 5, 10, 50] # List contour intervals (PS format only)

Map_deposit_thickness = 'Yes'                   # Yes/No                                        
Map_thickness_units = 'cm'                      # Possibilities (mm, cm, m)
Map_thickness_compaction_factor = 0.7           # Degree of compaction (i.e. 0.7)
Thickness_contours = [0.1, 1, 5, 10, 50, 100, 500] # List contour intervals (PS format only)

Map_total_concentration = 'No'                  # Yes/No                                
Map_total_concentration_z_cuts = [1000, 2000]   # List height in meters of each z-cut required (i.e. 1000 2000)
Total_concentration_contours = [1e-5, 1e-4]     # List contour intervals (PS format only)

Map_z_cummulative_concentration = 'No'          # Yes/No                        
Cummulative_concentration_contours = [0.01, 0.1, 1, 10] # List contour intervals (PS format only)
 
Map_Z_maximum_concentration = 'No'              # Yes/No                                                
Maximum_concentration_contours = [1e-4, 1e-3]   # List contour intervals (Ps format only)

Fixed_contour_interval = 1                                          # Contour interval for kml and shp files
Topography_grid = 'guntur_topography.txt'                           # Specify ASCII topography grid to use. 
                                                                    # If empty, AIM will look for a topography grid named
                                                                    # <scenario_name>_topography.txt         

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, dircomment=Eruption_comment)
    
 



