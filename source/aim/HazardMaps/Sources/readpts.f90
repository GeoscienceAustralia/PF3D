     subroutine readpts
!****************************************************************
!*
!*   Reads the deposit list of points.
!*
!****************************************************************
     use KindType
     use InpOut
     use Master
	 implicit none
!
     logical               :: go_on
     character(len=s_mess) :: word
     character(len=1)      :: cvoid
     integer  (ip)         :: info
!
!*** Get the number of points
!
     open(99,FILE=TRIM(fpts),STATUS='unknown',ERR=100)
     go_on = .true.
	 do while(go_on)
       read(99,*,iostat=info) cvoid
        if(info /= 0) then
          go_on = .false.
        else
          npts = npts + 1
        end if
     end do
!
!*** Allocates memory for vectors related to npts 
!
     allocate(use_pts(npts))
     use_pts = .false.
	 allocate(lat_pts(npts))
	 allocate(lon_pts(npts))
     allocate(nam_pts(npts))
     allocate(dis_pts(npts))
     allocate(pload_pts(npts,nload))
     allocate(pisoc_pts(npts,nload))
     allocate(pFL050_pts(npts,nfl))
     allocate(pFL100_pts(npts,nfl))
     allocate(pFL150_pts(npts,nfl))
     allocate(pFL200_pts(npts,nfl))
     allocate(pFL250_pts(npts,nfl))
     allocate(pFL300_pts(npts,nfl))
!
!*** Reads points 
!
     rewind(99)
     do ipts = 1,npts
        read(99,*) nam_pts(ipts), lat_pts(ipts), lon_pts(ipts) 
     end do
     close(99)
!
!*** Averiguates which points lay within the computational domain  
!
      do ipts = 1,npts
          if( (lon_pts(ipts).ge.lonmin).and.(lon_pts(ipts).le.lonmax).and. &
              (lat_pts(ipts).ge.latmin).and.(lat_pts(ipts).le.latmax)) use_pts(ipts) = .true.
      end do
!
     return
!
!***  List of errors
!
  100 call runend('Error opening the points file '//TRIM(fpts))
!  
     end subroutine readpts