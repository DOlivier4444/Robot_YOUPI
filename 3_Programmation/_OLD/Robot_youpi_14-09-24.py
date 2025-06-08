

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            0) DEFINITION DES VARIABLES                        #
#                                                                               #
#===============================================================================#


# 0.1) chargement des modules
from gpiozero import LEDBoard                        # type: ignore
from time import sleep
from enum import Enum


# 0.2) Création d'un byte envoyé au robot pour le contrôler
LEDBoard("GPIO18") #bit8 = Validation_sens_rotation = D7 
LEDBoard("GPIO23") #bit7 = Validation_pas_moteur    = D6 
LEDBoard("GPIO24") #bit6 = moteur6__pince           = D5 = .,.,.,.,.,1,0,1
LEDBoard("GPIO25") #bit5 = moteur5__rotation_main   = D4 = .,.,.,.,.,1,0,0
LEDBoard("GPIO12") #bit4 = moteur4__poignet         = D3 = .,.,.,.,.,0,1,1
LEDBoard("GPIO16") #bit3 = moteur3__coude           = D2 = .,.,.,.,.,0,1,0
LEDBoard("GPIO20") #bit2 = moteur2__epaule          = D1 = .,.,.,.,.,0,0,1
LEDBoard("GPIO21") #bit1 = moteur1__base            = D0 = .,.,.,.,.,0,0,0

#Utilisation de LEDBoard afin d'envoyer simultanément plusieurs signaux à différents GPIO du RPI, --> https://gpiozero.readthedocs.io/en/stable/recipes.html#ledboard
#byte =          (bit8,    bit7,    bit6,    bit5,    bit4,    bit3,    bit2,    bit1)
byte = LEDBoard("GPIO18","GPIO23","GPIO24","GPIO25","GPIO12","GPIO16","GPIO20","GPIO21")

# Signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01000111 suivi de 16#0---> Voir "Documentation général.pdf"
byte.value = (0,1,0,0,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(0.05)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(0.05)



#DH parameters of the Robot Youpi --> https://automaticaddison.com/the-ultimate-guide-to-inverse-kinematics-for-6dof-robot-arms/
#https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters

#Joint i	θi (deg)	αi (deg)	ai/ri (cm)	di (cm)
#1			-90 (+280)	90			0			28
#2			90			180			16.2		0
#3			0			180			16.2		0
#4			90			90			0			0
#5			0			0			0			150 + 0

# 0.3) Définitions des class (rotation, motor)
class rotation(Enum):
	BACKWARDS = 0
	FORWARD = 1

class motor(Enum):
    MOTOR_1_base = 0
    MOTOR_2_shoulder = 1
    MOTOR_3_elbow = 2
    MOTOR_4_wrist_tilt = 3
    MOTOR_5_wrist_rotation = 4
    MOTOR_6_actuator = 5


# 0.6) Définitions des bytes envoyé au moteurs (sens_rotations, validate move et step_motor)
def sens_rotations(rotations:list[int]):
	byte.value = ([1,0,] + [rotations])  #envoie du signal de sens de rotation
	byte.value = ([0,0,] + [rotations])  #confirmation du signal de sens de rotation

def validate_move(Coders_motors:list[int], rotations:list[int], motor_id:motor) -> bool:
	match motor_id:
		case motor.MOTOR_1_base : #base
		# données encore inconnus --> décrassage nécessaire
		#340° de liberté - résolution (mode demi-pas) : 0.03°
		#90° = --
		#--° = 1
		#Pour la sécurité anti collision : une fois le bras en bas, une collision avec la base est possible...
			return True #(
			#	rotations[motor_id] == rotation.FORWARD
			#	and (Coders_motors[motor.MOTOR_1_base] <= +200) #VALEUR MAX DE DEBATTEMENT A TROUVER...
			#) or (
			#	rotations[motor_id] == rotation.BACKWARDS
 			#	and (Coders_motors[motor.MOTOR_1_base] >= -200) #-VALEUR MAX DE DEBATTEMENT
			#)
		case motor.MOTOR_2_shoulder : #épaule
		#6900 pas de débattement - Pour être droit : Se mettre en butée avant puis -4500 pas | 90° par rapport au 0 : +3200 pas
		#90° = +3200
		#0.03° = 1
		#240° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and (Coders_motors[motor.MOTOR_2_shoulder.value] <= 4500)
				and ((Coders_motors[motor.MOTOR_2_shoulder.value] + Coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS 
				and (Coders_motors[motor.MOTOR_2_shoulder.value] >= -2400)
				and ((Coders_motors[motor.MOTOR_2_shoulder.value] + Coders_motors[motor.MOTOR_3_elbow.value]) >= -4500)
			)
		case motor.MOTOR_3_elbow : #coude
		#7700 pas de débattement  - Pour être droit : Se mettre en butée arrière puis -3200 pas
		#90° = +3200
		#0.03° = 1
		#220° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and ((Coders_motors[motor.MOTOR_2_shoulder.value] + Coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt.value] + Coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
			  and ((Coders_motors[motor.MOTOR_2_shoulder.value] + Coders_motors[motor.MOTOR_3_elbow.value]) >= -4400)
			  and ((Coders_motors[motor.MOTOR_4_wrist_tilt.value] + Coders_motors[motor.MOTOR_3_elbow.value]) >= -3200)
			)
		case motor.MOTOR_4_wrist_tilt : #poignet
		#6500 pas de débattement  --> Le 0 pris en position verticale, le débattement se fait de 4000 à -4000 --> pince à 90° partant du 0 : +/-3200 pas
		#90° = +3200
		#0.03° = 1
		#l'axe 5 tourne en même temps (Mécaniquement logique), 
		# ordonner les deux moteurs (4+5 pour garder la pince droite car 1 tour de pince = 6400 pas = une rotation 180° main)
		#220° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt.value] + Coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt.value] + Coders_motors[motor.MOTOR_3_elbow.value]) >= -3200)
			)
		case motor.MOTOR_5_wrist_rotation :#rotation main
		#12800 pas = 360° de la pince - rotation illimité
		#90° = +3200
		#0.03° = 1
		#degré de liberté infini - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
			)
		case motor.MOTOR_6_actuator : #pince
		#6000 pas de débattement
		#90mm = +6000
		#0.015mm = 1
		#Position 0 du codeur : pince fermé
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and (Coders_motors[motor.MOTOR_6_actuator.value] <= 0)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
				and (Coders_motors[motor.MOTOR_6_actuator.value] >= -6000)
			)

def step_motor(motor_id:motor, rotations, Coders_motors, length=3):
	if validate_move(Coders_motors, rotations, motor_id):
		bin_motor = bin(motor_id.value)[2:]  #Convertir en binaire et enlever le "0b"
		bin_motor = bin_motor.zfill(length)  #Compléter avec des zéros pour garantir la longueur désirée
		bin_motor = [int(digit) for digit in bin_motor]  #Convertir en liste d'entiers --> pas forcément optimisé : int --> bin --> list[int]
		byte.value = ([0,1,0,0,0,] + bin_motor)  #envoie du signal de sens de rotation
		sleep(0.002)
		byte.value = ([0,0,0,0,0,] + bin_motor)  #confirme le sens de rotation || #byte.value = (0,0,0,0,0, *bin_motor) aurait pu être utilisé : *bin_motor sers à décompacter la liste [x,x,x] --> x,x,x
		sleep(0.002)
		#sécurité pour ne pas dépasser la vitesse maximale des moteurs --> http://www.alphak.net/news/2009/12/youpi-testons-les-moteurs/
		#T=(1/(40/0.03)/2) = (0.03*2)/40 = 0.0015 --> 0.002 pour le moteur de la base

		match rotations[motor_id.value]:
			case rotation.FORWARD :
				Coders_motors[motor_id.value] += 1
			case rotation.BACKWARDS :
				Coders_motors[motor_id.value] -= 1
			case None:
				print("erreur modification valeur coders")

	else :
		print("mouvement impossible du moteur {} dans la direction {}".format((motor_id.name), rotations[motor_id.value].name))
		print("les valeurs des codeurs sont : {}".format(Coders_motors))


