#PF3D
**System requirements**
* A standard PC with at least 4GB RAM running Ubuntu Linux

**Dependancies**
* HDF5
* netCDF4
* netCDF4-python
* python-numpy
* python-scientific
* gfortran
* gdal-bin
* libnetcdf-dev

**Quick install**
* Download PF3D-v1.0.tar.gz
* tar zxvf PF3D-v1.0.tar.gz
* cd pf3d-1.0/source/aim
* python install_fall3d.py

##Project Description
Volcanic ash is the most widespread of all volcanic hazards and has the potential to affect hundreds of thousands, or even millions, of people across the Asia-Pacific region. Undertaking volcanic ash fallout hazard assessments is an important scientific, economic and political exercise and of great importance to public safety. One-third of the worlds largest volcanic eruptions that have occurred since 1800 have taken place within the Asia-Pacific. There is limited information available for this region on the hazard posed by volcanic ash, particularly from volcanoes that have not erupted in recent times. The potential impacts of volcanic ash fallout are widespread, varying and highly dependant on the scale of the eruption and the distance from source.

There is a need for computational models capable of accurately predicting volcanic ash dispersal both at ground level and suspended in the atmosphere when coupled with field observations of historical or on-going eruptive activity. To maximise the effectiveness of such models they should be readily accessible, easy to use and well tested. Geoscience Australia (GA) has been working since 2009 to develop tools and techniques for volcanic ash hazard modelling at multiple spatial scales.  

