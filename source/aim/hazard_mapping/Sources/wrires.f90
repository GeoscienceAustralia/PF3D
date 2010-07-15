     subroutine wrires
!**************************************************************************
!*
!*   Writes results (including coordinate variables) in netCDF format
!*
!**************************************************************************
     use KindType
     use InpOut
     use Master
     use Res_nc
     use netcdf
     implicit none
!
     integer(ip)           :: istat
     character(len=s_name) :: nc_name
     character(len=1     ) :: ext 
!
!*** Open netCDF file (define mode) and get ncID
!
     istat = nf90_create(TRIM(fout),NF90_CLOBBER, ncID)  
     if( istat /= 0 ) call runend('wrires : Error in nf90_create')
!
!**  Define dimensions
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
!
         istat = nf90_def_dim(ncID, nc_lon_name , nx, nx_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for lon')
         istat = nf90_def_dim(ncID, nc_lat_name , ny, ny_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for lat')
         istat = nf90_def_dim(ncID, nc_tim_name , 1 , nt_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for time')
!
     case('UTM')
!
         istat = nf90_def_dim(ncID, nc_x_name, nx, nx_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for x')
         istat = nf90_def_dim(ncID, nc_y_name, ny, ny_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for y')     
         istat = nf90_def_dim(ncID, nc_tim_name , 1 , nt_nc_ID ) 
         if( istat /= 0 ) call runend('wrires : error in nf90_def_dim for time')
!
     END SELECT
!
!*** Define coordinate variables 
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
!
        istat = nf90_def_var(ncID, nc_lon_name ,NF90_FLOAT, (/nx_nc_ID/), lon_nc_ID) 
        if( istat /= 0 ) call runend('wrires : error in nf90_def_variable for variable '//TRIM(nc_lon_name))
        istat = nf90_def_var(ncID, nc_lat_name ,NF90_FLOAT, (/ny_nc_ID/), lat_nc_ID) 
        if( istat /= 0 ) call runend('wrires : error in nf90_def_variable for variable '//TRIM(nc_lat_name))
!
     case('UTM')
!
        istat = nf90_def_var(ncID, nc_x_name ,NF90_FLOAT, (/nx_nc_ID/), x_nc_ID) 
        if( istat /= 0 ) call runend('wrires : error in nf90_def_variable for variable '//TRIM(nc_x_name))
        istat = nf90_def_var(ncID, nc_y_name ,NF90_FLOAT, (/ny_nc_ID/), y_nc_ID) 
        if( istat /= 0 ) call runend('wrires : error in nf90_def_variable for variable '//TRIM(nc_y_name))
!
     END SELECT           
!
!*** Define the rest of variables 
!
     if(pp_load) then
     do iload = 1,nload
         write(ext(1:1),'(i1.1)') iload
         nc_pload_name(iload) = 'PLOAD_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pload_name(iload), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pload_nc_ID(iload))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pload_name(iload)))
     end do
     end if
!
     if(pp_fl050) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pFL050_name(ifl) = 'PFL050_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pFL050_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pFL050_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pFL050_name(ifl)))
     end do
     end if
!
     if(pp_fl100) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pFL100_name(ifl) = 'PFL100_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pFL100_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pFL100_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pFL100_name(ifl)))
     end do
     end if
!
     if(pp_fl150) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pFL150_name(ifl) = 'PFL150_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pFL150_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pFL150_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pFL150_name(ifl)))
     end do
     end if
!
     if(pp_fl200) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pFL200_name(ifl) = 'PFL200_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pFL200_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pFL200_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pFL200_name(ifl)))
     end do
     end if
!
     if(pp_fl250) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pFL250_name(ifl) = 'PFL250_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pFL250_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pFL250_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pFL250_name(ifl)))
     end do
     end if
!
     if(pp_fl300) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         nc_pfl300_name(ifl) = 'PFL300_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pfl300_name(ifl), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pfl300_nc_ID(ifl))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pfl300_name(ifl)))
     end do
     end if
!
     if(pp_isoc) then
     do iload = 1,nload
         write(ext(1:1),'(i1.1)') iload
         nc_pisoc_name(iload) = 'ISOCHRO_'//TRIM(ext)
         istat = nf90_def_var(ncID, nc_pisoc_name(iload), NF90_FLOAT, (/nx_nc_ID,ny_nc_ID,nt_nc_ID/), pisoc_nc_ID(iload))
         if( istat /= 0 ) call runend('wrires : error in nf90_def_var for variable '//TRIM(nc_pisoc_name(iload)))
     end do
     end if
!
!*** Define attributes for coordinate variables
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
!
       attr_desc  = 'longitude. East positive'
       attr_units = 'degrees_east'  
       istat = nf90_put_att(ncID, lon_nc_ID, 'units', attr_units)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, lon_nc_ID, 'description', attr_desc) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!     
       attr_desc  = 'latitude. North positive'
       attr_units = 'degrees_north'  
       istat = nf90_put_att(ncID, lat_nc_ID, 'units', attr_units)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, lat_nc_ID, 'description', attr_desc) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!
     case('UTM')
!
       attr_desc  = 'UTM. West-East distance'
       attr_units = 'm'  
       istat = nf90_put_att(ncID, x_nc_ID, 'units', attr_units)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, x_nc_ID, 'description', attr_desc) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!     
       attr_desc  = 'UTM. South-North distance'
       attr_units = 'm'  
       istat = nf90_put_att(ncID, y_nc_ID, 'units', attr_units)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, y_nc_ID, 'description', attr_desc) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!
     END SELECT
!
!*** Define attributes for other variables
!
     if(pp_load) then
     do iload = 1,nload
         write(ext(1:1),'(i1.1)') iload
         attr_desc  = 'Probability for load '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pload_nc_ID(iload), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pload_nc_ID(iload), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pload_nc_ID(iload), 'value', real(cload(iload))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl050) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pFL050_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL050_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL050_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl100) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pFL100_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL100_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL100_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl150) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pFL150_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL150_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL150_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl200) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pFL200_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL200_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL200_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl250) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pFL250_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL250_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pFL250_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_fl300) then
     do ifl = 1,nfl
         write(ext(1:1),'(i1.1)') ifl
         attr_desc  = 'Probability for concentration threshold '//TRIM(ext)    
         attr_units = 'in %'  
         istat = nf90_put_att(ncID, pfl300_nc_ID(ifl), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pfl300_nc_ID(ifl), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pfl300_nc_ID(ifl), 'value', real(cfl(ifl))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
     if(pp_isoc) then
     do iload = 1,nload
         write(ext(1:1),'(i1.1)') iload
         attr_desc  = 'Averaged arrival time for load '//TRIM(ext)    
         attr_units = 'in h'  
         istat = nf90_put_att(ncID, pisoc_nc_ID(iload), 'units', attr_units) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pisoc_nc_ID(iload), 'description', attr_desc) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
         istat = nf90_put_att(ncID, pisoc_nc_ID(iload), 'value', real(cload(iload))) 
         if( istat /= 0 ) call runend('wrires : error in nf90_put_att')      
     end do
     end if