step_motor(motor.MOTOR_1_base, 45, )

# 0.4) Définition des menues
class menus(Enum):
	mode_manuel = 0
	principal = 1
	choix_Programme = 2
	Test_motor = 3
	lets_dance = 4

def menu_principal():
    clear_screen()
    print("|===================================================================|")
    print("|                        MENU PRINCIPAL                             |")
    print("|                                                                   |")
    print("|   Avec les numéros, choisir le menu souhaité :                    |")
    print("|   1 : Mode manuel et prise de la position initial                 |")
    print("|   2 : Choix du programme                                          |")
    print("|                                                                   |")
    print("|   Q : quitter le programme                                        |")
    print("|===================================================================|")

def menu_choix_programme():
    clear_screen()
    print("|===================================================================|")
    print("|                       CHOIX DU PROGRAMME                          |")
    print("|                                                                   |")
    print("|   Avoir fait la position initial avant d'executer un programme !  |")
    print("|                                                                   |")
    print("|   Avec les numéros, choisir le programme à executer :             |")
    print("|   1 : Test des moteurs (veuillez être en position initiale)       |")
    print("|   2 : let's dance ! (non_programmé)                               |")
    print("|                                                                   |")
    print("|   ESCAPE : Retour au menu précédent                               |")
    print("|===================================================================|")

