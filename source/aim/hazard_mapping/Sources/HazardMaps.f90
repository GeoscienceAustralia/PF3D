      program HazardMaps
!*****************************************************************************
!*
!*    AUTHOR : A.Folch
!*
!*    PURPOSE: This progrem reads a series of FALL3D NetCDF output files
!*             and computes hazard and isochron maps
!*
!*    INPUT FILES: 
!*           HazardMaps.inp       Contains list of netCDF files
!*           HazardMaps.pts       List of points (optional)
!*  
!*    OUTPUT FILES:
!*           HazardMaps.log       Log output file
!*           HazardMaps.res.nc    Final output in netCDF
!*           HazardMaps.res.pts   Final output at specific points (optional)
!*
!***************************************************************************** 
      use InpOut
      use Master
      implicit none
      logical :: found
!
!***  Opens the log file
!
      call openinp
!
!***  Reads the input file
!
      call readinp
!
!***  Loop over maps
!
      do imaps = 1,nmaps
!
!***     Reads results for the map imap
!
         fres = flist(imaps)
         call readres 
!
!***     Computes the isochrones for the map imap (nload values)
!
         if(pp_isoc) then
         isoc(:,:,:) = -1.
         do iload = 1,nload
            do it = 1,nt
               do iy =1,ny   
                  do ix =1,nx
                     if(load(ix,iy,it)   .ge.cload(iload).and. &
                        isoc(ix,iy,iload).eq.-1. ) then
                        isoc(ix,iy,iload) = times(it)-times(1) 
                     end if   
                  end do
              end do  
           end do
         end do
         end if
!      
!***     Computes load Hazard maps for all thresholds
!
         if(pp_load) then
         do iload = 1,nload
            do iy =1,ny   
               do ix =1,nx
                  if(load(ix,iy,nt).ge.cload(iload)) then 
                     pload(ix,iy,iload) = pload(ix,iy,iload) + 1.
                  end if   
               end do
            end do  
         end do
         end if
!    
!***     Computes FL050 hazard maps for all thresholds and all time instants
!
         if(pp_fl050) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(FL050(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pFL050(ix,iy,ifl) = pFL050(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes FL100 hazard maps for all thresholds and all time instants
!
         if(pp_fl100) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(FL100(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pFL100(ix,iy,ifl) = pFL100(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes FL150 hazard maps for all thresholds and all time instants
!
         if(pp_fl150) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(FL150(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pFL150(ix,iy,ifl) = pFL150(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes FL200 hazard maps for all thresholds and all time instants
!
         if(pp_fl200) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(FL200(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pFL200(ix,iy,ifl) = pFL200(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes FL250 hazard maps for all thresholds and all time instants
!
         if(pp_fl250) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(FL250(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pFL250(ix,iy,ifl) = pFL250(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes FL300 hazard maps for all thresholds and all time instants
!
         if(pp_fl300) then
         do ifl = 1,nfl
            do iy = 1,ny   
               do ix = 1,nx
                  found = .false.
                  do it = 1,nt
                     if(fl300(ix,iy,it).ge.cfl(ifl)) found = .true.
                  end do 
                  if(found) pfl300(ix,iy,ifl) = pfl300(ix,iy,ifl) + 1. 
               end do
            end do  
         end do
         end if
!    
!***     Computes at Isocrones for all maps (if ground load reaches a threshold
!***     value, then computes the averaged arrival time) 
!
         if(pp_isoc) then
         do iload = 1,nload
            do iy =1,ny   
               do ix =1,nx
                  if( isoc(ix,iy,iload).gt.-1.) then
                     pisoc(ix,iy,iload) = pisoc(ix,iy,iload) + isoc(ix,iy,iload)
                     nmaps_isoc(ix,iy,iload) = nmaps_isoc(ix,iy,iload) + 1
                   end if  
               end do
            end do  
         end do
         end if
!
      end do   ! imaps
!
!***  Normalization
!
      if(pp_load)  pload (:,:,:) = 100*pload (:,:,:)/nmaps
      if(pp_fl050) pFL050(:,:,:) = 100*pFL050(:,:,:)/nmaps
      if(pp_fl100) pFL100(:,:,:) = 100*pFL100(:,:,:)/nmaps
      if(pp_fl150) pFL150(:,:,:) = 100*pFL150(:,:,:)/nmaps
      if(pp_fl200) pFL200(:,:,:) = 100*pFL200(:,:,:)/nmaps
      if(pp_fl250) pFL250(:,:,:) = 100*pFL250(:,:,:)/nmaps
      if(pp_fl300) pfl300(:,:,:) = 100*pfl300(:,:,:)/nmaps
!
      if(pp_isoc) then
      do iload = 1,nload
         do iy =1,ny   
            do ix =1,nx
               if( nmaps_isoc(ix,iy,iload).gt.0) then
                  pisoc(ix,iy,iload) = pisoc(ix,iy,iload)/nmaps_isoc(ix,iy,iload)
               else
                  pisoc(ix,iy,iload) = -1.
               end if  
            end do
         end do  
      end do
      end if
!
!***  Writes results in netCDF format
!
      call wrires
!
!***  Reads and writes the points file
!
!      call readpts
!      call wripts
!
!***  Ends the program
!
      call runend('OK')
!
     end program HazardMaps