![ash particle](https://github.com/GeoscienceAustralia/PF3D/blob/master/images/ash_impacts.jpg)

*Images: Volcanic ash particle; volcanic ash covered crops and Volcanic ash impacts from the 2010 Mount Merapi eruption (Source: USGS)*

##Development 
The open-source computational model PF3D (python-FALL3D) was developed jointly between Geoscience Australia (GA), the Australia-Indonesia Facility for Disaster Reduction (AIFDR), Badan Geologi (Indonesia's Geological Agency), and the Philippines Institute for Volcanology and Seismology (PHIVOLCS) to assess the volcanic ash hazard on communities (with an emphasis on the Asia-Pacific region). This computational model is currenlty being used by government agencies in Australia, Indonesia, Papua New Guinea and the Philippines to generate deterministic, probabilisic and forecast scenarios for volcanic ash which will ultimately improve our understanding of the potential impact from volcanic eruptions and infrom disaster risk reduction decision making throughout the region. Some examples of PF3D output are provide below:

![ash load](https://github.com/GeoscienceAustralia/PF3D/blob/master/images/ash_load.jpg)

*Image: Ground load probability maps showing probability in % that the deposit load exceeds 1kg/m^2 (top) and 10kg/m^2 (bottom) for dry season (left) and rainy season (right) wind conditions* 

![ash accumulation](https://github.com/GeoscienceAustralia/PF3D/blob/master/images/ash_accumulation.jpg)

*Image: Isochron maps showing averaged accumulation time (in hours) for the volcanic ash load threshold values 1kg/m^2 (top) and 10kg/m^2 (bottom) for dry season (left) and rainy season (right) conditions.* 

**Source: Bear-Crozier, A.N., Kartadinata, N., Heriwaseso, A and Nielsen, O (2012). Development of python-FALL3D: a modified procedure for modelling volcanic ash dispersal in the Asia-Pacific region, Natural Hazards, Vol 64 (1), 821-838.** 

##Publications
###PF3D scientific journal articles
Bear-Crozier, A.N., Kartadinata, N., Heriwaseso, A and Nielsen, O (2012). Development of python-FALL3D: a modified procedure for modelling volcanic ash dispersal in the Asia-Pacific region, Natural Hazards, Vol 64 (1), 821-838.

Bear-Crozier, A.N., Kartadinata, N., Heriwaseso, A and Nielsen, O (in press). Evaluating volcanic ash ground loading hazard at Gunung Ciremai, West Java, Indonesia using PF3D, In: Geohazards in Indonesia, Geological Society of London Special Publication.

###Further recommended reading
Costa, A., Macedonio, G., Folch, A. (2006). A three-dimensional Eulerian model for transport and
deposition of volcanic ashes. Earth Planet. Sci. Lett., 241 (3-4), 634-647.

Folch, A., Jorba, O., and Viramonte, J. (2008). Volcanic ash forecast - application to the May 2008
Chaiten eruption, Nat. Hazards Earth Syst. Sci., 8, 927-940.

Scollo, S., A. Folch, A. Costa (2008). A parametric and comparative study of dierent tephra
fallout models, J. Volcanol. Geotherm. Res., 176, 199-211.

Folch A., C. Cavazzoni, A. Costa, G. Macedonio (2008). An automatic procedure to forecast tephra
fallout, J. Volcanol. Geotherm. Res., 177, 767-777.

Macedonio G., A. Costa, A. Folch (2008). Ash fallout scenarios at Vesuvius: Numerical simulations
and implications for hazard assessment, J. Volcanol. Geotherm. Res., 178, 366-377.

Folch A., Costa A., Macedonio G. (2009). FALL3D: A Computational Model for Volcanic Ash
Transport and Deposition, Comput. Geosci., doi:10.1016/j.cageo.2008.08.008.

Scollo S., Prestilippo M., Spata G., D'Agostino M., Coltelli M. (2009). Monitoring and forecasting
Etna volcanic plumes, Nat. Hazards Earth Syst. Sci., 9, 1573-1585.

Costa A., A. Folch, G. Macedonio (2010). A Model for Wet Aggregation of Ash Particles in
Volcanic Plumes and Clouds: I. Theoretical Formulation, J. Geophys. Res., Vol. 115, B09201,
doi:10.1029/2009JB007175.

Folch A., A. Costa, A. Durant,G. Macedonio (2010). A Model for Wet Aggregation of Ash Particles
in Volcanic Plumes and Clouds: II. Model Application, J. Geophys. Res., Vol. 115, B09202,
doi:10.1029/2009JB007176.

Folch A., Sulpizio R. (2010). Evaluating long-range volcanic ash hazard using supercomputing facilities:
application to Somma-Vesuvius (Italy), and consequences for civil aviation over the Central
Mediterranean Area, Bull. Volc., Vol. 72 (9), 1039-1059, doi:10.1007/s00445-010-0386-3.

Scollo S., A. Folch, M. Coltelli, V.J. Realmuto (2010). Three-dimensional volcanic aerosol dispersal:
A comparison between Multiangle Imaging Spectroradiometer (MISR) data and numerical
simulations, J. Geophys. Res., 115, D24210, doi:10.1029/2009JD013162.

Corradini S., Merucci L., Folch A. (2011). Volcanic Ash Cloud Properties: Comparison Between
MODIS Satellite Retrievals and FALL3D Transport Model, IEEE Geoscience and Remote Sensing
Letters, Vol. 8, 248-252, doi:10.1109/LGRS.2010.2064156.

Folch A., Costa A., Basart S. (2012). Validation of the FALL3D ash dispersion model using observations
of the 2010 Eyjafjallajokull volcanic ash cloud, Atmos. Environ., Vol. 48, 165-183,
doi:10.1016/j.atmosenv.2011.06.072.

Scaini C., Folch A., Navarro M. (2012). Tephra hazard assessment at Concepcion Volcano, Nicaragua,
J. Volcanol. Geotherm. Res., Volumes 219-220, 41-51 doi:10.1016/j.jvolgeores.2012.01.007.

Costa A., Folch A., Macedonio G., Giaccio B., Isaia R., Smith V.C. (2012) Quantifying volcanic
ash dispersal and impact from Campanian Ignimbrite super-eruption, Geophys. Res. Lett., Vol.
39, doi:10.1029/2012GL051605.

Bonasia R., Costa A., Folch A., Capra L., Macedonio G. (2012). Numerical simulation of tephra
transport and deposition of the 1982 El Chichon eruption, J. Volcanol. Geotherm. Res., doi:10.1016/j.jvolgeores.2012.04.006.

Sulpizio, R., Folch, A., Costa, A., Scaini, C., Dellino, P. (2012). Civil aviation hazard assessment of
far-range volcanic ash dispersal from a violent Strombolian eruption scenario at Somma-Vesuvius
volcano, Naples, Italy, Bulletin of volcanology, doi:10.1007/s00445-012-0656-3.

Collini, E., Osores, S., Folch, A., Viramonte, J.G., Villarosa, G., Salmuni, G. (2013). Volcanic ash
forecast during the June 2011 Cordon-Caulle, Natural Hazards, 66(2), 389-412, doi:10.1007/s11069-
012-0492-y.

Osores, M.S., Folch, A., Collini, E., Villarosa, G., Durant, A., Pujol, G., Viramonte, J.G. (2013).
Validation of the FALL3D model for the 2008 Chaiten eruption using eld, laboratory and satellite
data, Andean Geology, 40 (2): 262-276.
