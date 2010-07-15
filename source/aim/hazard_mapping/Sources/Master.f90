!***************************************************************
!*
!*		Module for master operations
!* 
!***************************************************************
 MODULE Master
   use KindType
   IMPLICIT NONE
   SAVE
!
!***  Grid 
!
      character(len=10) :: coord_sys
      integer(ip) :: nx ,ny ,nz ,nt ,ix,iy,it
      integer(ip) :: nx0,ny0,nz0,nt0
      real   (rp) :: lonmin ,lonmax ,latmin ,latmax ,dlon,dlat,lon_v,lat_v
      real   (rp) :: lonmin0,lonmax0,latmin0,latmax0
      real   (rp) ::   xmin ,  xmax ,  ymin ,  ymax ,  dx,  dy
      real   (rp) ::   xmin0,  xmax0,  ymin0,  ymax0
!
!***  Maps
!
      integer(ip) :: nmaps,imaps
!
!***  Variables
!
      logical :: pp_load,pp_isoc,pp_FL050,pp_FL100,pp_FL150,pp_FL200,pp_FL250,pp_FL300
!
      real(rp), allocatable :: lon(:),lat(:),times(:)
!      
      real(rp), allocatable :: work2d(:,:)       ! work2d(nx,ny)
      real(rp), allocatable :: load  (:,:,:)     ! load (nx,ny,nt)      Time-dependent deposit load     
      real(rp), allocatable :: FL300 (:,:,:)     ! FL300(nx,ny,nt)      Time-dependent FL300 concentration
      real(rp), allocatable :: FL250 (:,:,:)     ! FL250(nx,ny,nt)      Time-dependent FL250 concentration
      real(rp), allocatable :: FL200 (:,:,:)     ! FL200(nx,ny,nt)      Time-dependent FL200 concentration
      real(rp), allocatable :: FL150 (:,:,:)     ! FL150(nx,ny,nt)      Time-dependent FL150 concentration
      real(rp), allocatable :: FL100 (:,:,:)     ! FL100(nx,ny,nt)      Time-dependent FL100 concentration
      real(rp), allocatable :: FL050 (:,:,:)     ! FL050 (nx,ny,nt)     Time-dependent FL050  concentration
!
      integer(ip), allocatable :: nmaps_isoc(:,:,:)
      real(rp), allocatable :: isoc   (:,:,:)    ! isoc   (ny,nx,nload)  Isochrones
      real(rp), allocatable :: pisoc  (:,:,:)    ! pisoc  (ny,nx,nload)  Maps for isochrones
      real(rp), allocatable :: pload  (:,:,:)    ! pload  (ny,nx,nload)  Maps for different cload
      real(rp), allocatable :: pFL300 (:,:,:)    ! pFL300 (ny,nx,nfl  )  Maps for different cfl
      real(rp), allocatable :: pFL250 (:,:,:)    ! pFL250 (ny,nx,nfl  )  Maps for different cfl
      real(rp), allocatable :: pFL200 (:,:,:)    ! pFL200 (ny,nx,nfl  )  Maps for different cfl
      real(rp), allocatable :: pFL150 (:,:,:)    ! pFL150 (ny,nx,nfl  )  Maps for different cfl
      real(rp), allocatable :: pFL100 (:,:,:)    ! pFL100 (ny,nx,nfl  )  Maps for different cfl
      real(rp), allocatable :: pFL050 (:,:,:)    ! pFL050  (ny,nx,nfl )  Maps for different cfl
!
!***  Plot related variables
!
      integer(ip), parameter        :: mxnval = 10   ! max number of "loads" and "FL" thresholds
      integer(ip)                   :: nload,iload   ! load values
      real   (rp),dimension(mxnval) :: cload
      integer(ip)                   :: nfl  ,ifl     ! FL concentration values
      real   (rp),dimension(mxnval) :: cfl
!
!***  Points
!
      integer(ip) :: npts,ipts
      logical              , allocatable :: use_pts(:)
      character(len=s_name), allocatable :: nam_pts(:)
	  real(rp)             , allocatable :: lat_pts(:),lon_pts(:),dis_pts(:)
	  real(rp)             , allocatable :: pload_pts(:,:), & 
	                                        pisoc_pts(:,:), &
	                                        pFL050_pts(:,:), &
	                                        pFL100_pts(:,:), &
	                                        pFL150_pts(:,:), &	                                        
	                                        pFL200_pts(:,:), &
	                                        pFL250_pts(:,:), &	
	                                        pFL300_pts(:,:)
!
 END MODULE Master