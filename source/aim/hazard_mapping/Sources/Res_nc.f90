!***************************************************************
!*
!*    Module for NetCDF operations
!* 
!***************************************************************
     MODULE Res_nc
     use KindType
     implicit none
     save
!
     integer(ip), parameter :: maxdim = 100
     integer(ip)            :: ncID ,nDim, nVar, nAttr      
     integer(ip)            ::       iDim, iVar, iAttr, iD
!
     character(len=s_name) :: dimName(maxdim),varName(maxdim)
     integer(ip)           :: dimlen (maxdim),varDims(maxdim),varType(maxdim),varDimID(maxdim,maxdim)
     integer(ip)           :: ivoid  (maxdim)
!
!
     character(len=25 ) :: attr_units
     character(len=100) :: attr_title,attr_desc
     integer(ip)  :: nx_nc_ID
     integer(ip)  :: ny_nc_ID
     integer(ip)  :: nt_nc_ID
     integer(ip)  :: lon_nc_ID
     integer(ip)  :: lat_nc_ID
     integer(ip)  :: x_nc_ID
     integer(ip)  :: y_nc_ID
     integer(ip)  :: pisoc_nc_ID(10)
     integer(ip)  :: pload_nc_ID(10)
     integer(ip)  :: pfl300_nc_ID(10)
     integer(ip)  :: pfl250_nc_ID(10)
     integer(ip)  :: pfl200_nc_ID(10)
     integer(ip)  :: pfl150_nc_ID(10)
     integer(ip)  :: pfl100_nc_ID(10)
     integer(ip)  :: pFL050_nc_ID(10)
!
!*** Dimension variables name
!
     character(len=s_name) :: nc_lon_name  = 'lon'
     character(len=s_name) :: nc_lat_name  = 'lat'  
     character(len=s_name) :: nc_x_name    = 'x'
     character(len=s_name) :: nc_y_name    = 'y' 
     character(len=s_name) :: nc_alt_name  = 'alt'
     character(len=s_name) :: nc_tim_name  = 'time'    
!
     character(len=s_name) :: nc_load0_name = 'LOAD' 
     character(len=s_name) :: nc_fl300_name = 'C_FL300'     
     character(len=s_name) :: nc_fl250_name = 'C_FL250'
     character(len=s_name) :: nc_fl200_name = 'C_FL200'
     character(len=s_name) :: nc_fl150_name = 'C_FL150'
     character(len=s_name) :: nc_fl100_name = 'C_FL100'
     character(len=s_name) :: nc_fl050_name = 'C_FL050'
!
     character(len=s_name) :: nc_pisoc_name(10) 
     character(len=s_name) :: nc_pload_name(10)     
     character(len=s_name) :: nc_pfl300_name(10) 
     character(len=s_name) :: nc_pfl250_name(10) 
     character(len=s_name) :: nc_pfl200_name(10) 
     character(len=s_name) :: nc_pfl150_name(10) 
     character(len=s_name) :: nc_pfl100_name(10) 
     character(len=s_name) :: nc_pfl050_name(10) 
!
!*** Attribute names
!
     character(len=s_name) :: nc_coord_name  = 'COORDINATES' 
     character(len=s_name) :: nc_lonmin_name = 'LONMIN'
     character(len=s_name) :: nc_lonmax_name = 'LONMAX'
     character(len=s_name) :: nc_latmin_name = 'LATMIN'
     character(len=s_name) :: nc_latmax_name = 'LATMAX'
     character(len=s_name) :: nc_xmin_name   = 'XMIN'
     character(len=s_name) :: nc_xmax_name   = 'XMAX'
     character(len=s_name) :: nc_ymin_name   = 'YMIN'
     character(len=s_name) :: nc_ymax_name   = 'YMAX'
!
     END MODULE Res_nc