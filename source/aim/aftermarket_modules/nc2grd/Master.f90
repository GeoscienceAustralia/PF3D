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
      logical :: pp_topog = .false.
      logical :: pp_load0 = .false.
      logical :: pp_loadc = .false.
      logical :: pp_thick = .false.
      logical :: pp_concg = .false.
      logical :: pp_PM05g = .false.
      logical :: pp_PM10g = .false.
      logical :: pp_PM20g = .false.
!
      logical :: pp_cumul = .false.
      logical :: pp_cumug = .false.
      logical :: pp_PM10c = .false.
      logical :: pp_PM05c = .false.
      logical :: pp_PM20c = .false.
      logical :: pp_fl    = .false.
      logical :: pp_aot05 = .false.
!                        
      logical :: pp_cut3d = .false.
      logical :: pp_cut3g = .false.
      logical :: pp_cut3c = .false.
!
!*** Title and version
!
      character(len=10    ) :: fall3d_version
      character(len=s_mess) :: title_nc
!
!***  Grid 
!
      character(len=10) :: coord_sys
      integer(ip) :: nx,ny,nz,nt,iz
      real   (rp) :: lonmin,lonmax,latmin,latmax,dlon,dlat
      real   (rp) ::   xmin,  xmax,  ymin,  ymax,  dx,  dy
      integer(ip), parameter  :: mxzval = 500  ! max number of zvalues
!
      real(rp) :: zlayer(mxzval)
!
!***  Time
!
      character(len=15) :: date
      integer(ip) :: it,ifl,iyr,imo,idy,ihr,imi,irunb,irune
      real   (rp),allocatable :: times(:)
!
!***  Surfer related variables
!
      integer(ip) :: i3d
      real(rp), allocatable :: work2d(:,:),work3d(:,:,:)
!
!***  Plot related variables
! 
      real(rp) :: &
         fact, &
         fact_topog, &
         fact_load0, &
         fact_loadc, &
         fact_thick, &
         fact_concg, &
         fact_PMxxg, &
         fact_cumul, &
         fact_cumug, &
         fact_PMxxc, &
         fact_fl,    &
         fact_aot05, &
         fact_cut3d, &
         fact_cut3g, &
         fact_cut3c
!                                     
      character(len=s_name) :: &
         unit, &
         unit_topog, &
         unit_load0, &
         unit_loadc, &
         unit_thick, &
         unit_concg, &
         unit_PMxxg, &
         unit_cumul, &
         unit_cumug, &
         unit_PMxxc, &
         unit_fl,    &
         unit_aot05, &
         unit_cut3d, &
         unit_cut3g, &
         unit_cut3c                          
!
!***  Vertical postprocess cuts
!
      integer(ip),parameter         ::  mxncut = 100  ! max number of 3D cuts
      integer(ip)                   ::  ncut
      real   (rp),dimension(mxncut) ::  zcut  
!
 END MODULE Master
