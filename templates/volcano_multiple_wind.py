"""                 

volcano (multiple wind) template                                                                    

This template is for running multiple wind scnearios typically in parallel. Copy this template script into the modelling area, rename and edit as needed. 
The user must point to the location of the directory of multiple wind fields (i.e. 'guntur_wind_013000-020218.profile'). The user must also designate a name and location for the model outputs. 

To run:

python volcano_multiple_wind.py

To run in parallel:

mpirun -x FALL3DHOME -x PYTHONPATH -hostfile /etc/mpihosts -np 8 python volcano_multiple_wind.py
or
mpirun -x FALL3DHOME -x PYTHONPATH -hostfile /etc/mpihosts -host node17,node11 python volcano_multiple_wind.py

"""

# Short eruption comment to appear in output directory.
eruption_comment = 'multiple wind template'

# Temporal parameters (hours)
eruption_start = 12
eruption_duration = 18 
post_eruptive_settling_duration = 6

# Location (Volcanological input file)
x_coordinate_of_vent = 814924                   # UTM zone implied by topography projection 
y_coordinate_of_vent = 9208168                  # UTM zone implied by topography projection 

# Vertical discretisation for model domain
z_min = 0.0
z_max = 10000
z_increment = 1000

# Meteorological input
wind_profile = ''				# FIXME: currently specified at bottom of script

# Terrain model 
topography_grid = 'volcano_topography.txt'      # Path to topography file   

# Granulometry (Volcanological input file)
grainsize_distribution = 'GAUSSIAN'             # Possibilites are GAUSSIAN/BIGAUSSIAN
number_of_grainsize_classes = 6
mean_grainsize = 2.5                            # phi
sorting = 1.5
minimum_grainsize = 0                           # phi
maximum_grainsize = 5                           # phi
density_minimum = 1000                          # kg/m3
density_maximum = 2500                          # kg/m3
sphericity_minimum = 0.9
sphericity_maximum = 0.9

# Source (Volcanological input file)
vent_height = 2249 
source_type = 'suzuki'                          # Possibilities are 'plume', 'suzuki', 'point'
mass_eruption_rate = 1e4                        # kg/s (if point, if suzuki or if plume where Height_or_MFR = MFR)
height_above_vent = 9000 			# m (if point, if suzuki or if plume where Height_or_MFR = Height)            
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
load_contours = 2000

thickness_units = 'cm'                          # mm/cm/m



# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_multiple_windfields
    run_multiple_windfields(__file__, 
                            windfield_directory='/model_area/tephra/3D_wind/NCEP1/guntur_multiple_wind/2000-2009',
                            hazard_output_folder='guntur_mutliple_wind_hazard_outputs')



    
 



