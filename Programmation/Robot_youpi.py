

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
LEDBoard("GPIO18") # bit7 = Validation_sens_rotation = D7 
LEDBoard("GPIO23") # bit6 = Validation_pas_moteur    = D6 
LEDBoard("GPIO24") # bit5 = moteur6__pince           = D5 = .....,1,0,1
LEDBoard("GPIO25") # bit4 = moteur5__rotation_main   = D4 = .....,1,0,0
LEDBoard("GPIO12") # bit3 = moteur4__poignet         = D3 = .....,0,1,1
LEDBoard("GPIO16") # bit2 = moteur3__coude           = D2 = .....,0,1,0
LEDBoard("GPIO20") # bit1 = moteur2__epaule          = D1 = .....,0,0,1
LEDBoard("GPIO21") # bit0 = moteur1__base            = D0 = .....,0,0,0

#Utilisation de LEDBoard afin d'envoyer simultanément plusieurs signaux à différents GPIO du RPI, --> https://gpiozero.readthedocs.io/en/stable/recipes.html#ledboard
#byte =         ["bit7",  "bit6",  "bit5",  "bit4",  "bit3",  "bit2",  "bit1",  "bit0"]
byte = LEDBoard("GPIO18","GPIO23","GPIO24","GPIO25","GPIO12","GPIO16","GPIO20","GPIO21")

# Signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01000111 suivi de 16#0---> Voir "Documentation général.pdf"
byte.value = (0,1,0,0,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(0.05)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(0.05)


# 0.3) Définitions des class (rotation, motor)
class rotation(Enum):
	BACKWARDS = 0
	FORWARD = 1
rotations = [rotation.FORWARD] *6

class motor(Enum):
    MOTOR_1_base = 0
    MOTOR_2_shoulder = 1
    MOTOR_3_elbow = 2
    MOTOR_4_wrist_tilt = 3
    MOTOR_5_wrist_rotation = 4
    MOTOR_6_actuator = 5
last_motor_controlled = motor.MOTOR_1_base
Coders_motors = [0] *6  # Initialisation des codeurs à 0


# 0.6) Définitions des bytes envoyé au moteurs (sens_rotations, validate move et step_motor)
def sens_rotations(rotations):
	byte.value = ([1,0,] + [rotations])  #envoie du signal de sens de rotation
	byte.value = ([0,0,] + [rotations])  #confirmation du signal de sens de rotation
                           #rotations[::-1]?
#sens_rotations(rotations=[rotation.FORWARD, rotation.BACKWARDS,  ])


def validate_move(Coders_motors:list[int], rotations:list[int], motor_id:motor) -> bool:
	match motor_id:
		case motor.MOTOR_1_base : #base
		# données encore inconnus --> décrassage nécessaire
		#340° de liberté - résolution (mode demi-pas) : 0.04°
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
		#240° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id] == rotation.FORWARD 
				and (Coders_motors[motor.MOTOR_2_shoulder] <= 4500)
				and ((Coders_motors[motor.MOTOR_2_shoulder] + Coders_motors[motor.MOTOR_3_elbow]) <= 3200)
			) or (
				rotations[motor_id] == rotation.BACKWARDS 
				and (Coders_motors[motor.MOTOR_2_shoulder] >= -2400)
				and ((Coders_motors[motor.MOTOR_2_shoulder] + Coders_motors[motor.MOTOR_3_elbow]) >= -4500)
			)
		case motor.MOTOR_3_elbow : #coude
		#7700 pas de débattement  - Pour être droit : Se mettre en butée arrière puis -3200 pas
		#220° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id] == rotation.FORWARD
				and ((Coders_motors[motor.MOTOR_2_shoulder] + Coders_motors[motor.MOTOR_3_elbow]) <= 3200)
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt] + Coders_motors[motor.MOTOR_3_elbow]) <= 3200)
			) or (
				rotations[motor_id] == rotation.BACKWARDS
			  and ((Coders_motors[motor.MOTOR_2_shoulder] + Coders_motors[motor.MOTOR_3_elbow]) >= -4400)
			  and ((Coders_motors[motor.MOTOR_4_wrist_tilt] + Coders_motors[motor.MOTOR_3_elbow]) >= -3200)
			)
		case motor.MOTOR_4_wrist_tilt : #poignet
		#6500 pas de débattement (faux ?) --> Le 0 pris en position verticale, le débattement se fait de 4000 à -4000 --> pince à 90° partant du 0 : +/-3200 pas
		#l'axe 5 tourne en même temps (Mécaniquement logique), 
		# ordonner les deux moteurs (4+5 pour garder la pince droite car 6400 pas = 1 tour de pince et 6400 pas = une rotation 180° main)
		#220° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id] == rotation.FORWARD
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt] + Coders_motors[motor.MOTOR_3_elbow]) <= 3200)
			) or (
				rotations[motor_id] == rotation.BACKWARDS
				and ((Coders_motors[motor.MOTOR_4_wrist_tilt] + Coders_motors[motor.MOTOR_3_elbow]) >= -3200)
			)
		case motor.MOTOR_5_wrist_rotation :#rotation main
		#12800 pas = 360° de la pince - rotation illimité
		#degré de liberté infini - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id] == rotation.FORWARD
			) or (
				rotations[motor_id] == rotation.BACKWARDS
			)
		case motor.MOTOR_6_actuator : #pince
		#6000 pas de débattement
		#Position 0 du codeur : pince fermé
			return (
				rotations[motor_id] == rotation.FORWARD
				and (Coders_motors[motor_id] <= 0)
			) or (
				rotations[motor_id] == rotation.BACKWARDS
				and (Coders_motors[motor_id] >= -6000)
			)


