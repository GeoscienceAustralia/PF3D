#!/usr/bin/env python

import os, string
import unittest

from aim.interface import run_scenario, contour_hazardmap
from aim.wrapper import AIM
from aim.utilities import *

import numpy as num

def lines_numerically_close(s1, s2, rtol=1.0e-5, atol=1.0e-8):
    """Compare two strings but allow floats to be within a tolerance
    """

    # Convert strings to lists
    fields1 = s1.split()
    fields2 = s2.split()

    # Compare element by element
    for i, field1 in enumerate(fields1):
        field2 = fields2[i]
        if field1 != field2:
            # Not identical - try to compare numerically

            try:
                x = float(field1)
            except:
                # Element could not be converted to a float
                # so a numerical comparison is not possible
                return False

            try:
                y = float(field2)
            except:
                # Element could not be converted to a float
                # so a numerical comparison is not possible
                return False


            # Compare floats
            if not num.allclose(x, y, rtol=rtol, atol=atol):
                # Floats are not close enough to match
                return False

    # Elements are either identical or close enough numerically
    return True

def compare_to_reference_file(filename, scenario_name, subdir=None):
    """compare_to_reference_file
    """

    x = filename.split('.')
    ext = string.join(x[1:], '.')

    # Verify input file against reference data
    if subdir is None:
        ref = open('reference_output/%s_output/%s.%s' % (scenario_name,
                                                         scenario_name,
                                                         ext))
    else:
        ref = open('reference_output/%s_output/%s/%s.%s' % (scenario_name,
                                                            subdir,
                                                            scenario_name,
                                                            ext))

    ref_name = ref.name
    ref_data = ref.readlines()
    ref.close()

    new = open(filename)
    new_data = new.readlines()
    new_name = new.name
    new.close()

    for i in range(len(ref_data)):
        msg = 'Input file %s does not match ' % new_name
        msg += 'reference %s in line %i.\n' % (ref_name, i)
        msg += 'Generated data: %s\n' % new_data[i].strip()
        msg += 'Reference data: %s\n' % ref_data[i].strip()

        if new_data[i] != ref_data[i]:
            # Lines are different
            # Try to see if they are close enough
            # in a numerical sense

            if not lines_numerically_close(new_data[i], ref_data[i]):
                raise Exception(msg)



