"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Galunggung 1982                                                                    
Run Date: 1982_05_17           
Run number:1                                                                                   

Eruption observation details: 

"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'version_6_test'

# Time (Volcanological input file)
Eruption_Year = 1982                            # YYYY  
Eruption_Month = 5                              # MM  
Eruption_Day = 17                               # DD 
Start_time_of_meteo_data = 0                    # Hours after 00
Meteo_time_step = 60                            # Mins       
End_time_of_meteo_data = 5                      # Hours after 00
Start_time_of_eruption = 0                      # Hours after 00
End_time_of_eruption = 5                        # Hours after 00 
End_time_of_run = 5                             # Hours after 00  

# Grid (Volcanological input file)
Coordinates = 'UTM'                             # LON-LAT/UTM
Longitude_minimum = 0                           # LON-LAT only 
Longitude_maximum = 0                           # LON-LAT only
Latitude_minimum = 0                            # LON-LAT only
Latitude_maximum = 0                            # LON-LAT only
Longitude_of_vent = 0                           # LON-LAT only
Latitude_of_vent = 0                            # LON-LAT only
UTMZONE = '49S'                                 # UTM only
X_coordinate_minimum = 73273                    # UTM only   
X_coordinate_maximum = 275915                   # UTM only
Y_coordinate_minimum = 9095473                  # UTM only
Y_coordinate_maximum = 9298115                  # UTM only  
X_coordinate_of_vent = 176267                   # UTM only
Y_coordinate_of_vent = 9197056                  # UTM only  
Number_of_cells_X_direction = 151
Number_of_cells_Y_direction = 151               
Z_layers = [100, 250, 500, 1000, 2500, 5000, 10000] # List Z layers in increasing height order (meters; i.e.[100, 500, 1000, 5000, etc])

# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 6
Mean_grainsize = 2.5                            # phi
Sorting = 1.5
Minimum_grainsize = 0                           # phi
Maximum_grainsize = 5                           # phi
Density_minimum = 1200                          # kg/m3
Density_maximum = 2300                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 2168
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 5e4                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = [9000, 7000, 5000, 2000, 1000, 500, 250] # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
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

# Output (Volcanological input file)
Postprocess_time_interval = 1                   # Hours
Postprocess_3D_variables = 'No'                 # Yes/No
Postprocess_classes = 'No'                      # Yes/No
Track_points = 'No'                             # Yes/No

Topography_grid = 'galunggung_topography.txt'   # Specify ASCII topography grid to use. 
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)         

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=True,    
                 dircomment=Eruption_comment)


 