def step_motor(motor_id:motor, length=3):
	if validate_move(Coders_motors, rotations, motor_id, last_motor_controlled): #appel de la fonction car elle renvoie 
		bin_motor = bin(motor_id.value)[2:]  #Convertir en binaire et enlever le "0b"
		bin_motor = bin_motor.zfill(length)  #Compléter avec des zéros pour garantir la longueur désirée
		bin_motor = [int(digit) for digit in bin_motor]  #Convertir en liste d'entiers
		byte.value = ([0,1,0,0,0,] + bin_motor)  #envoie du signal de sens de rotation
		byte.value = ([0,0,0,0,0,] + bin_motor)  #confirme le sens de rotation || #byte.value = (0,0,0,0,0, *bin_motor) aurait pu être utilisé : *bin_motor sers à décompacter la liste [x,x,x] --> x,x,x
		last_motor_controlled = motor_id
		
		match rotations[motor_id]:
			case rotation.FORWARD :
				Coders_motors[motor_id.value] =+ 1
			case rotation.BACKWARDS :
				Coders_motors[motor_id.value] =- 1
	else :
		print("mouvement impossible du moteur {} dans la direction {}".format(motor_id), rotations[motor_id])
		print("les valeurs des codeurs sont : [{}]".format(Coders_motors))


# 0.4) Définition des menues
class menus(Enum):
	mode_manuel = 0
	principal = 1
	choix_Programme = 2
	Test_motor = 3
	lets_dance = 4
menu = menus.principal

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

