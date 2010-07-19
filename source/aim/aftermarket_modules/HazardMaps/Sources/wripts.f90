      subroutine wripts
!**********************************************************
!*    
!*    Writes the points file
!*
!*********************************************************
      use KindType
      use InpOut
      use Master
      implicit none
!
      character(len=s_file) :: string1,string2,string3
      logical  :: found
      integer(ip) :: ipt,jpt,ilen
      real(rp) :: pi = 3.14159265358979323846_rp   ! pi
      real(rp) :: Rearth = 6356d3                  ! Earth's radius
      real(rp) :: lonp,latp,latv,lonv      
      real(rp) :: x,y,s,t,shape(4)
!       
!***  First computes distance from the vent
!
      SELECT CASE(coord_sys)
      case('LON-LAT')  
        do ipts = 1,npts
           latp = lat_pts(ipts)*pi/180_rp
           lonp = lon_pts(ipts)*pi/180_rp 
           latv = lat_v*pi/180_rp
           lonv = lon_v*pi/180_rp                     
           dis_pts(ipts) = Rearth*acos(sin(latp)*sin(latv) + cos(latp)*cos(latv)*cos(lonp-lonv))
        end do
      case('UTM')  
        call runend('UTM distance not implemented')
      END SELECT 
!
!***  Ordinates the points by increasing distance
!
      call order_pts(lon_pts,lat_pts,dis_pts,nam_pts,npts)
!
!***  Computes pload_pts and pisoc_pts for each point
!
      do ipts = 1,npts
         if(use_pts(ipts)) then
            found = .false.
            do ix = 1,nx-1
                x = lon(ix)
                if((lon_pts(ipts).ge.x).and.(lon_pts(ipts).le.(x+dlon))) then
                    ipt = ix
                    s = (lon_pts(ipts)-x)/dlon
                    s = 2.0_rp*s - 1.0_rp         ! (-1,1)
                    found = .true.
                end if
            end do
            if(.not.found) call runend('get_pts_st: longitude value not found')
!
            found = .false.
            do iy = 1,ny-1
               y = lat(iy)
               if((lat_pts(ipts).ge.y).and.(lat_pts(ipts).le.(y+dlat))) then
                   jpt = iy
                   t = (lat_pts(ipts)-y)/dlat
                   t = 2.0_rp*t - 1.0_rp         ! (-1,1)
                   found = .true.
               end if
            end do
            if(.not.found) call runend('get_pts_st: latitude value not found')
!
!***        Interpolates results
!
            shape(1) = (1.0_rp-t-s+s*t)*0.25_rp                   !  4      3
            shape(2) = (1.0_rp-t+s-s*t)*0.25_rp                   !
            shape(3) = (1.0_rp+t+s+s*t)*0.25_rp                   !      
            shape(4) = (1.0_rp+t-s-s*t)*0.25_rp                   !  1      2
!
            do iload = 1,nload
               if(pp_load) then
                 pload_pts(ipts,iload) =  shape(1)*pload(ipt  ,jpt  ,iload) + &
                                          shape(2)*pload(ipt+1,jpt  ,iload) + &
                                          shape(3)*pload(ipt+1,jpt+1,iload) + & 
                                          shape(4)*pload(ipt  ,jpt+1,iload)
               else  
                 pload_pts(ipts,iload) = -1
               end if
               if(pp_isoc) then
                 pisoc_pts(ipts,iload) =  shape(1)*pisoc(ipt  ,jpt  ,iload) + &
                                          shape(2)*pisoc(ipt+1,jpt  ,iload) + &
                                          shape(3)*pisoc(ipt+1,jpt+1,iload) + & 
                                          shape(4)*pisoc(ipt  ,jpt+1,iload)
                 pisoc_pts(ipts,iload) = max(pisoc_pts(ipts,iload),0.)
               else
                 pisoc_pts(ipts,iload) = -1
               end if
            end do