!
!*** Put global attributes 
!
     attr_title = 'Fall3d 6.0 results'
     istat = nf90_put_att(ncID, NF90_GLOBAL, 'TITLE', attr_title) 
     if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!
     attr_title = TRIM(coord_sys)
     istat = nf90_put_att(ncID, NF90_GLOBAL, 'COORDINATES', attr_title) 
     if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'LONMIN', lonmin)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'LATMIN', latmin) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'LONMAX', lonmax) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'LATMAX', latmax) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
     case('UTM')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'XMIN', xmin) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'YMIN', ymin) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'XMAX', xmax)
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
       istat = nf90_put_att(ncID, NF90_GLOBAL, 'YMAX', ymax) 
       if( istat /= 0 ) call runend('wrires : error in nf90_put_att')
     END SELECT          
!
!*** Leave the define mode 
!
     if( nf90_enddef(ncID) /= 0 ) call runend('wrires: error in nf90_enddef')
!
!*** Write coordinate variables
!     
     SELECT CASE(coord_sys)
     case('LON-LAT')
       istat = nf90_put_var(ncID, lon_nc_ID, lon) 
       if( istat /= 0 ) call runend('wrires: error in nf90_put_var for varialbe lon')
       istat = nf90_put_var(ncID, lat_nc_ID, lat) 
       if( istat /= 0 ) call runend('wrires: error in nf90_put_var for varialbe lat')
     case('UTM')
       istat = nf90_put_var(ncID, x_nc_ID,lon)
       if( istat /= 0 ) call runend('wrires: error in nf90_put_var for varialbe x')
       istat = nf90_put_var(ncID, y_nc_ID, lat) 
       if( istat /= 0 ) call runend('wrires: error in nf90_put_var for varialbe y')
     END SELECT
