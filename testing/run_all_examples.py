"""Run all examples in test area
"""

import os
from aim.interface import run_scenario

scenarios = ['mayon',  
             'galunggung', 
             'pinatubo',
             'merapi',                           
             'tambora']
        
for scenario_name in scenarios:

    aim = run_scenario('%s.py' % scenario_name, 
                       store_locally=True, 
                       timestamp_output=False,
                       verbose=True)


