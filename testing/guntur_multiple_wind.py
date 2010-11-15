"""Configuration file for eruption scenario

Tephra modelling validation worksheet                 

Scenario Name: Mount Guntur 2010 (predictive scenario)                                                                    
Run Date: 2010_01_14           
Run number:1                                                                                   

Eruption observation details: 

To run in parallel you can do something like this

mpirun -x FALL3DHOME -hostfile /etc/mpihosts -np 8 python guntur_multiple_wind.py
or
mpirun -x FALL3DHOME -hostfile /etc/mpihosts -host node17,node11 python guntur_multiple_wind.py

"""

# Short eruption comment to appear in output directory.
Eruption_comment = 'multiple wind test'

# Time (Volcanological input file)
Eruption_Year = 2009                            # YYYY  
Eruption_Month = 1                              # MM  
Eruption_Day = 31                               # DD 
Start_time_of_meteo_data = 6                    # Hours after 00
Meteo_time_step = 360                            # Mins       
End_time_of_meteo_data = 36                       # Hours after 00
Start_time_of_eruption = 12                      # Hours after 00
End_time_of_eruption = 30                        # Hours after 00 
End_time_of_run = 36                              # Hours after 00  

# Location (Volcanological input file)
X_coordinate_of_vent = 814924                   # UTM zone implied by topography projection 
Y_coordinate_of_vent = 9208168                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
Z_min = 0.0
Z_max = 10000
Z_increment = 1000

# Select meteorological parameters
wind_profile = 'guntur_wind_013000-020218.profile'
#wind_altitudes = [100, 250, 500, 1000, 2500, 5000, 10000] # List Z layers in increasing height order (meters; i.e.[100, 500, 1000, 5000, etc])

# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 6
Mean_grainsize = 2.5                            # phi
Sorting = 1.5
Minimum_grainsize = 0                           # phi
Maximum_grainsize = 5                           # phi
Density_minimum = 1000                          # kg/m3
Density_maximum = 2500                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 2249 
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 1e4                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = [9000, 7000, 5000, 2000, 1000, 500] # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
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

Topography_grid = 'guntur_topography.txt'       # Specify ASCII topography grid to use. 
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)         
# Contouring:
#   False: Disabled
#   True: Provide a fixed number of contours covering entire range
#   Number: Fixed (vertical) interval between contours
#   List of numbers: Exact contour levels
Thickness_contours = True                       # True, False, number or list of numbers
Thickness_units = 'cm'                          # mm/cm/m

Load_contours = 2000                            # True, False, number or list of numbers                       

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_multiple_windfields
    run_multiple_windfields(__file__, 
                            windfield_directory='guntur_multiple_wind_test',
                            hazard_output_folder='guntur_mutliple_wind_hazard_outputs',
                            dircomment=Eruption_comment)



    
 



