"""Filter AIM multiple scenarios for use with hazard mapping by time interval

This is used to produce seasonal hazard maps
"""

import string, os
from aim.utilities import makedir

def filter_hazard_outputs(input_directory,
                          start_month,
                          start_date,
                          end_month,
                          end_date):
                          
    
    first = '%s%s' % (string.zfill(start_month, 2), string.zfill(start_date, 2))
    last = '%s%s' % (string.zfill(end_month, 2), string.zfill(end_date, 2))    
    
    output_directory = input_directory + '_filtered_from_%s_to_%s' % (first, last)

    s = '/bin/rm -rf %s' % output_directory
    try:
        os.system(s)
    except:
        pass
    makedir(output_directory)
    
    files = os.listdir(input_directory)
    print 'Filtering %i files in %s from date %i/%i to %i/%i' % (len(files), input_directory, start_date, start_month, end_date, end_month)
    for filename in files:
        if not filename.endswith('.nc'): continue
        
        fields = filename.split('.')
        if len(fields) != 4: continue
        assert fields[-2] == 'res'
        
        x = fields[1]
        timefield = x.split('_')[1]

        assert len(timefield) == 10  # E.g. 2007012506  (YYYYMMDDhh)
        
        
        month = int(timefield[4:6])
        date  = int(timefield[6:8])
        
        if start_month <= month <= end_month and start_date <= date <= end_date:
            print timefield
            print start_month, month, end_month
            print start_date, date, end_date
            print
        
            s = 'cp %s/%s %s' % (input_directory, filename, output_directory)
            os.system(s)
        
    print 'Filtered hazard outputs created in %s' % output_directory

    
if __name__ == '__main__':
    
    filter_hazard_outputs(input_directory = 'merapi_multiple_wind_2000_2009_VEI2_outputs',
                          start_month=11,
                          start_date=1,
                          end_month=11,
                          end_date=30)


