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
!*** Grib mesoscal/global model
!
     character(len=25) :: date
     integer(ip) :: ibyr,ibmo,ibdy,ibhr,ibmi,ibse,dt
     integer(ip) :: iyr,imo,idy,ihr,imi,ise
     integer(ip) :: nx,ny,nz,nt,np,ix,iy,iz,it,it1,it2
     integer(ip) :: ieyr,iemo,iedy,iehr,iemi,iese
     real   (rp) :: cen_lon,cen_lat,missing_value
!
!*** Input data
!
     real   (rp) :: lon_v,lat_v
     integer(ip) :: pbyr,pbmo,pbdy,pbhr
     integer(ip) :: peyr,pemo,pedy,pehr
!
!*** Output data
!
     integer(ip) :: ilen
     real   (rp) :: date0,date1
!
!*** Variables 
!     
     real(rp), allocatable :: level(:) 
     real(rp), allocatable :: lon  (:)
     real(rp), allocatable :: lat  (:)  
     real(rp), allocatable :: u    (:,:) 
     real(rp), allocatable :: v    (:,:)
     real(rp), allocatable :: T    (:,:)
     real(rp), allocatable :: H    (:,:)
     real(rp), allocatable :: umod (:,:)
     real(rp), allocatable :: udir (:,:)
     real(rp), allocatable :: work (:,:,:)     
!
!*** Input netCDF 
!
     integer(ip) :: ncID ,nDim, nVar, nAttr, nDimMax, iD
     integer(ip) :: varID,iDim, iVar, iAttr
!
     character(len=50) :: vancname
     character(len=50), allocatable :: dimName(:),varName(:)
     integer(ip)      , allocatable :: dimlen (:),varDims(:),varType(:),varDimID(:,:),ivoid(:)
!     
     real(rp) :: t2,t1,add_offset,scale_factor
     real(rp) :: data_lon_range(2),data_lat_range(2),data_level_range(2),data_time_range(2)
     
!
 END MODULE Master