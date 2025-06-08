#===============================================================================================
#
#                                            Robot youpi
#                                            Programme n°2
#
#===============================================================================================

from gpiozero import LEDBoard
from time import sleep

LEDBoard("GPIO18")  #  bit7 = Validation_sens_rotation = D7 
LEDBoard("GPIO23")  #  bit6 = Validation_pas_moteur    = D6 
LEDBoard("GPIO24")  #  bit5 = moteur6__pince           = D5 = .....,1,0,1
LEDBoard("GPIO25")  #  bit4 = moteur5__rotation_main   = D4 = .....,1,0,0
LEDBoard("GPIO12")  #  bit3 = moteur4__poignet         = D3 = .....,0,1,1
LEDBoard("GPIO16")  #  bit2 = moteur3__coude           = D2 = .....,0,1,0
LEDBoard("GPIO20")  #  bit1 = moteur2__epaule          = D1 = .....,0,0,1
LEDBoard("GPIO21")  #  bit0 = moteur1__base            = D0 = .....,0,0,0



#création d'un byte envoyé au robot
#byte =         ["bit7",  "bit6",  "bit5",  "bit4",  "bit3",  "bit2",  "bit1",  "bit0"]
byte = LEDBoard("GPIO18","GPIO23","GPIO24","GPIO25","GPIO12","GPIO16","GPIO20","GPIO21")

#signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01010111 ---> https://gpiozero.readthedocs.io/en/stable/recipes.html#ledboard
byte.value = (0,1,0,1,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(2)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(2)

#signal de sens de rotation
byte.value = (1,0,0,0,0,0,0,0)
print("envoie du signal de sens de rotation")
sleep(2)
byte.value = (0,0,0,0,0,0,0,0)
print("confirmation du signal de sens de rotation")
sleep(2)

#signal de rotation
for rotation in range(400):
	byte.value = (0,1,0,0,0,0,0,1)
	print("ordre de rotation du moteur 2")
sleep(2)

for rotation in range(400):	
    byte.value = (0,0,0,0,0,0,0,1)
    print("confirmation de rotation du moteur 2")
sleep(2)

print("fin du programme")

