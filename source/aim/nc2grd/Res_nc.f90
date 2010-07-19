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
     integer(ip)            ::       iDim, iVar, iAttr
!
     character(len=s_name) :: dimName(maxdim),varName(maxdim)
     integer(ip)           :: dimlen (maxdim),varDims(maxdim),varType(maxdim),varDimID(maxdim,maxdim)
     integer(ip)           :: ivoid  (maxdim)
!
!*** Dimension variables name
!
     character(len=s_name) :: nc_lon_name  = 'lon'
     character(len=s_name) :: nc_lat_name  = 'lat'  
     character(len=s_name) :: nc_x_name    = 'x'
     character(len=s_name) :: nc_y_name    = 'y' 
     character(len=s_name) :: nc_alt_name  = 'alt'
     character(len=s_name) :: nc_time_name = 'time'    
!
!*** Variable names (defined later)
!
     character(len=s_name) :: nc_topog_name = 'TOPOGRAPHY'
     character(len=s_name) :: nc_load0_name = 'DEP_LOAD' 
     character(len=s_name) :: nc_loadc_name = 'DEP_LOAD_' 
     character(len=s_name) :: nc_thick_name = 'DEP_THICKNESS' 
     character(len=s_name) :: nc_concg_name = 'CONC_GROUND'
     character(len=s_name) :: nc_PM05g_name = 'PM05_GROUND'
     character(len=s_name) :: nc_PM10g_name = 'PM10_GROUND'
     character(len=s_name) :: nc_PM20g_name = 'PM20_GROUND' 
     character(len=s_name) :: nc_cumul_name = 'CUMMUL_CONCENTRATION' 
     character(len=s_name) :: nc_cumug_name = ' '
     character(len=s_name) :: nc_PM05c_name = 'PM05_CUMMUL'
     character(len=s_name) :: nc_PM10c_name = 'PM10_CUMMUL'
     character(len=s_name) :: nc_PM20c_name = 'PM20_CUMMUL' 
     character(len=s_name) :: nc_fl_name    = 'FL'
     character(len=s_name) :: nc_aot05_name = 'AOT_05_MICR'
     character(len=s_name) :: nc_cut3d_name = 'CONCENTRATION'
     character(len=s_name) :: nc_cut3g_name = ' '
     character(len=s_name) :: nc_cut3c_name = 'CONCE_'
!
!*** Attribute names
!
     character(len=s_name) :: nc_title_name  = 'TITLE'
     character(len=s_name) :: nc_coord_name  = 'COORDINATES' 
     character(len=s_name) :: nc_lonmin_name = 'LONMIN'
     character(len=s_name) :: nc_lonmax_name = 'LONMAX'
     character(len=s_name) :: nc_latmin_name = 'LATMIN'
     character(len=s_name) :: nc_latmax_name = 'LATMAX'
     character(len=s_name) :: nc_xmin_name   = 'XMIN'
     character(len=s_name) :: nc_xmax_name   = 'XMAX'
     character(len=s_name) :: nc_ymin_name   = 'YMIN'
     character(len=s_name) :: nc_ymax_name   = 'YMAX'
     character(len=s_name) :: nc_iyr_name    = 'YEAR'
     character(len=s_name) :: nc_imo_name    = 'MONTH'
     character(len=s_name) :: nc_idy_name    = 'DAY'
     character(len=s_name) :: nc_irunb_name  = 'RUN_START'
     character(len=s_name) :: nc_irune_name  = 'RUN_END'
!
!
     CONTAINS
!
!
!
     subroutine set_nc_names(fall3d_version)
!*********************************************************************
!*
!*   Sets the names of the NetCDF variables depending on the code
!*  version
!*
!********************************************************************
     implicit none
     character(len=10    ) :: fall3d_version
!
     if(TRIM(fall3d_version).eq.'6.0'.or.TRIM(fall3d_version).eq.'6.1') then
!
        nc_topog_name = 'TOPOGRAPHY'
        nc_load0_name = 'DEP_LOAD' 
        nc_loadc_name = 'DEP_LOAD_' 
        nc_thick_name = 'DEP_THICKNESS' 
        nc_concg_name = 'CONC_GROUND'
        nc_PM05g_name = 'PM05_GROUND'
        nc_PM10g_name = 'PM10_GROUND'
        nc_PM20g_name = 'PM20_GROUND' 
        nc_cumul_name = 'CUMMUL_CONCENTRATION' 
        nc_cumug_name = '***********'              ! not available
        nc_PM05c_name = 'PM05_CUMMUL'
        nc_PM10c_name = 'PM10_CUMMUL'
        nc_PM20c_name = 'PM20_CUMMUL' 
        nc_fl_name    = 'FL'
        nc_aot05_name = 'AOT_05_MICR'
        nc_cut3d_name = 'CONCENTRATION'
        nc_cut3g_name = '***********'              ! not available
        nc_cut3c_name = 'CONCE_'     
!     
      else if(TRIM(fall3d_version).eq.'6.2') then
!
        nc_topog_name = 'TOPOGRAPHY'
        nc_load0_name = 'LOAD' 
        nc_loadc_name = 'LOAD_CLASS' 
        nc_thick_name = 'THICKNESS' 
        nc_concg_name = 'C_GRND'
        nc_PM05g_name = 'C_PM05_GRND'
        nc_PM10g_name = 'C_PM10_GRND'
        nc_PM20g_name = 'C_PM20_GRND' 
        nc_cumul_name = 'COL_MASS' 
        nc_cumug_name = 'COL_MASS_'        ! gas name generic
        nc_PM05c_name = 'COL_MASSPM05'
        nc_PM10c_name = 'COL_MASSPM10'
        nc_PM20c_name = 'COL_MASSPM20' 
        nc_fl_name    = 'C_FL'
        nc_aot05_name = 'AOD'
        nc_cut3d_name = 'CON'
        nc_cut3g_name = 'CON_GAS_'         ! gas name generic
        nc_cut3c_name = 'CON_CLASS'     
!     
      end if        
!     
      return
      end subroutine set_nc_names           
!
     END MODULE Res_nc