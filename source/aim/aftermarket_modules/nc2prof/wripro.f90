     subroutine wripro
!****************************************************
!*
!*
!****************************************************
     use Master
     use InpOut
     use TimeFun
     implicit none
!   
     integer(ip) :: ipass
!
!*** Loop over profiles
!
     ipass = 0
     do it = it1,it2
         ipass = ipass + 1
!      
!***     Computes date in format YYYYMMDDHH
!
         call addtime(ibyr,ibmo,ibdy,ibhr,iyr,imo,idy,ihr,imi,ise,(it-1)*6*3600.0_rp)
         date0 = 1d6*iyr + 1d4 *imo + 1d2 *idy + ihr  
         date1 = 1d4*iyr + 1d2 *imo + idy  
!
         luresname = 'ncep1_'
         ilen = LEN_TRIM(luresname)
         write(luresname(ilen+1:ilen+11),'(i10)') INT(date0)        
         luresname = TRIM(luresname)//'.profile'
!
!***    Opens the file
!
        open(90,FILE=TRIM(luresname),status='unknown')
!     
!*** Initial date
!
        write(90,'(a)') '814924 9208168'
        write(90,'(i8)') INT(date1)                      ! YYYYMMDD
        write(90,'(a)') '0 9999999'
        write(90,'(i2)') nz
!
        do iz= 1,nz
           write(90,10) H(iz,ipass),U(iz,ipass),V(iz,ipass),T(iz,ipass)-273.15,umod(iz,ipass),udir(iz,ipass)
 10        format(f8.1,1x,f7.2,1x,f7.2,1x,f7.2,1x,f7.2,1x,f7.2)
	    end do     
!
        close(90)
!
     end do
!
     return
     end subroutine wripro
     
     
    
 
!
