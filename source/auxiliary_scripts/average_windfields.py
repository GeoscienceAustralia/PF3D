"""Calculate averaged daily windfields and aggregrate


1: Calculate windfields for each time block averaged over all years available. 
2: Aggregate the individual hour blocks into a single file spanning the entire period

Note if layer boundaries are different, this function will use those from the first file.
"""


# FIXME: CURRENTLY NOT IN USE: Code to average wind profiles. This was used for the mnt Sinabung eruption but has not yet been integrated into AIM.
# It is an open question whether this approach makes sense. Perhaps we should average speed and direction separately.


import os, numpy


def average_windfields(input_filenames, output_filename):
    """Average windfields
    """
    
    # Read and summarise
    N = len(input_filenames)
    reading_first_file = True
    layers = []
    layer_data = {}
    for filename in input_filenames:
        print '    Reading', filename
        fid = open(filename)
        lines = fid.readlines()
        fid.close()
        
        # Read data
        for k, line in enumerate(lines[4:]):
            fields = line.split()
            layer = fields[0]
            
            # Data variables
            data = numpy.array([float(x) for x in fields[1:]])
            M = len(data)

            # Create list of variables first time around
            if reading_first_file:
                layers.append(layer)
                layer_data[layer] = numpy.array([0.0]*M)
                
            # Summarise for this layer
            #if k == 8: print '  ', data
            
            layer_data[layers[k]] += data
            #if k == 8: print '  ', layer_data[layers[k]]
            #print layers[k], data
                
        reading_first_file = False


    # Average layer data            
    for layer in layers:
        layer_data[layer] /= N


    #print '  RES', layer_data[layers[8]]
                
    # Write file with average layers    
    fid = open(output_filename, 'w')
  
    lines[1] = '2010'+lines[1][4:] # This year
    for line in lines[:4]:
        fid.write(line)
    
    for layer in layers:
        s = '\t%.2f'*M % tuple(layer_data[layer])
        fid.write(' %s %s\n' % (layer.ljust(10), s))
        
    fid.close()
    
    
def get_date_and_hour(filename):
    """Get date and hour from filename. E.g.
    
    ncep1_2004091312.profile
    
    returns
       091312
    
    """
        
    # Extract MMDDhh from filename
    basename, ext = os.path.splitext(filename)
    MMDDhh = basename[-6:]

    return MMDDhh
    

        
        
if __name__ == '__main__':                

    # Collect all files and sort them by date so that each entry will have 
    # data for that date from all years available.
    wind_data_files = {}
    
    for x in os.listdir('.'):
        if os.path.isdir(x):
            for y in os.listdir(x):
                if y.endswith('profile'):        
                
                    filename = os.path.join(x, y)
                    MMDDhh = get_date_and_hour(filename)
                    
                    if MMDDhh not in wind_data_files:
                        wind_data_files[MMDDhh] = []
                        
                    wind_data_files[MMDDhh].append(filename)    
        
    # Average each collection    
    for key in wind_data_files:
        #if key[:4] == '0909' and key[-2:] == '06':
        
        print 'Averaging date %s, hour %s' % (key[:4], key[-2:])
        average_windfields(wind_data_files[key], 'ncep1_average_%s.profile' % key)
            


