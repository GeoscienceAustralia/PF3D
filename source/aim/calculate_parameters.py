"""Input column height
"""

column_height = 5000       # m
mass_eruption_rate = 1e5   # kg/m^3
volume = 4.3e6             # m^3
density = 700              # kg/m^3

#--------------------------------

mass = volume * density
duration = mass/mass_eruption_rate


print 'Column height:      %.2e m' % column_height
print 'Mass eruption rate: %.2e kg/m^3' % mass_eruption_rate
print 'Volume:             %.2e m^3' % volume
print 'Mass:               %.2e kg' % mass
print 'Duration:           %.3f hours' % (float(duration)/3600)