class Test_AIM(unittest.TestCase):
    def setUp(self):
        self.scenarios = ['mayon',
                          'galunggung',
                          'pinatubo',
                          'merapi',
                          'tambora']

    def tearDown(self):
        pass


    def XXtest_Fall3d_files(self):
        """test_Fall3d_files - Characterisation test of generated files
        Exclude final output for space reasons
        """

        for scenario_name in self.scenarios:

            # Get parameters specified in scenario_file
            scenario_file = scenario_name + '.py'
            params = get_scenario_parameters(scenario_file)
            assert params['scenario_name'] == scenario_name

            # Instantiate model object
            aim = AIM(params,
                      timestamp_output=False,
                      verbose=False)

            #-----------------------------------------------------
            # Test Fall3d input files against reference data
            #-----------------------------------------------------

            aim.write_input_file()
            compare_to_reference_file(aim.inputfile, scenario_name)

            aim.generate_windprofile()
            compare_to_reference_file(aim.windprofile, scenario_name)

            aim.generate_topography()
            compare_to_reference_file(aim.topography, scenario_name)


            #-------------------------------------------------
            # Test Fall3d outputs against reference data
            #-------------------------------------------------

            aim.set_granum(verbose=False)
            compare_to_reference_file(aim.grainfile, scenario_name)

            aim.set_database(verbose=False) # has output still??
            compare_to_reference_file(aim.databasefile + '.lst',
                                      scenario_name)

            aim.set_source(verbose=False)
            #print scenario_name
            #print aim.sourcefile

            compare_to_reference_file(aim.sourcefile,
                                      scenario_name)

            #aim.run_fall3d()
            #aim.process_model_results()

    def test_full_simulation(self):
        """test_full_simulation - Characterisation test of end to end scenario.
        """

        merapi = dict(
            # Short eruption comment to appear in output directory.
            eruption_comment='Test of full simulation for southern hemisphere using Merapi as example',

            # Temporal parameters (hours)
            eruption_start=0,
            eruption_duration=3,
            post_eruptive_settling_duration=1,

            # Location
            x_coordinate_of_vent=439423,   # UTM zone implied by topography projection
            y_coordinate_of_vent=9167213,  # UTM zone implied by topography projection

            # Vertical discretisation for model domain
            z_min=0.0,
            z_max=15000,
            z_increment=5000,

            # Meteorological data
            wind_profile='IDY25100_2012120412_6h.profile',

            # Terrain model
            topography_grid='merapi_topography.txt',

            # Granulometry
            grainsize_distribution='GAUSSIAN',
            number_of_grainsize_classes=6,
            mean_grainsize=-2,
            sorting=1.5,
            minimum_grainsize=4,
            maximum_grainsize=-4,
            density_minimum=1200,
            density_maximum=2300,
            sphericity_minimum=0.9,
            sphericity_maximum=0.9,

            # Source
            vent_height=2968,
            source_type='suzuki',
            mass_eruption_rate='estimate',
            height_above_vent=10000,
            A=4,
            L=1,
            height_or_MFR='MFR',
            MFR_minimum=1e7,
            MFR_maximum=1e9,
            exit_velocity=100,
            exit_temperature=1073,
            exit_volatile_fraction=0,

            # Fall3D
            terminal_velocity_model='ganser',
            vertical_turbulence_model='similarity',
            horizontal_turbulence_model='rams',
            vertical_diffusion_coefficient=250,
            horizontal_diffusion_coefficient=100,
            value_of_CS=0.1,

            # Contouring: True, False, number or list of numbers
            thickness_contours=True,
            load_contours=True,
            thickness_units='cm')


        aim = run_scenario(merapi,
                           timestamp_output=False,
                           verbose=False)

        # FIXME: Check output
        # In this case we also generate grd files

        #for hour in ['001h', '002h', '003h']:
        #    for ext in ['grd', 'asc', 'kml']:
        #        grd_filename = '%s/%s.%s.depothick.%s' % (hour,
        #                                                  scenario_name,
        #                                                  hour,
        #                                                  ext)
        #        compare_to_reference_file(os.path.join(aim.output_dir,
        #                                               grd_filename),
        #                                  scenario_name,
        #                                  subdir=hour)


    def test_grd2asc(self):
        """test_grd2asc - Test conversion from grd to asc files

        This test relies on files
        test_data.grd
        test_data.asc
        test_data.prj # FIXME: Not tested yet
        """


        # Rename input file to a temporary filename
        grdfilename = 'tmpxkshkoek.grd'

        s = 'cp test_data.grd %s' % grdfilename
        run(s, verbose=False)

        # Run conversion from grd to asc
        grd2asc(grdfilename)

        # Check that result is good
        # FIXME: Refactor compare_to_reference_file to accommodate the more general case

        fid1 = open(grdfilename[:-4] + '.asc')
        data1 = fid1.readlines()
        fid1.close()

        fid2 = open('test_data.asc')
        data2 = fid2.readlines()
        fid2.close()

        for i in range(len(data1)):
            msg = 'ASC file does not match '
            msg += 'reference test_data.asc in line %i.\n' % i

            #print data1[i].strip()
            #print data2[i].strip()
            #print

            if data1[i] != data2[i]:
                # Lines are different
                # Try to see if they are close enough
                # in a numerical sense

                if not lines_numerically_close(data1[i], data2[i]):
                    raise Exception(msg)

        os.remove(grdfilename)

    def test_asc2grd(self):
        """test_asc2grd - Test conversion from asc to grd files

        This test relies on files
        test_data.grd
        test_data.asc
        test_data.prj # FIXME: Not tested yet
        """


        # Rename input file to a temporary filename
        ascfilename = 'yfeauhkrc.asc'

        s = 'cp test_data.asc %s' % ascfilename
        run(s, verbose=False)

        # Run conversion from asc to grd
        asc2grd(ascfilename)

        # Check that result is good
        # FIXME: Refactor compare_to_reference_file to accommodate the more general case

        #print 'Open', ascfilename[:-4] + '.grd'

        fid1 = open(ascfilename[:-4] + '.grd')
        data1 = fid1.readlines()
        fid1.close()

        fid2 = open('test_data.grd')
        data2 = fid2.readlines()
        fid2.close()

        for i in range(len(data1)):
            msg = 'GRD file does not match '
            msg += 'reference test_data.grd in line %i:\n' % i
            msg += '%s\n' % str(data1[i])
            msg += '%s\n' % str(data2[i])


            #print data1[i].strip()
            #print data2[i].strip()
            #print

            if data1[i] != data2[i]:
                # Lines are different
                # Try to see if they are close enough
                # in a numerical sense
                if not lines_numerically_close(data1[i], data2[i]):
                    raise Exception(msg)

        os.remove(ascfilename)

    def test_nc2asc(self):
        """test_nc2asc - Test conversion from NetCDF to asc files

        This test relies on files
        merapi.res.nc
        merapi.003h.depothick.asc

        """

        ref_data = 'test_data/merapi.03h.depthick.asc'

        # Run conversion from grd to asc
        nc2asc('test_data/merapi.res.nc', 'THICKNESS',
               verbose=False)

        # Check that result is good
        # FIXME: Refactor compare_to_reference_file to accommodate the more general case

        fid1 = open('test_data/merapi.03h.thickness.asc')
        data1 = fid1.readlines()
        fid1.close()

        fid2 = open(ref_data)
        data2 = fid2.readlines()
        fid2.close()


        for i in range(len(data1)):
            msg = 'ASC file does not match '
            msg += 'reference %s in line %i.\n' % (ref_data, i)
            msg += data1[i]
            msg += data2[i]

            if data1[i] != data2[i]:
                # Lines are different
                # Try to see if they are close enough
                # in a numerical sense

                if not lines_numerically_close(data1[i], data2[i], atol=1.e-6):
                    raise Exception(msg)


    def test_pipe(self):
        """test_pipe

        Test that simplified process piping works
        """

        #
        p = pipe('whoami', verbose=False)
        res = p.stdout.read().strip()
        ref = os.getlogin().strip()
        assert res == ref

        #
        p = pipe('klchaohckck')
        res = p.stdout.read().strip()
        assert len(res) == 0

        err = p.stderr.read().strip()
        assert err.endswith('not found')

        #
        p = pipe('wc -c', verbose=False)
        p.stdin.write('aoeu')
        p.stdin.close()
        assert p.stdout.read().strip() == '4'


    def test_ASCII_extrema(self):
        """test_ASCII_extrema

        Test that maxima and minima can be computed from ESRI ASCII files
        """

        min, max = calculate_extrema('test_data.asc', verbose=False)

        assert min <= max

        assert num.allclose([min, max], [3.163064e-27, 5648.979])


    # FIXME: Obsolete now
    def XXtest_label_kml_contours(self):
        """test labeling of kml contours.

        This is really not testing the validity of the KML, but generates one that
        must be checked with Google Earth.
        """

        s = 'cp test_contour.kml test_contour_with_labels.kml'
        os.system(s)

        # Edit label file
        label_kml_contours('test_contour_with_labels.kml', 78.4866, 5, 'cm')


    def test_hazardmap_contouring(self):
        """Test that hazard maps can be contoured
        """

        # Parameters for Guntur
        scenario = {'vent_easting': 814924,
                    'vent_northing': 9208168,
                    'vent_zone': 48,
                    'vent_hemisphere': 'S',
                    'load_values': [1, 10, 100],
                    'fl_values': [0.0002, 0.002],
                    'model_output_directory': 'test_data',
                    'PLOAD_contours': True,
                    'PLOAD_units': 'pct',
                    'ISOCHRON_contours': True,
                    'ISOCHRON_units': 'h'}

        contour_hazardmap(scenario, verbose=False)

        # Assert that kml files are there
        # FIXME: Should also check the contents
        found = False
        for filename in os.listdir('test_data'):
            if filename == 'HazardMaps.pload_1.kml':
                found = True
        assert found

        fid = open('test_data/HazardMaps.pload_1.kml')
        lines = fid.readlines()
        fid.close()

        assert len(lines) > 20

        assert lines[1].startswith('<kml')



################################################################################

if __name__ == '__main__':
    suite = unittest.makeSuite(Test_AIM, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
