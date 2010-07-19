     subroutine wri_grd 
!************************************************************
!*
!*   Writes a file block in grd format (e.g. for SURFER)
!*
!************************************************************
     use KindType
     use Res_nc
     use Master
     use InpOut
     use netcdf
     implicit none
     
     integer(ip),save :: ipass = 0
     integer(ip) :: ilen
     real   (rp) :: xo,yo,dxo,dyo

!*** If necessary allocates memory
     if(ipass.eq.0) then
        ipass = 1
        allocate(work2d(nx,ny))
        allocate(work3d(nx,ny,nz))         
     end if

!***  File name (date is in format hh:mmZddmmmyyyy) ! NO IT IS NOT
     fname = TRIM(fgrd)//'.'
         ilen = LEN_TRIM(fname)
	 write(fname(ilen+1:ilen+9),'(a)') date(7:15)       ! time
     fname = TRIM(fname)//'.'	 
	 ilen = LEN_TRIM(fname)
	 write(fname(ilen+1:ilen+5),'(a)') date(1:5)  
     fname = TRIM(fname)//'.'//TRIM(name)//'.grd'

!*** Gets dimensions
     SELECT CASE(coord_sys)
     case('LON-LAT')
        xo  = lonmin
        yo  = latmin
        dxo = dlon
        dyo = dlat
     case('UTM')
        xo  = xmin
        yo  = ymin
        dxo = dx
        dyo = dy
     END SELECT
!
!*** Reads the results
!
     if(i3d.eq.0) then 
       if( nf90_get_var(ncID,iVar,work2d,start=(/1,1,it/)) /=0 ) &
          call runend('readres: Error reading nc file')
!
     else if(i3d.eq.1) then 
       if( nf90_get_var(ncID,iVar,work3d,start=(/1,1,1,it/)) /=0 ) &
          call runend('readres: Error reading nc file')
       work2d(1:nx,1:ny) = work3d(1:nx,1:ny,iz)
     end if
!  
!*** Writes the results
!
     call wrigrd(fname,nx,ny,xo,yo,dxo,dyo,work2d)   
!
     return
     end subroutine wri_grd 
!
!
!
      subroutine wrigrd(fname,nx,ny,xo,yo,dx,dy,f)
!************************************************************
!*
!*    Writes GRD file in format surfer (ASCII version)
!* 
!************************************************************
      use KindType
      implicit none
      integer(ip) :: nx,ny
      real   (rp) :: xo,yo,dx,dy
	  real   (rp) :: f(*)
      character(len=s_file) :: fname
!
      integer(ip) :: ix,iy,ipos
	  real   (rp) :: fmin,fmax
!
!***  Computes the maximum and the minimum
!
      fmax = -1d20
      fmin =  1d20
      do ipos=1,nx*ny
        if(f(ipos).gt. 1d40) f(ipos) =  1d40
		if(f(ipos).lt.-1d40) f(ipos) = -1d40
!
	    if(f(ipos).gt.fmax) fmax=f(ipos)
	    if(f(ipos).lt.fmin) fmin=f(ipos)
      end do
!
!***  Starts to write
!
      open(99,file=TRIM(fname),status='unknown')
      write(99,'(a4          )') 'DSAA'
      write(99,'(i4  ,1x,i4  )') nx,ny
      write(99,'(f9.1,1x,f9.1)') xo,xo+(nx-1)*dx
      write(99,'(f9.1,1x,f9.1)') yo,yo+(ny-1)*dy
      write(99,'(e13.6,1x,e13.6)') fmin,fmax
!
      do iy=1,ny
	   write(99,10) (f(ipos),ipos=(iy-1)*nx+1,iy*nx)
      end do
  10  format(1000(e13.6,1x))
!
      close(99)
      return
      end subroutine wrigrd
