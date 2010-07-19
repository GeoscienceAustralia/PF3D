!***************************************************************
!*
!*    Module for kind definition
!* 
!***************************************************************
     MODULE KindType
     implicit none
     save
!
     integer, parameter :: ip = 4
     integer, parameter :: rp = 8 
!
     integer, parameter :: s_grads = 15 ! max string length in GRADS
     integer, parameter :: s_name = 25
     integer, parameter :: s_file = 250
     integer, parameter :: s_mess = 100
!
	 END MODULE KindType