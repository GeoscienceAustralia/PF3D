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
Eruption_comment = 'guntur_1840_validation'

# Temporal parameters (hours)
#Start_time_of_eruption = 0                      # Hours after 00
#End_time_of_eruption = 5                      	# Hours after 00 
#End_time_of_run = 5                             # Hours after 00  
eruption_start = 0
eruption_duration = 5 
post_eruptive_settling_duration = 0

# Location (Volcanological input file)
X_coordinate_of_vent = 814924                   # UTM zone implied by topography projection 
Y_coordinate_of_vent = 9208168                  # UTM zone implied by topography projection

# Vertical discretisation for model domain
Z_min = 0.0
Z_max = 10000
Z_increment = 1000

# Meteorological input: Either pathway to profile (single file or directory with multiple files in case of hazard maps) or web site with forecast data)
wind_profile = 'guntur1840_wind.profile'

# Terrain model for model domain (pathway to topography data)
Topography_grid = 'guntur1840_topography.txt'   # Specify ASCII topography grid to use. 

                                                # FIXME: GET RID OF THIS OPTION - BUT MAKE SURE TOP FILE IS STILL CORRECTLY GENERATED
                                                # If empty, AIM will look for a topography grid named
                                                # <scenario_name>.top (surfer GRD format)         
                                                


# Granulometry (Volcanological input file)
Grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
Number_of_grainsize_classes = 8
Mean_grainsize = -1.5                           # phi
Sorting = 2
Minimum_grainsize = -4                          # phi
Maximum_grainsize = 3                        	# phi
Density_minimum = 1200                          # kg/m3
Density_maximum = 2500                          # kg/m3
Sphericity_minimum = 0.9
Sphericity_maximum = 0.9

# Source (Volcanological input file)
Vent_height = 2250
Source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
Mass_eruption_rate = 3e6                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
Height_above_vent = 8000                        # m (if point, if suzuki or if plume where Height_or_MFR = Height)            
A = 4                                           # (suzuki only)            
L = 1                                           # (suzuki only)
Height_or_MFR = 'MFR'                           # plume only
MFR_minimum = 1e6                               # kg/s (plume only)
MFR_maximum = 2e6                               # kg/s (plume only) 
Exit_velocity = 100                             # m/s (plume only)
Exit_temperature = 1073                         # K (plume only)
Exit_volatile_fraction = 0                      # % (plume only)

# Fall3D (Volcanological input file)
Terminal_velocity_model = 'ganser'              # Possibilites are ARASTOOPOR/GANSER/WILSON/DELLINO
Vertical_turbulence_model = 'constant'          # Possibilites are CONSTANT/SIMILARITY
Horizontal_turbulence_model = 'constant'        # Possbilities are CONSTANT/RAMS
Vertical_diffusion_coefficient = 100            # m2/s
Horizontal_diffusion_coefficient = 1000         # m2/s
Value_of_CS = 0.1                               # RAMS only

# Contouring: True, False, number or list of numbers    
Thickness_contours = [1, 2, 5, 10, 25, 50, 75, 100]  
Load_contours = True                            

Thickness_units = 'cm'                          # mm/cm/m


# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__, 
                 timestamp_output=False,    
                 store_locally=True,
                 dircomment=Eruption_comment)


 
#   False: Disabled
#   True: Provide a fixed number of contours covering entire range
#   Number: Fixed (vertical) interval between contours
#   List of numbers: Exact contour levels