!
            do ifl = 1,nfl
               if(pp_fl050) then
                 pFL050_pts(ipts,ifl) =  shape(1)*pFL050(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL050(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL050(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL050(ipt  ,jpt+1,ifl)
               else
                 pFL050_pts(ipts,ifl) = -1
               end if
!
               if(pp_fl100) then
                 pFL100_pts(ipts,ifl) =  shape(1)*pFL100(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL100(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL100(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL100(ipt  ,jpt+1,ifl)
               else
                 pFL100_pts(ipts,ifl) = -1
               end if
!
               if(pp_fl150) then
                 pFL150_pts(ipts,ifl) =  shape(1)*pFL150(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL150(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL150(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL150(ipt  ,jpt+1,ifl)
               else
                 pFL150_pts(ipts,ifl) = -1
               end if
!
               if(pp_fl200) then
                 pFL200_pts(ipts,ifl) =  shape(1)*pFL200(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL200(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL200(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL200(ipt  ,jpt+1,ifl)
               else
                 pFL200_pts(ipts,ifl) = -1
               end if
!
               if(pp_fl250) then
                 pFL250_pts(ipts,ifl) =  shape(1)*pFL250(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL250(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL250(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL250(ipt  ,jpt+1,ifl)
               else
                 pFL250_pts(ipts,ifl) = -1
               end if
!
               if(pp_fl300) then
                 pFL300_pts(ipts,ifl) =  shape(1)*pFL300(ipt  ,jpt  ,ifl) + &
                                         shape(2)*pFL300(ipt+1,jpt  ,ifl) + &
                                         shape(3)*pFL300(ipt+1,jpt+1,ifl) + & 
                                         shape(4)*pFL300(ipt  ,jpt+1,ifl)
               else
                 pFL300_pts(ipts,ifl) = -1
               end if
!                
            end do
!
         end if
      end do                                     
!
!***  Writes the file
!
      string1 = 'location        longitude latitude  distance'
      string2 = '                   (o)       (o)      (km)  '
      string3 = '--------------------------------------------'
!
      do iload=1,nload
         string1=TRIM(string1)//' probab '
         string2=TRIM(string2)//'    (%)  '
         string3=TRIM(string3)//'--------'
      end do   
      do iload=1,nload
         string1=TRIM(string1)//'   time '
         string2=TRIM(string2)//'     (h) '
         string3=TRIM(string3)//'--------'
      end do   
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL050 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do   
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL100 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL150 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL200 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL250 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do
      do ifl=1,nfl
         string1=TRIM(string1)//'   FL300 '
         string2=TRIM(string2)//'     (%) '
         string3=TRIM(string3)//'--------'
      end do   
            
      open (99,file=TRIM(fptsout),status='unknown')                
      write(99,10) TRIM(string1),TRIM(string2),TRIM(string3)
 10   format(3(/,a))
!
      do ipts = 1,npts
         if(use_pts(ipts)) then
           write(99,11) nam_pts(ipts),lon_pts(ipts),lat_pts(ipts),dis_pts(ipts)/1d3, &
                        (pload_pts(ipts,iload),iload=1,nload),(pisoc_pts(ipts,iload),iload=1,nload), &
                        (pFL050_pts(ipts,ifl),ifl=1,nfl), &
                        (pFL100_pts(ipts,ifl),ifl=1,nfl), &
                        (pFL150_pts(ipts,ifl),ifl=1,nfl), &
                        (pFL200_pts(ipts,ifl),ifl=1,nfl), &
                        (pFL250_pts(ipts,ifl),ifl=1,nfl), &
                        (pFL300_pts(ipts,ifl),ifl=1,nfl)
 11        format(a15,1x,f7.2,2x,f7.2,5x,f5.0,2x,80(f5.0,3x))
         end if
      end do
      close(99)
!
      return
      end subroutine wripts
!
!
!
      subroutine order_pts(lon_pts,lat_pts,dis_pts,nam_pts,npts)
!******************************************************************************
!*
!*    Orders the points by distance
!*
!******************************************************************************
      use KindType
      implicit none
      integer(ip)           :: npts
      real(rp)              :: lon_pts(npts),lat_pts(npts),dis_pts(npts)
      character(len=s_name) :: nam_pts(npts)
!
      logical     :: found
      integer(ip) :: ipts,jpts
      real(rp)    :: dmax
      real(rp)             , allocatable :: wlon_pts(:),wlat_pts(:),wdis_pts(:)
      character(len=s_name), allocatable :: wnam_pts(:)
!
!***  Allocates memory
!
      allocate(wlon_pts(npts))
      allocate(wlat_pts(npts))            
      allocate(wdis_pts(npts))      
      allocate(wnam_pts(npts))      
!
      do ipts=1,npts               
         dmax = maxval(dis_pts(1:npts))
         jpts = 0
         found = .false.
         do while(.not.found)
            jpts = jpts + 1 
            if(dis_pts(jpts).eq.dmax) then
               wdis_pts(npts-ipts+1) = dis_pts(jpts) 
               wlon_pts(npts-ipts+1) = lon_pts(jpts)
               wlat_pts(npts-ipts+1) = lat_pts(jpts)               
               wnam_pts(npts-ipts+1) = nam_pts(jpts)
!
               found = .true.
               dis_pts(jpts) = -1
            end if
         end do
      end do
!
      dis_pts(1:npts) = wdis_pts(1:npts) 
      lon_pts(1:npts) = wlon_pts(1:npts)
      lat_pts(1:npts) = wlat_pts(1:npts)               
      nam_pts(1:npts) = wnam_pts(1:npts)
!
      return
      end              