def menu_mode_manuel(Coders_motors:motor, rotations:motor, step_manu:int, speed_manu:float):
    clear_screen()
    print("|===================================================================|")
    print("|                           MODE MANUEL                             |")
    print("|                                                                   |")
    print("|      N (Négatif) et P (Positif) servent à contrôler Le sens       |")
    print("|     de rotation, Les touches 1 à 6 correspondent aux moteurs.     |")
    print("|                                                                   |")
    print("|      REMISE EN POSITION INITIAL : La touche SPACE effectue        |")
    print("|     un RAZ de la valeur du codeur du dernier moteur utilisé.      |")
    print("|                                                                   |")
    print("|          7, 8, 9, 0 servent respectivement à regler la            |")
    print("|  très petite, petite, moyenne et grande vitesse du mode manuel.   |")
    print("|                                                                   |")
    print("|   Distance : {:6d}                                               |".format(step_manu))
    print("|   Vitesse : {:0.3f}                                                    |".format(speed_manu))
    print("|                                                                   |")
    print("|                                                                   |")
    print("|  /!\Barre espace pour l'arrêt d'urgence(pas encore programmé)/!\  |")
    print("|                                                                   |")
    print("|                                                                   |")
    print("|   1 : base              | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_1_base.value], rotations[motor.MOTOR_1_base.value]))
    print("|   2 : epaule            | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_2_shoulder.value],rotations[motor.MOTOR_2_shoulder.value]))
    print("|   3 : coude             | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_3_elbow.value],rotations[motor.MOTOR_3_elbow.value]))
    print("|   4 : poignet           | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_4_wrist_tilt.value],rotations[motor.MOTOR_4_wrist_tilt.value]))
    print("|   5 : rotation main     | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_5_wrist_rotation.value],rotations[motor.MOTOR_5_wrist_rotation.value]))
    print("|   6 : pince             | Valeur du codeur : {:6d} |   {}   |".format(Coders_motors[motor.MOTOR_6_actuator.value],rotations[motor.MOTOR_6_actuator.value]))
    print("|                                                                   |")
    print("|   ESCAPE : Retour au menu précédent                               |")
    print("|===================================================================|")

def clear_screen():
	print(chr(27) + "[2J")


#===============================================================================================================================================================#
#                                                                                                                                                               #
#                                                                       Robot youpi - Olivier DANIEL                                                            #
#                                                                                                                                                               #
#                                                                       PROGRAMME PRINCIPAL                                                                     #
#                                                                                                                                                               #
#===============================================================================================================================================================#

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            1) GESTION DES MENUES ET PROGRAMMES                #
#                                                                               #
#===============================================================================#


def main():
	menu = menus.principal
	step_manu = 0
	speed_manu = 0.000
	last_motor_controlled = None
	rotations = [rotation.FORWARD] *6
	Coders_motors = [0] *6 # Initialisation des codeurs à 0

	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !
		if menu == menus.principal:
			menu_principal()
			try:
				key = input() # Capturer la touche appuyée
				match ord(key):
					case 81 | 113: # Q ou q - arrêt du programme
						break
					case 49: # 1 - Mode manuel
						menu = menus.mode_manuel
					case 50: # 2 - Choix du programme
						menu = menus.choix_Programme

			except (KeyError, Exception) as e:
				print(f"Erreur : {e}")



		elif menu == menus.choix_Programme:
			menu_choix_programme()
			key = input()
			match ord(key):
				case 27: # ESCAPE - retour au menu principal
					menu = menus.principal
				case 49: # 1 - Test des moteurs
					menu = menus.Test_motor
				case 50: # 2 - Dance des robot
					menu = menus.lets_dance


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            2) CONTROLE MANUEL                                 #
#                                                                               #
#===============================================================================#


#--> replace "menu == menus.mode_manuel" with "key != 32" for the emergency stop to work ?
		while menu == menus.mode_manuel:
			menu_mode_manuel(Coders_motors, rotations, step_manu, speed_manu)
			if (0 >= step_manu or step_manu >= 100000): #Prevent a too big or too small step_motor
				step_manu = 0
			if (0 >= speed_manu or speed_manu >= 0.006): #Prevent a too big speed or a negative speed
				speed_manu = 0.000
			try:
				key = input()
				#0 == 48
				#1 == 49...
				#p == 112
				#n == 110
				#+ == 43
				#- == 45

				#speed should be entered manually...
				#elif key == 48: #Chiffre 0
				#	step_manu = input()

				match ord(key):
					case 27: # ESC
						menu = menus.principal
					case 32:	# SPACE - RAZ of the coder of the last motor used (calibration purposes)
						if last_motor_controlled is not None:
							Coders_motors[last_motor_controlled] = 0

					case 112: # sens positif - "p"
						rotations[last_motor_controlled] = rotation.BACKWARDS
						sens_rotations(rotations)
						step_motor()

					case 110: # sens négatif - "n"
						rotations[last_motor_controlled] = rotation.BACKWARDS
						sens_rotations(rotations)
					case 43 : # +
						speed_manu += 0.001
					case 45 : # -
						speed_manu -= 0.001
					case 48: # 0
						step_manu = 0      # vitesse null
					case 55: # 7
						step_manu += 100      # distance 1
					case 56: # 8
						step_manu += 200      # distance 2
					case 57: # 9
						step_manu += 400      # distance 4

					case 49: # 1
						for m1 in range (step_manu):
							step_motor(motor.MOTOR_1_base)
					case 50: # 2
						for m2 in range (step_manu):
							step_motor(motor.MOTOR_2_shoulder)
							sleep(speed_manu)
					case 51: # 3
						for m3 in range (step_manu):
							step_motor(motor.MOTOR_3_elbow)
							sleep(speed_manu)
					case 52: # 4
						for m4 in range (step_manu):
							step_motor(motor.MOTOR_4_wrist_tilt)
							sleep(speed_manu)
					case 53: # 5
						for m5 in range (step_manu):
							step_motor(motor.MOTOR_5_wrist_rotation)
							sleep(speed_manu)
					case 54: # 6
						for m6 in range (step_manu):
							step_motor(motor.MOTOR_6_actuator)
							sleep(speed_manu)

			except (KeyError, Exception) as e:
				print(f"Erreur : {e}")


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            3) TEST DES MOTEURS                                #
#                                                                               #
#===============================================================================#

		while menu == menus.Test_motor:
			numbers_of_steps = 400 # 200 pas = 1 tour moteur
			clear_screen()
			for i in range(0, 6):
				for Boucle in range(2):
					if Boucle == 0:
						print("- Sens de rotation Négatif :")
						rotations[i] = rotation.BACKWARDS
						sens_rotations(rotations)
					else:
						print("- Sens de rotation Positif :")
						rotations[i] == rotation.FORWARD
						sens_rotations(rotations)

					for nbrs_of_steps in range (numbers_of_steps) :
						step_motor(motor(i)) # appel de la fonction moteur() en fonction de i
						clear_screen()
						print("Test de rotation du moteur {} : ".format(i+1))
						if Boucle == 0:
							print("- Sens de rotation Positif :")
							rotations[i] = rotation.FORWARD
						else:
							print("- Sens de rotation Négatif :")
							rotations[i] = rotation.BACKWARDS
						print("La valeur du codeur est de : {}".format(Coders_motors[i]))
						print("le byte envoyé au robot est :{}".format(byte.value))
					sleep(1)

			print("fin du test des moteurs, retour au menu précédent...")
			sleep(3)
			menu = menus.choix_Programme


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            4) Dance du robot                                  #
#                                                                               #
#===============================================================================#


		while menu == menus.lets_dance:
			clear_screen()
			print("Programmation en cours, encore en test, début du programme...")
			sleep(1)
#		for x in range (1):
#			rotations = [rotation.FORWARD, rotation.FORWARD, rotation.BACKWARDS, rotation.FORWARD, rotation.FORWARD, rotation.FORWARD]
			print(rotations)
			rotations=([rotation.FORWARD]*6)
			rotations[last_motor_controlled] = [rotation.BACKWARDS]
#			rotations=([rotation.FORWARD]*3 + [rotation.BACKWARDS]*3)
			sens_rotations(rotations)
			print(rotations)
			step_motor(motor.MOTOR_1_base)
			step_motor(motor.MOTOR_2_shoulder)
			step_motor(motor.MOTOR_3_elbow)
			step_motor(motor.MOTOR_4_wrist_tilt)
			step_motor(motor.MOTOR_5_wrist_rotation)
			step_motor(motor.MOTOR_6_actuator)
#		for x in range (1):
#			rotations = [rotation.BACKWARDS, rotation.BACKWARDS, rotation.FORWARD, rotation.BACKWARDS, rotation.BACKWARDS, rotation.BACKWARDS]
			sens_rotations(rotations = [rotation.BACKWARDS]*3 + [rotation.FORWARD]*3)
			print(rotations)
			step_motor(motor.MOTOR_1_base)
			step_motor(motor.MOTOR_2_shoulder)
			step_motor(motor.MOTOR_3_elbow)
			step_motor(motor.MOTOR_4_wrist_tilt)
			step_motor(motor.MOTOR_5_wrist_rotation)
			step_motor(motor.MOTOR_6_actuator)
			print("Fin du programme, appuyez sur SPACE pour retour au menu précédent")
			key = input()
			if ord(key) == 32: #space
				menu = menus.choix_Programme
			

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            Système d'arrêt d'urgence                          #
#                                                                               #
#===============================================================================#


#	while key == 32:
#		mode_manuel = False
#		Test_moteurs = False
#		clear_screen()
#		print(2, 0, "ARRET D'URGENCE !")
#		print(4, 0, "Arret des mouvements...")
#		for b in range (500):
#			byte.value = (0,0,0,0,0,0,0,0)
#			byte.value = ()
#		print(6, 0, "Arret du programme.")
#		sleep(2)
#		break

if __name__ == "__main__":
	main()