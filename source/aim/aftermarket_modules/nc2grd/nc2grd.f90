     program nc2grd
!*****************************************************************************
!*
!*    AUTHOR       : A.Folch
!*    date         : JUN 2010 
!*                   Compatible with Fall3d-6.2 output format 
!*
!*    PURPOSE:  This progrem reads a NetCDF file (normally from a Fall3d
!*              simulation) and converts to a series of GRD file format
!*
!***************************************************************************** 
      use KindType
      use Master
      use InpOut
      use TimeFun
      use Res_nc
      implicit none
!
      integer(ip)       :: iarg,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,icut,k
      real   (rp)       :: dt
      character(len=2)  :: ext
!
!***  Gets filenames from the call arguments
!
      iarg = 1                          ! log     file
      call GETARG(iarg,flog)
      iarg = 2                          ! input   file
      call GETARG(iarg,finp)
      iarg = 3                          ! results file (NetCDF file)
      call GETARG(iarg,fres)
      iarg = 4                          ! basename for        GRD   postprocess files (without extension)
      call GETARG(iarg,fgrd)
!
!***  Opens the log file
!
      call openinp
!
!***  Reads input and points file
!
      call readat
!
!***  Reads the NetCDF results file
!
      call readres
!
!***  Fixes the names of the variables
!***  (this depends on the Fall3d version) 
!
      call set_nc_names(fall3d_version)
!
!***  Loop over variables               
!      
      do iVar = 1,nVar
!
!****    Topography
!
         if( (TRIM(varName(iVar)).eq.TRIM(nc_topog_name)).and.pp_topog) then
!        
             call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(1))
             call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
                
             name  = 'topography'
             fact  = fact_topog
             it    = 1 
             iz    = 1
             i3d = 0
             call wri_grd
!             
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_load0_name)).and.pp_load0) then      
!
!***     Deposit load
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!                                  
                name  = 'depload'
                fact  = fact_load0
                iz    = 1
                i3d = 0
                call wri_grd
!
             end do   
!
         else if( (varName(iVar)(1:LEN_TRIM(varName(iVar))-2).eq.TRIM(nc_loadc_name)).and.pp_loadc) then      
!
!***     Class deposit load
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!               
                ext   = varName(iVar)(LEN_TRIM(varName(iVar))-1:LEN_TRIM(varName(iVar)))                   
                name  = 'depload-'//TRIM(ext)
                fact  = fact_loadc
                iz    = 1
                i3d = 0
                call wri_grd
!
             end do  
!                
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_thick_name)).and.pp_thick) then
!
!***     Deposit thickness
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'depthick'
                fact  = fact_thick
                iz    = 1
                i3d = 0
                call wri_grd
!
             end do   
!
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_concg_name)).and.pp_concg) then
!
!***      Particle ground concentration 
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'concg'
                fact  = fact_concg
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!                
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM05g_name)).and.pp_PM05g) then
!
!***        PM05 concentration at ground (first layer)
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm05.ground'
                fact  = fact_PMxxg
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM10g_name)).and.pp_PM10g) then
!
!***        PM10 concentration at ground (first layer)
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm10.ground'
                fact  = fact_PMxxg
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM20g_name)).and.pp_PM20g) then
!
!***        PM20 concentration at ground (first layer)
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm20.ground'
                fact  = fact_PMxxg
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!              
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_cumul_name)).and.pp_cumul) then
!
!***       Total cummulative concentration (column mass)
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'colmass'
                fact  = fact_cumul
                iz    = 1
                i3d = 0
                call wri_grd
            end do
!              
         else if( (varName(iVar)(1:9).eq.TRIM(nc_cumug_name)).and.pp_cumug) then
!
!***       Gas cummulative concentration (column mass)
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'colmass'//varName(iVar)(10:12)
                fact  = fact_cumug
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!                
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM05c_name)).and.pp_PM05c) then
!
!***        PM05 cummulative concentration 
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm05.column'
                fact  = fact_PMxxc
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!            
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM10c_name)).and.pp_PM10c) then
!
!***        PM10 cummulative concentration
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm10.column'
                fact  = fact_PMxxc
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_PM20c_name)).and.pp_PM20c) then
!
!***        PM20 cummulative concentration 
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'pm20.column'
                fact  = fact_PMxxc
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!
         else if( (varName(iVar)(1:LEN_TRIM(varName(iVar))-3).eq.TRIM(nc_fl_name)).and.pp_fl) then
!
!***        Flight levels FLxxx
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                flm   = varName(iVar)(3:LEN_TRIM(varName(iVar)))     
                name  = 'FL'//TRIM(flm)
                fact  = fact_fl
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do    
!            
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_aot05_name)).and.pp_aot05) then
!
!***        AOT 
!
            do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!      
                name  = 'aot05'
                fact  = fact_aot05
                iz    = 1
                i3d = 0
                call wri_grd
!
            end do
!
         else if( (TRIM(varName(iVar)).eq.TRIM(nc_cut3d_name)).and.pp_cut3d) then
!
!***        Cuts for total concentration
!
            do icut = 1,ncut
                write(h(1:5),'(i5.5)') INT(zcut(icut)) 
                iz    = nz           
                do k  = 1, nz-1
                   if( (zlayer(k).lt.zcut(icut)).and.(zlayer(k+1).ge.zcut(icut)) ) iz = k
                end do
!            
                do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                   call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                   call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!     
                   name  = 'z'//h
                   fact  = fact_cut3d
                   i3d = 1
                   call wri_grd
!
                end do  
             end do              
!
         else if( (varName(iVar)(1:8).eq.TRIM(nc_cut3g_name)).and.pp_cut3g) then 
!
!***        Cuts some gas concentration
!
            do icut = 1,ncut
                write(h(1:5),'(i5.5)') INT(zcut(icut)) 
                iz    = nz            
                do k  = 1, nz-1
                   if( (zlayer(k).lt.zcut(icut)).and.(zlayer(k+1).ge.zcut(icut)) ) iz = k
                end do
!            
                do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                   call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                   call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!
                   name  = 'z'//h//'.'//varName(iVar)(9:LEN_TRIM(varName(iVar)))
                   fact  = fact_cut3g
                   i3d = 1
                   call wri_grd
!
                end do  
             end do    
!
         else if( (varName(iVar)(1:LEN_TRIM(varName(iVar))-2).eq.TRIM(nc_cut3c_name)).and.pp_cut3c) then 
!
!***        Cuts for some class concentration
!
            do icut = 1,ncut
                write(h(1:5),'(i5.5)') INT(zcut(icut)) 
                iz    = nz            
                do k  = 1, nz-1
                   if( (zlayer(k).lt.zcut(icut)).and.(zlayer(k+1).ge.zcut(icut)) ) iz = k
                end do
!            
                do it = 1,nt
!
!***            Gets the current time instant date = hh:mmZddmmmyyyy adding times to 00:00UTC
!
                   call addtime(iyr,imo,idy,0,0,i1yr,i1mo,i1dy,i1hr,i1mi,i1se,times(it))
                   call get_date(i1yr,i1mo,i1dy,i1hr,i1mi,date) 
!
                   ext   = varName(iVar)(LEN_TRIM(varName(iVar))-1:LEN_TRIM(varName(iVar)))
                   name  = 'z'//h//'.class-'//TRIM(ext)
                   fact  = fact_cut3c
                   i3d = 1
                   call wri_grd
!
                end do  
             end do    
!
         end if
!
      end do   ! end loop iVar = 1,nVar
!
!***  Ends the program
!
      call runend('OK')
      end program nc2grd