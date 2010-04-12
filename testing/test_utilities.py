import unittest

from aim.utilities import *
from numpy import allclose
from math import sqrt

class Test_utilities(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wind_field(self):
        """test_wind_field - Test conversions to windfield
        
        Test that wind speed and 'meteorological' direction are
        converted correctly to wind field
        """
    
        # Southerly wind (blowing straight north)
        u, v = convert_meteorological_winddirection_to_windfield(10, 180)
        assert allclose(u, 0)
        assert allclose(v, 10)                  
        
        # Northerly wind (blowing straight south)
        u, v = convert_meteorological_winddirection_to_windfield(10, 0)
        assert allclose(u, 0)
        assert allclose(v, -10)                          
    
        # Easterly wind (blowing straight west)
        u, v = convert_meteorological_winddirection_to_windfield(10, 90)
        assert allclose(u, -10)
        assert allclose(v, 0)                  
        
        # Westerly wind (blowing straight east)
        u, v = convert_meteorological_winddirection_to_windfield(10, 270)
        assert allclose(u, 10)
        assert allclose(v, 0)                          
        
        # North Easterly wind (blowing straight south west)
        u, v = convert_meteorological_winddirection_to_windfield(2, 45)
        assert allclose(u, -sqrt(2))
        assert allclose(v, -sqrt(2))                                  
    
        # Arbitrary example 
        u, v = convert_meteorological_winddirection_to_windfield(10, 10)
        assert allclose(u, -1.736482)
        assert allclose(v, -9.848078)              
        
        
        
    def test_wind_direction(self):
        """test_wind_direction - Test conversion to wind direction
        
        Test that wind vector field is converted correctly to speed and 'meteorological' direction
        """
        
        # Southerly wind (blowing straight north)
        s, d = convert_windfield_to_meteorological_winddirection(0, 10)
        assert allclose(s, 10)
        assert allclose(d, 180)                  
        
        # Easterly wind (blowing straight west)
        s, d = convert_windfield_to_meteorological_winddirection(-10, 0)
        assert allclose(s, 10)
        assert allclose(d, 90)                  
        
        # Westerly wind (blowing straight east)
        s, d = convert_windfield_to_meteorological_winddirection(10, 0)
        assert allclose(s, 10)
        assert allclose(d, 270)                          

        # Northerly wind (blowing straight south)
        s, d = convert_windfield_to_meteorological_winddirection(0, -10)
        assert allclose(s, 10)
        assert allclose(d, 0), 'Angle %f should have been 0' % d                          
    
        # North Easterly wind (blowing straight south west)
        s, d = convert_windfield_to_meteorological_winddirection(-sqrt(2), 
                                                                  -sqrt(2))
        assert allclose(s, 2)
        assert allclose(d, 45)                                  
        

    def test_wind_field_conversions(self):
        """test_wind_field_conversions - Test that the wind field conversions are each others' inverses
        """

        # Use speed and direction
        for s in [2, 3.7, 7.9]:
            for d in range(360):
                u, v = convert_meteorological_winddirection_to_windfield(s, d)
                speed, phi = convert_windfield_to_meteorological_winddirection(u, v)
                assert allclose(speed, s)
                assert allclose(phi, d), 'Direction %f should have been %f' % (phi, d)
        
        
        # Use vector fields
        for u in [-15, -3.4, -1, 0, 0.12, 3.7, 7.9]:
            for v in [-17, -4.3, -2.11, -1, 0, 0.14, 1, 3.3, 7.9, 8.13]:
                s, d = convert_windfield_to_meteorological_winddirection(u, v)            
                ux, uy = convert_meteorological_winddirection_to_windfield(s, d)

                assert allclose(u, ux)
                assert allclose(v, uy)
        
    def test_windinput(self):
        """test_windinput - Test that direction format can be either as 'NW' or degrees
        """
        
        degrees = 0
        for direction in ['N', 'NNE', 'NE', 'ENE',
                          'E', 'ESE', 'SE', 'SSE',
                          'S', 'SSW', 'SW', 'WSW',
                          'W', 'WNW', 'NW', 'NNW']:
            
        
            msg = 'Direction %s failed' % direction
            assert get_wind_direction(direction) == degrees, msg
            assert get_wind_direction('%s' % str(degrees)) == degrees
            degrees += 22.5
        


################################################################################

if __name__ == '__main__':
    suite = unittest.makeSuite(Test_utilities, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
