"""Class AIM - implementing Ash Impact Modelling using Fall3d
"""

import os, string

from config import tephra_output_dir
from utilities import run, write_line, makedir, header, tail
from utilities import check_presence_of_required_parameters, grd2asc
from utilities import get_fall3d_home, get_tephradata, get_username, get_timestamp
from utilities import convert_meteorological_winddirection_to_windfield
from utilities import get_wind_direction

from parameter_checking import derive_implied_parameters
from parameter_checking import check_parameter_ranges
        
class AIM:

    def __init__(self, params, 
                 timestamp_output=True, 
                 store_locally=False,
                 dircomment=None,
                 verbose=True):
        """Create AIM instance and common file names
        
        
        Optional arguments:
        timestamp_output: If True, create unique output directory with timestamp
                          If False, overwrite output at every run
        store_locally: If True, store in same directory where scenario scripts 
                                are stored
                       If False, use environment variable TEPHRADATA for output.
        dircomment (string or None): Optional comment added to output dir
        verbose: (True, False) determine if diagnostic output is to be printed
        """
        
        params = params.copy() # Ensure modifications are kept local
        
        #---------------------------------
        # AIM names, files and directories 
        #---------------------------------        
                
        # AIM names and directories
        self.scenario_name = scenario_name = params['scenario_name']
        if store_locally:
            output_dir = os.path.join(os.getcwd(), tephra_output_dir)
        else:
            output_dir = get_tephradata()
        
        # Build output datastructure like    
        # $TEPHRADATA/<scenario>/<scenario>_user_timestamp
        output_dir = os.path.join(output_dir, 'scenarios')        
        output_dir = os.path.join(output_dir, scenario_name)
        
        scenario_dir = get_username()            
        if timestamp_output:
            scenario_dir += '_' + get_timestamp()        
            
        if dircomment is not None:
            try:
                dircomment = string.replace(dircomment, ' ', '_')
            except:
                msg = 'Dircomment %s could not be appended to output dir' % str(dircomment)
                raise Exception(msg)                
            
            scenario_dir += '_' + dircomment
        
        output_dir = os.path.join(output_dir, scenario_dir)
                                  
        # Base filename for all files in this scenario 
        self.basepath = os.path.join(output_dir, scenario_name)
        
        # AIM input files
        self.wind_profile = scenario_name + '_wind.txt'
        
        if params['Topography_grid']:
            self.topography_grid = params['Topography_grid']
        else:
            # If Topography grid is not specified, look for one named as scenario
            self.topography_grid = scenario_name + '_topography.txt'
                        
        # Derive projection file name               
        basename, ext = os.path.splitext(self.topography_grid) 
        self.projection_file = basename + '.prj'

        # Determine if topography is an AIM input file
        msg = 'AIM topography grid %s must have extension .txt' % self.topography_grid
        assert ext == '.txt', msg
        
        try:
            fid = open(self.topography_grid)
        except:
            self.native_AIM_topo = False
        else:    
            fid.close()
            self.native_AIM_topo = True


            
        
        
        #--------------------------------------
        # Fall3d specific files and directories 
        #--------------------------------------        
        
        # Fall3d directories
        self.Fall3d_dir = Fall3d_dir = get_fall3d_home()
        self.utilities_dir = os.path.join(Fall3d_dir, 'Utilities')        
        
        # Fall3d input files
        self.inputfile = self.basepath + '.inp'
        self.grainfile = self.basepath + '.grn'
        self.sourcefile = self.basepath + '.src'
        
        # Vertical wind profile data generated from scenario_wind.txt
        self.windprofile = self.basepath + '.profile.dat'
        
        # Regional topographic grid generated from scenario_topography.txt
        self.topography = self.basepath + '.regionaltopo.grd'
                                       
        # Output database file
        self.databasefile = self.basepath + '.dbs'
                                         
        # Output result file
        self.resultfile = self.basepath + '.res'
                                       
                                       
        #----------------------------
        # Precomputations, checks etc
        #----------------------------
        
        # Verify that the right parameters have been provided        
        check_presence_of_required_parameters(params)        
        
        # Derive implied spatial and modelling parameters
        derive_implied_parameters(self.topography_grid, params)
        
        # Check that parameters are physically compatible  
        check_parameter_ranges(params)
        self.params = params

        # Create output dir
        if verbose:
            header('Running AIM/Fall3d scenario %s' % self.scenario_name)
            print 'Writing to %s' % output_dir
            
        makedir(output_dir)
        self.output_dir = output_dir
                                       
    #---------------------------
    # Fall3d script replacements
    #---------------------------        
    def runscript(self, cmd, name, logfile, lines=5, verbose=False):
        """Run Fall3d script and report
        """

        stdout = self.basepath + '.%s.stdout' % name
        stderr = self.basepath + '.%s.stderr' % name
        err=run(cmd, 
                stdout=stdout,
                stderr=stderr,
                verbose=False)

            
        if verbose:
            print 'Logfile %s ends as follows:' % logfile
            tail(logfile, lines)
            
        if err:
            msg = 'SetSrc ended abnormally. Log files are:\n'
            msg += '  %s\n' % logfile
            msg += '  %s\n' % stdout            
            msg += '  %s\n' % stderr                        
            raise Exception(msg)


    def run_with_errorcheck(self, cmd, name, verbose=False):
        """Run general command with logging and errorchecking
        """
        
        stdout = '%s.stdout' % name    
        stderr = '%s.stderr' % name    
        err = run(cmd,
                  stdout=stdout,
                  stderr=stderr,
                  verbose=verbose)        
        if err:
            msg = 'Command "%s" ended abnormally. Log files are:\n' % cmd
            msg += '  %s\n' % stdout            
            msg += '  %s\n' % stderr                        
            raise Exception(msg)
            
                            
    def set_granum(self, verbose=True):
        """Create grainsize profile

        Requires 
        - input file
        """
            
        executable = os.path.join(self.utilities_dir, 
                                  'SetGrn', 'SetGrn.exe')
        
        logfile = self.basepath + '.SetGrn.log'

        if verbose:
            header('Setting grain size (SetGrn)')

        cmd = '%s %s %s %s' % (executable, logfile, 
                               self.inputfile, self.grainfile)
                               
        self.runscript(cmd, 'SetGrn', logfile, lines=4, 
                       verbose=verbose)                               
        
        
    def set_database(self, verbose=True):
        """Create meteorological database
        
        Requires 
        - input file
        - topography
        - windprofile
        """
        
        
        executable = os.path.join(self.utilities_dir, 
                                  'SetDbs', 'SetDbs.exe')
        
        logfile = self.basepath + '.SetDbs.log'
        
        if verbose:
            header('Building meteorological database (SetDbs)')

        cmd = '%s '*7 % (executable, logfile, 
                         self.inputfile, self.windprofile, 
                         self.databasefile, 'profile', 
                         self.topography)
                         
        self.runscript(cmd, 'SetDbs', logfile, lines=5,
                       verbose=verbose)
                       
                            
    def set_source(self, verbose=True):
        """Create eruptive source file
        
        Requires 
        - input file
        - grain file
        - database file
        """
    
        executable = os.path.join(self.utilities_dir, 
                                  'SetSrc', 'SetSrc.exe')
        
        logfile = self.basepath + '.SetSrc.log'

        if verbose:
            header('Creating eruptive source file (SetSrc)')
  

        cmd = '%s '*6 % (executable, logfile, 
                         self.inputfile,
                         self.sourcefile,                                
                         self.grainfile,
                         self.databasefile)
                 
        
        self.runscript(cmd, 'SetSrc', logfile, lines=5, 
                       verbose=verbose)
        

    def run_fall3d(self, verbose=True):
        """Run Fall3d (serial)
        
        Requires 
        - input file
        - source file
        - grain file
        - database file
        """
    
        executable = os.path.join(self.Fall3d_dir, 'Fall3d.ser.exe')
        
        logfile = self.basepath + '.Fall3d.log'
        
        if verbose:
            header('Running ash model (Fall3d)')

               
        cmd = '%s '*7 % (executable, 
                         self.inputfile,
                         self.sourcefile,                                
                         self.grainfile,
                         self.databasefile,
                         logfile,
                         self.resultfile)
                         
        self.runscript(cmd, 'Fall3d', logfile, lines=2,
                       verbose=verbose)                         

    
    def process_model_results(self, verbose=True):
        """Postprocess Fall3d output
        """
    
                
        executable = os.path.join(self.utilities_dir, 
                                  'Fall3dPostp', 
                                  'Fall3dPostp.exe')
        
        logfile = self.basepath + '.Fall3dPostp.log'
        
        if verbose:
            header('Processing model outputs (Fall3dPostp)')
        
                               
        # Optional terrain symbols file
        symfile = self.basepath + '.sym'


        cmd = '%s '*6 % (executable, logfile,
                         self.inputfile,
                         self.resultfile,
                         self.basepath,
                         symfile)
                         
        self.runscript(cmd, 'Fall3dPostp', logfile, lines=4,
                       verbose=verbose)                          
            
            
    def convert_surfergrids_to_asciigrids(self, verbose=True):
        """Convert GRD files to ASC files
        
        The purposes of the ASCII files are
        * They can be ingested by ESRI and other GIS tools.
        * They have an associated projection file that allows georeferencing.
        * They form the inputs for the contouring 
        """

        grd = self.params['Output_results_in_GRD_format'].lower()
        if verbose and grd == 'yes':
            header('Converting GRD files to ASCII grids')
                               
                
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.grd'):
                if verbose: print '  ', filename
                grd2asc(os.path.join(self.output_dir, filename), 
                        projection=self.WKT_projection)
                        
                        
                        
    def generate_contours(self, interval=1, verbose=True):
        """Contour ASCII grid
        """
        
        grd = self.params['Output_results_in_GRD_format'].lower()        
        if verbose and grd == 'yes':
            header('Contouring ASCII grids')        
        
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.asc'):
            
                pathname = os.path.join(self.output_dir, filename)
                if verbose: print '  ', pathname        
                
                basename, ext = os.path.splitext(pathname)
                
                tiffile = basename + '.tif'
                shpfile = basename + '.shp'
                kmlfile = basename + '.kml'
                prjfile = basename + '.prj'
                

                
                # Generate GeoTIFF raster
                s = 'gdal_translate -of GTiff %s %s' % (pathname, tiffile)
                self.run_with_errorcheck(s, tiffile, 
                                         verbose=verbose)                                


                # Generate contours as shapefiles
                s = '/bin/rm -rf %s' % shpfile # Clear the way
                run(s, verbose=False)
                
                s = 'gdal_contour -i %f %s %s' % (interval, tiffile, shpfile)
                self.run_with_errorcheck(s, shpfile, 
                                         verbose=verbose)                
                
                # Generate KML
                if self.WKT_projection:
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 -s_srs %s %s %s' % (prjfile, kmlfile, shpfile)
                else:    
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 %s %s' % (kmlfile, shpfile)                
                
                self.run_with_errorcheck(s, kmlfile, 
                                         verbose=verbose)
                    
                          

                
    def write_input_file(self, verbose=False):
        """Generate input file for Fall3d-5.1.1
        """

        params = self.params
        # Create local variables from dictionary
        for key in params:
            s = '%s = params["%s"]' % (key, key)
            exec(s)
        

        fid = open('%s' % self.inputfile, 'w')
        
        header = 'Fall3d input file for %s eruption' % self.scenario_name
        dashes = '-'*len(header)

        write_line(fid, dashes) 
        write_line(fid, '') 
        write_line(fid, header) 
        write_line(fid, '') 
        write_line(fid, dashes) 
        write_line(fid, '') 

        write_line(fid, 'TIME_UTC')  
        write_line(fid, 'YEAR = %i' % Eruption_Year, indent=2) 
        write_line(fid, 'MONTH = %02i' % Eruption_Month, indent=2)  
        write_line(fid, 'DAY = %i' % Eruption_Day, indent=2) 
        write_line(fid, 'RUN_START_(HOURS_AFTER_00) = %f' % Start_time_of_run, indent=2) 
        write_line(fid, 'ERUPTION_END_(HOURS_AFTER_00) = %f' % End_time_of_eruption, indent=2) 
        write_line(fid, 'RUN_END_(HOURS_AFTER_00) = %f' % End_time_of_run, indent=2)
        write_line(fid, '')
        write_line(fid, 'FALL3D')
        write_line(fid, 'ZLAYER_(M) FROM %f TO %f INCREMENT %f' % (Z_layer_minimum, 
                                                                   Z_layers[-1],
                                                                   Z_layer_increment), indent=2)
        write_line(fid, 'TERMINAL_VELOCITY_MODEL = %s' % Terminal_velocity_model, indent=2)
        write_line(fid, 'VERTICAL_TURBULENCE_MODEL = %s' % Vertical_turbulence_model, indent=2) 
        write_line(fid, 'VERTICAL_DIFFUSION_COEFFICIENT = %f' % Vertical_diffusion_coefficient, indent=2) 
        write_line(fid, 'VERTICAL_DIFFUSION_COEFFICIENT_(M2/S) = %f' % Vertical_diffusion_coefficient, indent=2) 
        write_line(fid, 'HORIZONTAL_TURBULENCE_MODEL = %s' % Horizontal_turbulence_model, indent=2) 
        write_line(fid, 'HORIZONTAL_DIFFUSION_COEFFICIENT = %f' % Horizontal_diffusion_coefficient, indent=2) 
	write_line(fid, 'HORIZONTAL_DIFFUSION_COEFFICIENT_(M2/S) = %f' % Horizontal_diffusion_coefficient, indent=2)
        write_line(fid, 'POSTPROCESS_TIME_INTERVAL_(HOURS) = %f' % Post_process_time_interval, indent=2)
        write_line(fid, '') 
        write_line(fid, dashes)  
        write_line(fid, dashes)
        write_line(fid, '')

        write_line(fid, 'GRANULOMETRY')
        write_line(fid, 'NUMBER_OF_CLASSES = %i' % Number_of_grainsize_classes, indent=2)
        write_line(fid, 'FI_MEAN = %f' % Mean_grainsize, indent=2)
        write_line(fid, 'FI_DISP = %f' % Sorting, indent=2)
        write_line(fid, 'FI_RANGE = %f %f' % (Minimum_grainsize,
                                              Maximum_grainsize), indent=2)
        write_line(fid, 'DENSITY_RANGE = %f %f' % (Density_minimum,
                                                   Density_maximum), indent=2)
        write_line(fid, 'SPHERICITY_RANGE = %f %f' % (Sphericity_minimum,
                                                          Sphericity_maximum), indent=2)
        write_line(fid, '')
        write_line(fid, dashes)
        write_line(fid, dashes)
        write_line(fid, '')
        write_line(fid, 'METEO_DATABASE')
        write_line(fid, 'YEAR = %i' % Year, indent=2)
        write_line(fid, 'MONTH = %i' % Month, indent=2)
        write_line(fid, 'DAY = %i' % Day, indent=2)
        write_line(fid, 'BEGIN_METEO_DATA_(HOURS_AFTER_00) = %f' % Start_time_of_meteo_data, indent=2)
        write_line(fid, 'END_METEO_DATA_(HOURS_AFTER_00) = %f' % End_time_of_meteo_data, indent=2)
        write_line(fid, 'TIME_STEP_METEO_DATA_(MIN) = %f' % meteo_time_step, indent=2)
        write_line(fid, 'X_ORIGIN_(UTM_M) = %f' % X_coordinate_lower_left_corner, indent=2)
        write_line(fid, 'Y_ORIGIN_(UTM_M) = %f' % Y_coordinate_lower_left_corner, indent=2)
        write_line(fid, 'CELL_SIZE_(KM) = %f' % Cell_size, indent=2)
        write_line(fid, 'NX = %i' % Number_cells_X_direction, indent=2)
        write_line(fid, 'NY = %i' % Number_cells_Y_direction, indent=2)

        Z_layer_string = ''
        for Z in Z_layers:
            Z_layer_string += '%f ' % Z
        write_line(fid, 'Z_LAYER_(M) = %s' % Z_layer_string, indent=2)

        write_line(fid,'')
        write_line(fid, dashes)
        write_line(fid, dashes)
        write_line(fid, '')
        write_line(fid, 'SOURCE')
        write_line(fid, 'X_VENT_(UTM_M) = %f' % Vent_location_X_coordinate, indent=2)
        write_line(fid, 'Y_VENT_(UTM_M) = %f' % Vent_location_Y_coordinate, indent=2)
        write_line(fid, 'MASS_FLOW_RATE_(KGS) = %f' % Mass_eruption_rate, indent=2)
        write_line(fid, 'SOURCE_TYPE = %s' % Source_type, indent=2)
        write_line(fid, 'POINT_SOURCE', indent=2)
        write_line(fid, 'HEIGHT_ABOVE_VENT_(M) = %f' % Height_above_vent, indent=5)
        write_line(fid, 'SUZUKI_SOURCE', indent=2)
        write_line(fid, 'HEIGHT_ABOVE_VENT_(M) = %f' % Height_above_vent, indent=5)
        write_line(fid, 'A = %i' % A, indent=5)
        write_line(fid, 'L = %i' % L, indent=5)
        write_line(fid, 'PLUME_SOURCE', indent=2)
        write_line(fid, 'EXIT_VELOCIY_(MS) = %f' % Exit_velocity, indent=5)
        write_line(fid, 'EXIT_TEMPERATURE_(K) = %f' % Exit_temperature, indent=5)
        write_line(fid, 'EXIT_VOLATILE_FRACTION_(IN%%) = %f' % Exit_volatile_fraction, indent=5)
        write_line(fid, '')
        write_line(fid, dashes)
        write_line(fid, dashes)
        write_line(fid, 'POSTPROCESS_MODELS')
        write_line(fid, 'OUTPUT_FILES_IN_GRD_FORMAT = %s' % Output_results_in_GRD_format, indent=2)
        write_line(fid, 'OUTPUT_FILES_IN_PS_FORMAT = %s' % Output_results_in_PS_format, indent=2)
        write_line(fid, '')

        write_line(fid, 'MAP_TOTAL_LOAD = %s' % Map_total_load, indent=2)
        write_line(fid, 'UNITS = %s' % load_units, indent=5)
        Load_contours_string = ''
        for contours in Load_contours:
            Load_contours_string += '%f ' % contours
        write_line(fid, 'CONTOUR_LEVELS = %s' % Load_contours_string, indent=5)
        write_line(fid, '')

        write_line(fid, 'MAP_CLASS_LOAD = %s' % Map_class_load, indent=2)
        Class_load_contours_string = ''
        for contours in Class_load_contours:
            Class_load_contours_string += '%f ' % contours
        write_line(fid, 'UNITS = %s' % class_load_units, indent=5)
        write_line(fid, 'CONTOUR_LEVELS = %s' % Class_load_contours_string, indent=5)

        write_line(fid, '')

        write_line(fid, 'MAP_DEPOSIT_THICKNESS = %s' % Map_deposit_thickness, indent=2)
        write_line(fid, 'UNITS = %s' % Map_thickness_units, indent=5)
        write_line(fid, 'COMPACTATION_FACTOR = %f' % Map_thickness_compaction_factor, indent=5)
        Thickness_contours_string = ''
        for contours in Thickness_contours:
            Thickness_contours_string += '%f ' % contours
        write_line(fid, 'CONTOUR_LEVELS = %s' % Thickness_contours_string, indent=5)
        write_line(fid, '')

        write_line(fid, 'MAP_TOTAL_CONCENTRATION = %s' % Map_total_concentration, indent=2)
        Map_total_concentration_z_cuts_string = ''
        for z_cuts in Map_total_concentration_z_cuts:
            Map_total_concentration_z_cuts_string += '%f ' % z_cuts
        write_line(fid, 'UNITS = %s' % total_concentration_units, indent=5)
        write_line(fid, 'Z_CUTS_(M) = %s' % Map_total_concentration_z_cuts_string, indent=5)
        Total_concentration_contours_string = ''
        for contours in Total_concentration_contours:
            Total_concentration_contours_string += '%e ' % contours
        write_line(fid, 'CONTOUR_LEVELS = %s' % Total_concentration_contours_string, indent=5)
        write_line(fid, '')

        write_line(fid, 'MAP_Z_CUMMULATIVE_CONCENTRATION = %s' % Map_z_cummulative_concentration, indent=2)
        write_line(fid, 'UNITS = %s' % z_cummulative_concentration_units, indent=5)
        Cummulative_concentration_contours_string = ''
        for contours in Cummulative_concentration_contours:
            Cummulative_concentration_contours_string += '%f ' % contours
        write_line(fid, 'CONTOUR_LEVELS = %s' % Cummulative_concentration_contours_string, indent=5)
        write_line(fid, '')

        write_line(fid, 'MAP_Z_MAXIMUM_CONCENTRATION = %s' % Map_Z_maximum_concentration, indent=2)
        write_line(fid, 'UNITS = %s' % z_maximum_concentration_units, indent=5)
        Maximum_concentration_contours_string = ''
        for contours in Maximum_concentration_contours:
            Maximum_concentration_contours_string += '%e ' % contours
        write_line(fid, 'CONTOUR_LEVELS = %s' % Maximum_concentration_contours_string, indent=5)
        write_line(fid, '')
        fid.close()
    
    
        
    #------------------------
    # AIM conversion routines
    #------------------------    
        
    def generate_windprofile(self, verbose=False):
        """Read wind profile data in the format 
    
               Hour 1
               10 10 14
               10 10 4
               10 10 1
               10 10 -2
               10 10 -12
               10 10 -30
               
               Hour 2
               10 10 14
               10 10 4
               ...
               
       
           Each row under each Hour heading correspond to an element in zlayers.  
           
           
           Alternatively, this format can be specified as 
           
           Constant
           10 10 14
           10 10 4
           10 10 1
           10 10 -2
           10 10 -12
           10 10 -30
           
           in which case values will be reused for the simulation duration   
        """
        
        zlayers = self.params['Z_layers']
        nz=len(zlayers)

        try:
            infile = open(self.wind_profile)
        except IOError:
        
            # Assume existence of Fall3d native <scenario_name>.profile.dat
            # and copy to work area
        
            native_profile = '%s.profile.dat' % self.scenario_name
            print('AIM wind profile %s could not be found.' % self.wind_profile)
            print('Assuming existence of Fall3d profile named %s' % native_profile)
            
            s = 'cp %s %s' % (native_profile, self.output_dir)
            print(s)
            os.system(s)
            return
            
        lines = infile.readlines()
        infile.close()

        timeblocks=[]
        
        if lines[0].startswith('Constant'):
            # Model will use these wind values throughout
            timeblock = []
            for line in lines[1:]:
                if line.strip()=='': continue # Skip blank lines
                timeblock.append(line.strip())                
            
            # Repeat timeblock for duration of eruption (rounded up)
            t_stop = self.params['End_time_of_run']
            t_start = self.params['Start_time_of_run']
            for i in range(int(t_stop-t_start+1)):
                timeblocks.append(timeblock)
        else:    
            # Model will use same timeblock for each hour
            for line in lines:
                if line.strip()=='': continue # Skip blank lines
                if line.startswith('Hour'):
                    timeblock=[]
                    timeblocks.append(timeblock)
                else:
                    timeblock.append(line.strip())



        outfile=open(self.windprofile, 'w')
        for hour, timeblock in enumerate(timeblocks):
            if len(timeblock) != nz:
                msg = 'Number of z layers must be constant for all time blocks'
                raise Exception(msg)
            
            itime1=hour*3600
            itime2=itime1+3600
            outfile.write('%i %i\n' % (itime1, itime2))
            outfile.write('%i\n' % nz)
            for i, zlayer in enumerate(zlayers):
                fields = timeblock[i].strip().split()
                s = float(fields[0]) # Speed (m/s)
                
                d = get_wind_direction(fields[1], 
                                       filename=self.windprofile)
                
                ux, uy = convert_meteorological_winddirection_to_windfield(s, d)
                
                T = float(fields[2])
                outfile.write('%f %f %f %f\n' % (zlayer, ux, uy, T))

        outfile.close()

        

    def generate_topography(self, verbose=False):    
        """Convert file with latitude longitude elevation to DEM 
        suitable for SetDbs utility in Fall3d
        
        Also, read in associated projection file (.prj) if present 
        and record georeference.
        """

        self.WKT_projection = None # Default - no projection

        if not self.native_AIM_topo:
            # Assume existence of Fall3d native <scenario_name>.regionaltopo.grd
            # and copy to work area
            
            native_grid = '%s.regionaltopo.grd' % self.scenario_name
            s = 'cp %s %s' % (native_grid, self.output_dir)
            print(s)
            os.system(s)
            return
        
        infile = open(self.topography_grid)
        lines = infile.readlines()
        infile.close()
        ncols = int(lines[0].split()[1])
        nrows = int(lines[1].split()[1])
        xllcorner = float(lines[2].split()[1])
        yllcorner = float(lines[3].split()[1])
        cellsize = float(lines[4].split()[1])

        header1 = 'DSAA'
        header2 = '%i %i' % (ncols, nrows)
        header3 = '%.1f %.1f' % (xllcorner, xllcorner+ncols*cellsize)
        header4 = '%.1f %.1f' % (yllcorner, yllcorner+nrows*cellsize)
        header5 = '0.0 0.0' # Can be obtained from data if needed

        outfile = open(self.topography, 'w')
        outfile.write(header1+'\n')
        outfile.write(header2+'\n')
        outfile.write(header3+'\n')
        outfile.write(header4+'\n')
        outfile.write(header5+'\n')

        data = lines[6:]
        data.reverse()

        for i, line in enumerate(data):
            for j, element in enumerate(line.split()):
                z = float(element)
                if z == -9999:
                    z = 0
                s = ' %14E' % (z) 
                outfile.write(s)
            outfile.write('\n')

        outfile.close()
        
        # Take note of projection file if present
        try:
            infile = open(self.projection_file)        
        except:
            #msg = 'Projection file %s could not be opened. '\
            #    % self.projection_file
            #msg += 'The topography file must be '
            #msg += 'georeferenced with an '
            #msg += 'ESRI WKT projection file '
            #msg += 'named %s.' % self.projection_file
            #raise Exception(msg)
            
            msg = 'WARNING: Projection file %s could not be opened. '\
                % self.projection_file
            msg += 'This means that model results must be manually '
            msg += 'georeferenced or the model run again with an '
            msg += 'ESRI WKT projection file '
            msg += 'named %s.' % self.projection_file
            print msg
            return
            
        # Read in projection file
        self.WKT_projection = infile.read()

        # This section demonstrates how the OSGEO GDAL libraries 
        # might help get projection details.
        #
        #from osgeo import osr # GDAL libraries
        #srs = osr.SpatialReference()
        #srs.ImportFromWkt(WKT)
        #proj4 = srs.ExportToProj4()   
        #fields = proj4.split()
        #
        #zone = proj = datum = units = None
        #for field in fields:
        #    print field
        #    
        #    res = field.split('=')
        #    if len(res) == 2:
        #        x, y = res
        #        if x == '+zone': zone = y
        #        if x == '+proj': proj = y            
        #        if x == '+ellps': datum = y            
        #        if x == '+units': units = y
        #    else:    
        #        if res == '+south': 
        #            hemisphere = 'S'
        #        else: 
        #            hemisphere = 'N'
        #
        #print zone, hemisphere, proj, datum, units
            
    
    def store_inputdata(self, verbose=False):
        """Create exact copy of input data into output area
        
        The intention is to ensure that all output has an audit trail.
        """
        
        audit_dir = os.path.join(self.output_dir, 'input_data')
        makedir(audit_dir)
        
        # Store input files
        s = 'cp %s %s' % (self.wind_profile, audit_dir)
        run(s, verbose=verbose)
        
        #s = 'cp %s %s' % (self.topography_grid, audit_dir)
        #run(s, verbose=verbose)        
        
        scenario_file = self.params['scenario_name'] + '.py'
        s = 'cp %s %s' % (scenario_file, audit_dir)
        run(s, verbose=verbose)                
        
        # Store actual parameters (as Python file)        
        actual_params_file = os.path.join(audit_dir, 'actual_parameters.py')
        run('chmod +w %s' % actual_params_file, verbose=verbose) # In case it was there already
        fid = open(actual_params_file, 'w')
        fid.write('"""All actual parameters used in scenario %s\n\n'\
                      % self.basepath)
        fid.write('This file is automatically generated by AIM\n')
        fid.write('and in serves a log of all input parameters used in\n')
        fid.write('Fall3d/AIM whether supplied or derived.\n')
        fid.write('"""\n\n\n')
        
        for param in self.params:
            value = self.params[param]
            fid.write('%s = %s\n' % (param, value))
        
        fid.close()
        
        # Set all files to read only to avoid accidental changes
        s = 'chmod -R -w %s' % audit_dir
        run(s, verbose=verbose)
                
        
    def organise_output(self, verbose=False):
        """Organise output files in directories by time
        
        Output files named e.g.
        merapi.003h.depothick.asc
        merapi.003h.depothick.ps
        ...
        will all go to a sub directory named 003h
        
        """
        
        dirname = None
        last_hour = -1
        last_dir = None
        for file in os.listdir(self.output_dir):
            if file.startswith(self.scenario_name):
                fields = file.split('.')
                if len(fields) > 1:
                    if fields[1].endswith('h'):
                        dirname = os.path.join(self.output_dir, fields[1])
                        filename = os.path.join(self.output_dir, file)
                        makedir(dirname)
                        s = 'mv %s %s' % (filename, dirname)
                        run(s, verbose=verbose)
                     
                        # Record last hour
                        hour = int(fields[1][:-1])
                        if hour > last_hour:
                            last_hour = hour
                            last_dir = dirname
                        
        # Create shortcut to last dir                
        if last_dir:
            s = 'ln -s %s %s/final_output' % (last_dir, self.output_dir)
            run(s, verbose=verbose)
            