!
!*** Closes the file and re-opens in write mode
!
     if( nf90_close(ncID)  /= 0 ) call runend('wrires: Error in closing the file') 
     if( nf90_open(TRIM(fout),NF90_WRITE, ncID) /= 0 ) call runend('wrires : Error in nf90_open')
!
!*** Write the rest of variables
!   
     if(pp_load) then   
     do iload = 1,nload
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pload(ix,iy,iload)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pload_name(iload),pload_nc_ID(iload))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pload')
        istat = nf90_put_var(ncID, pload_nc_ID(iload),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pload')
     end do
     end if
!
     if(pp_fl050) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pFL050(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pFL050_name(ifl),pFL050_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pFL050')
        istat = nf90_put_var(ncID, pFL050_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pFL050')
     end do
     end if
!
     if(pp_fl100) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pFL100(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pFL100_name(ifl),pFL100_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pFL100')
        istat = nf90_put_var(ncID, pFL100_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pFL100')
     end do
     end if
!
     if(pp_fl150) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pFL150(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pFL150_name(ifl),pFL150_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pFL150')
        istat = nf90_put_var(ncID, pFL150_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pFL150')
     end do
     end if
!
     if(pp_fl200) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pFL200(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pFL200_name(ifl),pFL200_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pFL200')
        istat = nf90_put_var(ncID, pFL200_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pFL200')
     end do
     end if
!
     if(pp_fl250) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pFL250(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pFL250_name(ifl),pFL250_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pFL250')
        istat = nf90_put_var(ncID, pFL250_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pFL250')
     end do
     end if
!
     if(pp_fl300) then
     do ifl = 1,nfl
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pfl300(ix,iy,ifl)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pfl300_name(ifl),pfl300_nc_ID(ifl))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pfl300')
        istat = nf90_put_var(ncID, pfl300_nc_ID(ifl),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pfl300')
     end do
     end if
!     
     if(pp_isoc) then
     do iload = 1,nload
        do ix=1,nx
           do iy=1,ny
              work2d(ix,iy)= pisoc(ix,iy,iload)
           end do
        end do
        istat = nf90_inq_varid(ncID,nc_pisoc_name(iload),pisoc_nc_ID(iload))
        if( istat /= 0 ) call runend('wrires: error in nf90_inq_varid for variable pisoc')
        istat = nf90_put_var(ncID, pisoc_nc_ID(iload),work2d,start=(/1,1,1/),count=(/nx,ny,1/))
        if( istat /= 0 ) call runend('wrires: error in nf90_put_var for variable pisoc')
     end do
     end if
!
!*** Closes the file
!
     if ( nf90_close(ncID) /=0 ) call runend('wrires: Error in closing the file') 
!     
     return
     end subroutine wrires    