def menu_mode_manuel(Coder_motors:list[int], rotations:list[rotation], speed_manu:int):
    clear_screen()
    print("|===================================================================|")
    print("|                           MODE MANUEL                             |")
    print("|                                                                   |")
    print("|      N (Négatif) et P (Positif) servent à contrôler Le sens       |")
    print("|     de rotation, Les touches 1 à 6 correspondent aux moteurs.     |")
    print("|                                                                   |")
    print("|      REMISE EN POSITION INITIAL : La touche ENTREE effectue       |")
    print("|     un RAZ de la valeur du codeur du dernier moteur utilisé.      |")
    print("|                                                                   |")
    print("|          7, 8, 9, 0 servent respectivement à regler la            |")
    print("|  très petite, petite, moyenne et grande vitesse du mode manuel.   |")
    print("|                                                                   |")
    print("|   Vitesse : {6d}                                                    |".format(speed_manu))
    print("|                                                                   |")
    print("|  /!\Barre espace pour l'arrêt d'urgence(pas encore programmé)/!\  |")
    print("|                                                                   |")
    print("|                                                                   |")
    print("|   1 : base           | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_1_base]),rotations[motor.MOTOR_1_base])
    print("|   2 : epaule         | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_2_shoulder]),rotations[motor.MOTOR_2_shoulder])
    print("|   3 : coude          | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_3_elbow]),rotations[motor.MOTOR_3_elbow])
    print("|   4 : poignet        | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_4_wrist_tilt]),rotations[motor.MOTOR_4_wrist_tilt])
    print("|   5 : rotation main  | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_5_wrist_rotation]),rotations[motor.MOTOR_5_wrist_rotation])
    print("|   6 : pince          | Valeur du codeur : {6d}  | Rotation {1d} |".format(Coder_motors[motor.MOTOR_6_actuator]),rotations[motor.MOTOR_6_actuator])
    print("|                                                                   |")
    print("|   ESCAPE : Retour au menu précédent                               |")
    print("|===================================================================|")

def clear_screen():
	print(chr(27) + "[2J")


# 0.7) Variables
speed_manu = 1


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
	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !
		if menu == menus.principal:
			menu_principal()
			key = input() # Capturer la touche appuyée
			match key:
				case 81 | 113: # Q ou q - arrêt du programme
					break
				case 49: # 1 - Mode manuel
					menu = menus.mode_manuel
				case 50: # 2 - Choix du programme
					menu = menus.choix_Programme

		elif menu == menus.choix_Programme:
			menu_choix_programme()
			key = input()
			match key:
				case 27: # ESCAPE - retour au menu principal
					menu = menus.principal
				case 49: # 1 - Test des moteurs
					menu = menus.mode_manuel
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
			menu_mode_manuel()
			if (100000 <= speed_manu <=0): #Prevent a too big speed or a negative speed
				speed_manu =1
			key = input()
			#0 == 48
			#1 == 49
			#....
			#p == 112
			#n == 110
			match key:
				case 27:  # ESC
					menu = menus.principal
					
			#speed should be entered manually...
			#elif key == 48: #Chiffre 0
			#	speed_manu = input()

				case 10:	# ENTER - RAZ of the coder of the last motor used (calibration purposes)
					Coders_motors[last_motor_controlled] = 0
				case 112: # sens positif - "p"
					rotations[last_motor_controlled] = rotation.FORWARD
				case 110: # sens négatif - "n"
					rotations[last_motor_controlled] = rotation.BACKWARDS

				case 49: # 1
					for m1 in range (speed_manu):
						step_motor(motor.MOTOR_1_base)
				case 50: # 2
					for m2 in range (speed_manu):
						step_motor(motor.MOTOR_2_shoulder)
						if speed_manu == 200:
							speed_manu = 200 #Petit test temporaire...
				case 51: # 3
					for m3 in range (speed_manu):
						step_motor(motor.MOTOR_3_elbow)
				case 52: # 4
					for m4 in range (speed_manu):
						step_motor(motor.MOTOR_4_wrist_tilt)
				case 53: # 5
					for m5 in range (speed_manu):
						step_motor(motor.MOTOR_5_wrist_rotation)
				case 54: # 6
					for m6 in range (speed_manu):
						step_motor(motor.MOTOR_6_actuator)

				case 55: # 7
					speed_manu = 1      # vitesse basse
				case 56: # 8
					speed_manu = 200      # vitesse moyenne
				case 57: # 9
					speed_manu = 400      # vitesse haute
				case 48: # 0
					speed_manu = 800      # vitesse maximal (pour le moment)

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
			for i in range(1, 7):
				Pos_txt = int((i-1)/(6/18)) # Droite affine pour la position des textes
				print(Pos_txt, 0, "Test de rotation du moteur {} : ".format(i))
				sleep(1)
				for Boucle in range(2):
					if Boucle == 0:
						print(Pos_txt + 1, 0, "- Sens de rotation Négatif :")
						rotations[i-1] = rotation.BACKWARDS
					else:
						print(Pos_txt + 1, 0, "- Sens de rotation Positif :")
						rotations[i-1] = rotation.FORWARD
					print(Pos_txt + 2, 0, " ")

					for nbrs_of_steps in range (numbers_of_steps) :
						step_motor(motor(i-1)) # appel de la fonction moteur() en fonction de i
						sleep(1)
			print(Pos_txt + 4, 0, "fin du test des moteurs, retour au menu précédent...")
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
			print(2, 0,  "Programmation en cours, encore en test, début du programme...")
			clear_screen()
			sleep(1)
			for x in range (200):
				rotations[rotation.FORWARD, rotation.FORWARD, rotation.BACKWARDS, rotation.FORWARD, rotation.FORWARD, rotation.FORWARD]
				step_motor(motor.MOTOR_1_base)
				step_motor(motor.MOTOR_2_shoulder)
				step_motor(motor.MOTOR_3_elbow)
				step_motor(motor.MOTOR_4_wrist_tilt)
				step_motor(motor.MOTOR_5_wrist_rotation)
				step_motor(motor.MOTOR_6_actuator)
			for x in range (200):
				rotations[rotation.BACKWARDS, rotation.BACKWARDS, rotation.FORWARD, rotation.BACKWARDS, rotation.BACKWARDS, rotation.BACKWARDS]
				step_motor(motor.MOTOR_1_base)
				step_motor(motor.MOTOR_2_shoulder)
				step_motor(motor.MOTOR_3_elbow)
				step_motor(motor.MOTOR_4_wrist_tilt)
				step_motor(motor.MOTOR_5_wrist_rotation)
				step_motor(motor.MOTOR_6_actuator)
			print(4, 0,  "Fin du programme, retour au menu précédent")
			sleep(1)
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