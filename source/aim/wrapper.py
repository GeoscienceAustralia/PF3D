"""Class AIM - implementing Ash Impact Modelling using Fall3d
"""

import os, string

from config import tephra_output_dir
from utilities import run, write_line, makedir, header, tail
from utilities import check_presence_of_required_parameters, grd2asc
from utilities import get_fall3d_home, get_tephradata, get_username, get_timestamp
from utilities import convert_meteorological_winddirection_to_windfield
from utilities import get_wind_direction, calculate_extrema, label_kml_contours

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
        if not timestamp_output:
            try:
                os.listdir(output_dir)
            except:
                # OK if it doesn't exist
                pass
            else:
                # Clean out any previous files
                s = 'chmod -R +w %s' % output_dir 
                run(s, verbose=False)                    
                s = '/bin/rm -rf %s' % output_dir
                run(s, verbose=False)        
        
                                  
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
        self.windprofile = self.basepath + '.profile'
        
        # Topographic surfer grid generated from scenario_topography.txt
        self.topography = self.basepath + '.top'
                                       
        # Output database file
        self.databasefile = self.basepath + '.dbs'
                                         
        # Output result file (Fall3d adds another .nc to this)
        self.resultfile = self.basepath + '.res'
        
        # Output Surfer grid file        
        self.grdfile = self.basepath + '.grd'
                                       
                                       
        #----------------------------
        # Precomputations, checks etc
        #----------------------------
        
        # Verify that the right parameters have been provided        
        #check_presence_of_required_parameters(params)        
        
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

        if verbose:
            print 'Logfile: %s' % logfile

        
        stdout = self.basepath + '.%s.stdout' % name
        stderr = self.basepath + '.%s.stderr' % name
        err=run(cmd, 
                stdout=stdout,
                stderr=stderr,
                verbose=False)

            
        if verbose:
            print 'Logfile ended as follows:'
            tail(logfile, lines)
            
        if err:
            msg = 'Script %s ended abnormally. Log files are:\n' % cmd
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
                                  'SetGrn', 'SetGrn.PUB.exe')
        
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
                                  'SetDbs', 'SetDbs.PUB.exe')
        
        logfile = self.basepath + '.SetDbs.log'
        
        if verbose:
            header('Building meteorological database (SetDbs)')

        cmd = '%s '*7 % (executable, logfile, 
                         self.inputfile, self.windprofile, 
                         self.databasefile, 
                         self.topography, 'profile')
                         
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
                                  'SetSrc', 'SetSrc.PUB.exe')
        
        logfile = self.basepath + '.SetSrc.log'

        if verbose:
            header('Creating eruptive source file (SetSrc)')
  

        cmd = '%s '*8 % (executable, logfile, 
                         self.inputfile,
                         self.sourcefile,                                
                         self.grainfile,
                         self.databasefile,
                         'FALL3D',    # Taken from hardwired values in Script-SetSrc
                         'YES')
                 
        
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
    
        executable = os.path.join(self.Fall3d_dir, 'Fall3d_ser.PUB.exe')
        
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
                       
                                                
    def nc2grd(self, verbose=True):
        """Run nc2grd - post processing tool
        
        Requires 
        - input file
        - source file
        - grain file
        - database file
        """
        
        executable = os.path.join(self.utilities_dir, 'nc2grd', 'nc2grd.exe')
        
        logfile = self.basepath + '.nc2grd.log'
        
        if verbose:
            header('Running nc2grd')

               
        cmd = '%s '*5 % (executable, 
                         logfile,
                         self.inputfile,
                         self.resultfile + '.nc',
                         self.grdfile)
                         
        self.runscript(cmd, 'nc2grd', logfile, lines=2,
                       verbose=verbose)
                       
                                                
        # Fix the filenames up (FIXME: Hopefully this is a temporary measure)
        #print 'Post processing generated the following files:'
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.grd'):
                fields = filename.split('.')
                
                # Ditch date and minutes
                hour, _ = fields[3].split(':')
                
                new_filename = fields[0] + '.' + hour + 'h.' + fields[-2] + '.' + fields[-1]
                
                
                s = 'cd %s; mv %s %s' % (self.output_dir, filename, new_filename)
                os.system(s)
                
                                                    
    def convert_surfergrids_to_asciigrids(self, verbose=True):
        """Convert GRD files to ASC files
        
        The purposes of the ASCII files are
        * They can be ingested by ESRI and other GIS tools.
        * They have an associated projection file that allows georeferencing.
        * They form the inputs for the contouring 
        """

        # FIXME (Ole): This function is probably obsolete in Fall3d, version 6
        #grd = self.params['Output_results_in_GRD_format'].lower()
        #if verbose and grd == 'yes':
        #    header('Converting GRD files to ASCII grids')
                               
        if verbose:
            header('Converting grd files to ASCII')
                            
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.grd'):
                if verbose: print '  ', filename
                grd2asc(os.path.join(self.output_dir, filename), 
                        projection=self.WKT_projection)
                        
                        

    def convert_ncgrids_to_asciigrids(self, verbose=True):
        """Convert (selected) NC data layers to ASC files
        
        One ASCII file is generated for each timestep (assumed to be in hours).
        
        The purposes of the ASCII files are
        * They can be ingested by ESRI and other GIS tools.
        * They have an associated projection file that allows georeferencing.
        * They form the inputs for the contouring 
        """
    
        if verbose:
            header('Converting NetCDF data to ASCII grids')
                               
                
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.res.nc'):
                if verbose: print '  ', filename
                for subdataset in ['LOAD', 'THICKNESS']:
                    nc2asc(os.path.join(self.output_dir, filename), 
                           subdataset=subdataset,
                           ascii_header_file=self.topography_grid,                           
                           projection=self.WKT_projection)
                           
                        
    def generate_contours(self, number_of_contours=5, verbose=True):
        """Contour ASCII grids
        """
       
        assert number_of_contours > 0
        
        if verbose:
            header('Contouring ASCII grids to KML files')        
        
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.asc'):
            
                fields = filename.split('.')
                
                # FIXME: Unit specified in post processing block (hardwired)
                if fields[-2] == 'depload': 
                    units = 'kg/m^2'
                elif fields[-2] == 'depthick': 
                    units = 'cm'
                else:                 
                    units = 'no unit'
                
                pathname = os.path.join(self.output_dir, filename)
                basename, ext = os.path.splitext(pathname)
                
                tiffile = basename + '.tif'
                shpfile = basename + '.shp'
                kmlfile = basename + '.kml'
                prjfile = basename + '.prj'
                

                # Calculate minimum and maximum values of ascii file
                min, max = calculate_extrema(pathname)
                interval = (max-min)/number_of_contours
                if verbose: 
                    print '  %s:' % os.path.split(kmlfile)[-1]
                    print '     Range (%s): [%f, %f]' % (units, min, max) 
                    print '     Contour interval: %f %s' % (interval, units)
                    
                if interval < 1.0e-6: 
                    print 'WARNING (generate_contours): Range in file %s is really too small to contour: %f' % (pathname, interval)
                
                # Generate GeoTIFF raster
                s = 'gdal_translate -of GTiff %s %s' % (pathname, tiffile)
                self.run_with_errorcheck(s, tiffile, 
                                         verbose=False)                                


                # Generate contours as shapefiles
                s = '/bin/rm -rf %s' % shpfile # Clear the way
                run(s, verbose=False)
                
                s = 'gdal_contour -i %f %s %s' % (interval, tiffile, shpfile)
                self.run_with_errorcheck(s, shpfile, 
                                         verbose=False)                
                
                # Generate KML
                if self.WKT_projection:
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 -s_srs %s %s %s' % (prjfile, kmlfile, shpfile)
                else: 
                    print 'WARNING (generate_contours): Model did not have a projection file'
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 %s %s' % (kmlfile, shpfile)                
                
                self.run_with_errorcheck(s, kmlfile, 
                                         verbose=False)
                    
                # Label KML file with contour intervals
                label_kml_contours(kmlfile, interval)
                                                

    def Xgenerate_contours(self, interval=1, verbose=True):
        """Contour NetCDF grids directly
        """
        # FIXME (Ole): This does not work - probably due to the GDAL NetCDF driver ignoring coordinate system
	       
        if verbose:
            header('Contouring NetCDF thickness grids')       
	       
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.res.nc'):
                
                pathname = os.path.join(self.output_dir, filename)
                if verbose: print '  ', pathname       
	               
                basename, ext = os.path.splitext(pathname)
	               
                tiffile = basename + '.tif'
                shpfile = basename + '.shp'
                kmlfile = basename + '.kml'
                prjfile = basename + '.prj'
	               
	
	               
                # Generate GeoTIFF raster
                netcdf_subdata = 'NETCDF:"%s":THICKNESS' % pathname
                s = 'gdal_translate -of GTiff -b 1 %s %s' % (netcdf_subdata, tiffile) # FIXME: Band is hardwired
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
                    # Create associated projection file
                    fid = open(prjfile, 'w')
                    fid.write(self.WKT_projection)
                    fid.close()        
                            
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 -s_srs %s %s %s' % (prjfile, kmlfile, shpfile)
                else:   
                    s = 'ogr2ogr -f KML -t_srs EPSG:4623 %s %s' % (kmlfile, shpfile)               
	               
                self.run_with_errorcheck(s, kmlfile, 
                                         verbose=verbose)                                
                                                
                
    def write_input_file(self, verbose=False):
        """Generate input file for Fall3d-6
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
	write_line(fid, 'BEGIN_METEO_DATA_(HOURS_AFTER_00) = %f' % Start_time_of_meteo_data, indent=2)
	write_line(fid, 'TIME_STEP_METEO_DATA_(MIN) = %f' % Meteo_time_step, indent=2)
	write_line(fid, 'END_METEO_DATA_(HOURS_AFTER_00) = %f' % End_time_of_meteo_data, indent=2)	
        write_line(fid, 'ERUPTION_START_(HOURS_AFTER_00) = %f' % Start_time_of_eruption, indent=2)
        write_line(fid, 'ERUPTION_END_(HOURS_AFTER_00) = %f' % End_time_of_eruption, indent=2) 
        write_line(fid, 'RUN_END_(HOURS_AFTER_00) = %f' % End_time_of_run, indent=2)
        write_line(fid, '')

	write_line(fid, 'GRID')
	write_line(fid, 'COORDINATES = %s' % Coordinates, indent=2)
	write_line(fid, 'LON-LAT')
	write_line(fid, 'LONMIN = %f' % Longitude_minimum, indent=5)
	write_line(fid, 'LONMAX = %f' % Longitude_maximum, indent=5)
	write_line(fid, 'LATMAX = %f' % Latitude_minimum, indent=5)
	write_line(fid, 'LATMAX = %f' % Latitude_maximum, indent=5)
	write_line(fid, 'LON_VENT = %f' % Longitude_of_vent, indent=5)
	write_line(fid, 'LAT_VENT = %f' % Latitude_of_vent, indent=5)
	write_line(fid, 'UTM')
	write_line(fid, 'UTMZONE = %s' % UTMZONE, indent=5)        
	write_line(fid, 'XMIN = %f' % X_coordinate_minimum, indent=5)
	write_line(fid, 'XMAX = %f' % X_coordinate_maximum, indent=5)
	write_line(fid, 'YMIN = %f' % Y_coordinate_minimum, indent=5)
	write_line(fid, 'YMAX = %f' % Y_coordinate_maximum, indent=5)
	write_line(fid, 'X_VENT = %f' % X_coordinate_of_vent, indent=5)
	write_line(fid, 'Y_VENT = %f' % Y_coordinate_of_vent, indent=5)
	write_line(fid, 'NX = %i' % Number_cells_X_direction, indent=2)
        write_line(fid, 'NY = %i' % Number_cells_Y_direction, indent=2)
 	write_line(fid, 'ZLAYER_(M) FROM %f TO %f INCREMENT %f' % (Z_layer_minimum, 
                                                                   Z_layers[-1],
                                                                   Z_layer_increment), indent=2)
	write_line(fid, '')
	
	write_line(fid, 'GRANULOMETRY')
	write_line(fid, 'DISTRIBUTION = %s' % Grainsize_distribution, indent=2)
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
	write_line(fid, 'SOURCE')
	write_line(fid, 'VENT_HEIGHT_(M) = %f' % Vent_height, indent=2)
        write_line(fid, 'SOURCE_TYPE = %s' % Source_type, indent=2) 
        write_line(fid, 'POINT_SOURCE', indent=2)
        write_line(fid, 'MASS_FLOW_RATE_(KGS) = %f' % Mass_eruption_rate, indent=5)

        Height_above_vent_string = ''
        for H in Height_above_vent:
            Height_above_vent_string += '%f ' % H
        
        write_line(fid, 'HEIGHT_ABOVE_VENT_(M) = %s' % Height_above_vent_string, indent=5)
        write_line(fid, 'SUZUKI_SOURCE', indent=2)
	write_line(fid, 'MASS_FLOW_RATE_(KGS) = %f' % Mass_eruption_rate, indent=5)
        write_line(fid, 'HEIGHT_ABOVE_VENT_(M) = %s' % Height_above_vent_string, indent=5) # FIXME: Why?
        write_line(fid, 'A = %i' % A, indent=5)
        write_line(fid, 'L = %i' % L, indent=5)
        write_line(fid, 'PLUME_SOURCE', indent=2)
	write_line(fid, 'SOLVE_PLUME_FOR = %s' % Height_or_MFR, indent =5)
	write_line(fid, 'MFR_SEARCH_RANGE = %f %f' % (MFR_minimum, 
						      MFR_maximum), indent=5)
	write_line(fid, 'HEIGHT_ABOVE_VENT = %s' % Height_above_vent_string, indent=5) # FIXME: Why?
	write_line(fid, 'MASS_FLOW_RATE_(KGS) = %f' % Mass_eruption_rate, indent=5)
        write_line(fid, 'EXIT_VELOCIY_(MS) = %f' % Exit_velocity, indent=5)
        write_line(fid, 'EXIT_TEMPERATURE_(K) = %f' % Exit_temperature, indent=5)
        write_line(fid, 'EXIT_VOLATILE_FRACTION_(IN%%) = %f' % Exit_volatile_fraction, indent=5)
        write_line(fid, '')

        write_line(fid, 'FALL3D')
        write_line(fid, 'TERMINAL_VELOCITY_MODEL = %s' % Terminal_velocity_model, indent=2)
        write_line(fid, 'VERTICAL_TURBULENCE_MODEL = %s' % Vertical_turbulence_model, indent=2) 
        write_line(fid, 'VERTICAL_DIFFUSION_COEFFICIENT = %f' % Vertical_diffusion_coefficient, indent=2) 
        write_line(fid, 'VERTICAL_DIFFUSION_COEFFICIENT_(M2/S) = %f' % Vertical_diffusion_coefficient, indent=2) 
        write_line(fid, 'HORIZONTAL_TURBULENCE_MODEL = %s' % Horizontal_turbulence_model, indent=2) 
        write_line(fid, 'HORIZONTAL_DIFFUSION_COEFFICIENT = %f' % Horizontal_diffusion_coefficient, indent=2) 
	write_line(fid, 'HORIZONTAL_DIFFUSION_COEFFICIENT_(M2/S) = %f' % Horizontal_diffusion_coefficient, indent=2)
	write_line(fid, 'RAMS_CS = %f' % Value_of_CS, indent=2)
        write_line(fid, '') 

        Z_layer_string = ''
        for Z in Z_layers:
            Z_layer_string += '%f ' % Z
        write_line(fid, 'Z_LAYER_(M) = %s' % Z_layer_string, indent=2)

        write_line(fid,'')

        write_line(fid, 'OUTPUT')
        write_line(fid, 'POSTPROCESS_TIME_INTERVAL_(HOURS) = %F' % Postprocess_time_interval, indent=2)
        write_line(fid, 'POSTPROCESS_3D_VARIABLES = %s' % Postprocess_3D_variables, indent=2)
        write_line(fid, 'POSTPROCESS_CLASSES = %s' % Postprocess_classes, indent=2)
	write_line(fid, 'TRACK_POINTS = %s' % Track_points, indent=2)
        
        # Write POST processing data (hardwired for now - note in particular that units are CM (see contouring))
        write_line(fid, '')        
        write_line(fid, 'POSTPROCESS')
        write_line(fid, 'MAP_TOPOGRAPHY = no                 (Possibilities: YES/NO)', indent=2)
        write_line(fid, 'UNITS = M                           (Possibilities: M)', indent=5)
        write_line(fid, 'MAP_TOTAL_LOAD = yes                (Possibilities: YES/NO)', indent=2)
        write_line(fid, 'UNITS = KG/M2                       (Possibilities: KG/M2)', indent=5)
        write_line(fid, 'MAP_CLASS_LOAD = no                 (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = KG/M2                       (Possibilities: KG/M2)',  indent=5)
        write_line(fid, 'MAP_DEPOSIT_THICKNESS = yes         (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = CM                          (Possibilities: MM/CM/M)',  indent=5)
        write_line(fid, 'COMPACTATION_FACTOR = 0.7',  indent=5)
        write_line(fid, 'MAP_COLUMN_MASS = no                (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M2                       (Possibilities: GR/M2)',  indent=5)
        write_line(fid, 'MAP_FLIGHT_LEVEL = no               (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M3                       (Possibilities: GR/M3)',  indent=5)
        write_line(fid, 'MAP_CONCE_GROUND = no               (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M3                       (Possibilities: GR/M3)',  indent=5)
        write_line(fid, 'MAP_PMxx_GROUND = no                (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M3                       (Possibilities: GR/M3)',  indent=5)
        write_line(fid, 'MAP_PMxx_CUMMUL = no                (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M2                       (Possibilities: GR/M2)',  indent=5)
        write_line(fid, 'MAP_TOTAL_CONCENTRATION = no        (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M3                       (Possibilities: GR/M3)',  indent=5)
        write_line(fid, 'Z_CUTS_(M)       = 2000. 4000. 6000.',  indent=5)
        write_line(fid, 'MAP_CLASS_CONCENTRATION = no        (Possibilities: YES/NO)',  indent=2)
        write_line(fid, 'UNITS = GR/M3                       (Possibilities: GR/M3)',  indent=5)
        
        
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
        
            # Assume existence of Fall3d native <scenario_name>.profile
            # and copy to work area
        
            native_profile = '%s.profile' % self.scenario_name
            print('AIM wind profile %s could not be found.' % self.wind_profile)
            print('Assuming existence of Fall3d profile named %s' % native_profile)
            
            s = 'cp %s %s' % (native_profile, self.output_dir)
            print(s)
            os.system(s)
            return
            
        lines = infile.readlines()
        infile.close()

        
        # Gather wind data for each time block
        timeblocks=[]
        if lines[0].startswith('Constant'):
            # Model will use these wind values throughout
            timeblock = []
            for line in lines[1:]:
                if line.strip()=='': continue # Skip blank lines
                timeblock.append(line.strip())                
            
            # Repeat timeblock for duration of eruption (rounded up)
            t_stop = self.params['End_time_of_run']
            t_start = self.params['Start_time_of_eruption']
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


        # Write Fall3D wind profile
        outfile=open(self.windprofile, 'w')

        vent_location_x = self.params['X_coordinate_of_vent']
        vent_location_y = self.params['Y_coordinate_of_vent']        
        outfile.write('%.0f. %.0f.\n' % (vent_location_x, vent_location_y))
                
        eruption_year = self.params['Eruption_Year']
        eruption_month = self.params['Eruption_Month']                
        eruption_day = self.params['Eruption_Day']
        outfile.write('%s%s%s\n' % (str(eruption_year), string.zfill(eruption_month, 2), string.zfill(eruption_day, 2)))        
        
        for hour, timeblock in enumerate(timeblocks):
            if len(timeblock) != nz:
                msg = 'Number of z layers in each time block much equal the number of specified Z layers.\n'
                msg += 'You specfied %i Z layers ' % nz
                msg += 'but timeblock in %s was %s, i.e. %i layers.' % (self.wind_profile, timeblock, len(timeblock))
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
            # Assume existence of Fall3d native <scenario_name>.top
            # and copy to work area
            
            native_grid = '%s.top' % self.scenario_name
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
        header3 = '%f %f' % (xllcorner, xllcorner+ncols*cellsize)
        header4 = '%f %f' % (yllcorner, yllcorner+nrows*cellsize)
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
        if os.path.isfile(actual_params_file):
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
        merapi.grd.18may2010.03:00.depload.grd
        
        are renamed to 
        
        merapi.03h.depload.asc        

       
        and will all go to a sub directory named 03h
        
        """
        
        # FIXME: This really needs to use a proper standard for time stamps
        
        dirname = None
        last_hour = -1
        last_dir = None
        for file in os.listdir(self.output_dir):
            if file.startswith(self.scenario_name):
                fields = file.split('.')
                if fields[1][-1] == 'h':
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
            
