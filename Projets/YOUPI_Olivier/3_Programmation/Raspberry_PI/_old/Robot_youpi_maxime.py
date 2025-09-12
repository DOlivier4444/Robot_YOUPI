

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            0) DEFINITION DES VARIABLES                        #
#                                                                               #
#===============================================================================#


# 0.1) chargement des modules

import curses
from enum import Enum
#import threading --> Utilisable plus tard ?
from gpiozero import LEDBoard                               # type: ignore (ignorer l'"erreur" dans vscode)
import pygame                                               # type: ignore
from pygame.locals import *                                 # type: ignore
from time import sleep


# 0.2) Création des E/S - VARIABLES - CONSTANTES

LEDBoard("GPIO18") # bit7 = Validation_sens_rotation = D7 
LEDBoard("GPIO23") # bit6 = Validation_pas_moteur    = D6 
LEDBoard("GPIO24") # bit5 = moteur6__pince           = D5 = .....,1,0,1
LEDBoard("GPIO25") # bit4 = moteur5__rotation_main   = D4 = .....,1,0,0
LEDBoard("GPIO12") # bit3 = moteur4__poignet         = D3 = .....,0,1,1
LEDBoard("GPIO16") # bit2 = moteur3__coude           = D2 = .....,0,1,0
LEDBoard("GPIO20") # bit1 = moteur2__epaule          = D1 = .....,0,0,1
LEDBoard("GPIO21") # bit0 = moteur1__base            = D0 = .....,0,0,0

class rotation(Enum):
	BACKWARDS = 0
	FORWARD = 1

class motor(Enum):
    MOTOR_1 = 0
    MOTOR_2 = 1
    MOTOR_3 = 2
    MOTOR_4 = 3
    MOTOR_5 = 4
    MOTOR_6 = 5

# 0.3) création d'un byte envoyé au robot pour le contrôler

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


# 0.5) Définitions des sens de rotations et des moteurs

def sens_rotation(rotations:list[rotation]):
	byte.value = tuple([1,0] + rotations[::-1]) # envoie du signal de sens de rotation
	byte.value = tuple([0,0] + rotations[::-1]) # confirmation du signal de sens de rotation


# 0.6) Définitions des moteurs

def step_moteur(motor_id:motor):
	bin_id = bin(motor_id)[::-1]
	bit_1 = (bin_id & (1 << 0)) >> 0
	bit_2 = (bin_id & (1 << 1)) >> 1
	bit_3 = (bin_id & (1 << 2)) >> 2
	byte.value = (0,1,0,0,0,bit_1, bit_2, bit_3)  #ordre de rotation du moteur
	byte.value = (0,0,0,0,0,bit_1, bit_2, bit_3)  #confirmation de rotation du moteur


def validate_move(Codeurs_moteurs:list[int], rotations:list[int], motor_id:motor) -> bool:
	match motor_id:
		case motor.MOTOR_1 :
			return True
		case motor.MOTOR_2 :
			return (
				rotations[motor_id] == rotation.FORWARD 
				and (Codeurs_moteurs[motor.MOTOR_2] <= 4500-1)
				and (Codeurs_moteurs[motor.MOTOR_2] + Codeurs_moteurs[motor.MOTOR_3] <= 3200-1)
			) or (
				rotations[motor_id] == rotation.BACKWARDS 
				and (Codeurs_moteurs[motor.MOTOR_2] >= -2400+1)
				and (Codeurs_moteurs[motor.MOTOR_2] + Codeurs_moteurs[motor.MOTOR_3] >= -4500+1)
			)

# a finir, voir en dessous

	# if (sens_rotation == 1) and ((Codeur_moteur2 + Codeur_moteur3) <= 3200-1) and ((Codeur_moteur4 + Codeur_moteur3) <= 3200-1): #Sécurité anti-collision
	# 	rotation_moteur_3()
	# 	Codeur_moteur3 += 1
	# elif (sens_rotation == 0) and ((Codeur_moteur2 + Codeur_moteur3) >= -4400+1) and ((Codeur_moteur4 + Codeur_moteur3) >= -3200+1):
	# 	rotation_moteur_3()
	# 	Codeur_moteur3 -= 1
	# global sens_rotation, Codeur_moteur4, Codeur_moteur3
	# if (sens_rotation == 1) and ((Codeur_moteur4 + Codeur_moteur3) <= 3200-1):
	# 	rotation_moteur_4()
	# 	Codeur_moteur4 += 1
	# if (sens_rotation == 0) and ((Codeur_moteur4 + Codeur_moteur3) >= -3200+1):
	# 	rotation_moteur_4()
	# 	Codeur_moteur4 -= 1
	# if sens_rotation == 1:
	# 	rotation_moteur_5()
	# 	Codeur_moteur5 += 1
	# if sens_rotation == 0:
	# 	rotation_moteur_5()
	# 	Codeur_moteur5 -= 1
	# if (sens_rotation == 1) and (Codeur_moteur6 <= 0):
	# 	rotation_moteur_6()
	# 	Codeur_moteur6 += 1
	# if (sens_rotation == 0) and (Codeur_moteur6 >= -6000):
	# 	rotation_moteur_6()
	# 	Codeur_moteur6 -= 1

# 0.7) Variables

Menu = 1
Menu_affiché = False
Mode_manuel = False
Test_moteurs = False
Dance_robot = False
Choix_dance = 0

moteurX = 0
Codeur_moteur = [0] * 6
Rotations = [rotation.FORWARD] * 6
vitesse_manu = 1

# 0.4) Définition des menues

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

def menu_mode_manuel(codeur_moteurs:list[int], rotations:list[rotation], vitesse_manu:int):
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
    print("|   Vitesse : {6d}                                                    |".format(vitesse_manu))
    print("|                                                                   |")
    print("|  /!\Barre espace pour l'arrêt d'urgence(pas encore programmé)/!\  |")
    print("|                                                                   |")
    print("|                                                                   |")
    print("|   1 : base           | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_1]),rotations[motor.MOTOR_1])
    print("|   2 : epaule         | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_2]),rotations[motor.MOTOR_2])
    print("|   3 : coude          | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_3]),rotations[motor.MOTOR_3])
    print("|   4 : poignet        | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_4]),rotations[motor.MOTOR_4])
    print("|   5 : rotation main  | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_5]),rotations[motor.MOTOR_5])
    print("|   6 : pince          | Valeur du codeur : {6d}  | Rotation {1d} |".format(codeur_moteurs[motor.MOTOR_6]),rotations[motor.MOTOR_6])
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
	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !
		if Menu == 1:
			menu_principal()
			key = input() # Capturer la touche appuyée
			match key:
				case 81 | 113: # Q ou q - arrêt du programme
					break
				case 49: # 1 - Mode manuel
					Mode_manuel = True
					Menu_affiché = False
					Menu = 0
				case 50: # 2 - Choix du programme
					Menu_affiché = False
					Menu = 2

		elif Menu == 2:
			menu_choix_programme()
			key = input()
			match key:
				case 27: # ESCAPE - retour au menu principal
					Menu = 1
				case 49: # 1 - Test des moteurs
					Test_moteurs = True
					Menu = 0
				case 50: # 2 - Dance des robot
					Dance_robot = True
					Menu = 0


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            2) CONTROLE MANUEL                                 #
#                                                                               #
#===============================================================================#


		while Mode_manuel == True:               #--> remplacer par if pour que l'ATU fonctionne ?
			menu_mode_manuel()
			if 100000 <= vitesse_manu <=0: #Empèchement d'une vitesse négative ou trop importante
				vitesse_manu =1
			key = input()
			#0 == 48
			#1 == 49
			#....
			#p == 112
			#n == 110
			match key:
				case 27:  # Touche ESC
					Menu = 1
					Mode_manuel = False
			#elif key == 48: #Chiffre 0
			#	vitesse_manu = input()

				case 10:	#Touche ENTER
					globals()[f'Codeur_moteur{moteurX}'] = 0
					
				case 112: # sens positif
					sens_rotation(rotations=[1,1,1,1,1,1])
				case 110: # sens négatif
					sens_rotation(rotations=[0,0,0,0,0,0])

				case 49: # 1
					for f1 in range (vitesse_manu):
						
				case 50: # 2
					for f2 in range (vitesse_manu):
						moteur_2()
				case 51: # 3
					for f3 in range (vitesse_manu):
						moteur_3()
				case 52: # 4
					for f4 in range (vitesse_manu):
						moteur_4()
				case 53: # 5
					for f5 in range (vitesse_manu):
						moteur_5()
				case 54: # 6
					for f6 in range (vitesse_manu):
						moteur_6()
	
				case 55: # 7
					vitesse_manu = 1      # vitesse basse
				case 56: # 8
					vitesse_manu = 200      # vitesse moyenne
				case 57: # 9
					vitesse_manu = 400      # vitesse haute
				case 48: # 0
					vitesse_manu = 800      # vitesse maximal (pour le moment)



			#elif key == curses.KEY_F2:
			#	for f2 in range (vitesse_manu):
			#		moteur_2()
			#
			#while key == curses.KEY_F2:
			#	for f2 in range (200):
			#		moteur_2()
			#		key = stdscr.getch()  # Vérifie si la touche est toujours enfoncée
			#
			#elif key == curses.KEY_F2:
			#	for f2 in range (vitesse_manu):
			#		moteur_2()
			#		key = stdscr.getch() # Vérifie si la touche est toujours enfoncée
			#		if key != curses.KEY_F2:
			#			f2 = vitesse_manu

					#curses.wrapper(main)


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            3) TEST DES MOTEURS                                #
#                                                                               #
#===============================================================================#


		while Test_moteurs == True:
			Nombre_de_pas_rotation_moteur = 400 # 200 pas = 1 tour moteur
			clear_screen()
			for i in range(1, 7):
				Pos_txt = int((i-1)/(6/18)) # Droite affine pour la position des textes
				#Pos_txt = int(Pos_txt)

				print(Pos_txt, 0, "Test de rotation du moteur {} : ".format(i))
				sleep(1)
				for Boucle in range(2):
					if Boucle == 0:
						print(Pos_txt + 1, 0, "- Sens de rotation Négatif :")
						sens_rotation(rotations=[1,1,1,1,1,1])
					else:
						print(Pos_txt + 1, 0, "- Sens de rotation Positif :")
						sens_rotation_1()
					print(Pos_txt + 2, 0, " ")

					for rotation in range (Nombre_de_pas_rotation_moteur) :
						globals()[f'moteur_{i}']()  # appel de la fonction moteur() en fonction de i
					sleep(1)
			print(Pos_txt + 4, 0, "fin du test des moteurs, retour au menu précédent...")
			sleep(3)
			Menu = 2
			Test_moteurs = False


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            4) Dance du robot                                  #
#                                                                               #
#===============================================================================#


		while Dance_robot == True:
			stdscr.clear()
			stdscr.addstr(2, 0,  "Programmation en cours, encore en test, début du programme...")
			stdscr.refresh()
			sleep(1)
			for x in range (200):
				sens_rotation_1()
				moteur_2()
				sens_rotation_0
				moteur_3()

				sens_rotation_0()
				moteur_2()
				sens_rotation_1
				moteur_3()
			stdscr.addstr(4, 0,  "Fin du programme, retour au menu précédent")
			sleep(1)
			Menu = 2
			Dance_robot = False
			Menu_affiché = False
			

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            Système d'arrêt d'urgence                          #
#                                                                               #
#===============================================================================#


#	while key == 32:
#		Mode_manuel = False
#		Test_moteurs = False
#		stdscr.clear()
#		stdscr.addstr(2, 0, "ARRET D'URGENCE !")
#		stdscr.addstr(4, 0, "Arret des mouvements...")
#		for b in range (500):
#			byte.value = (0,0,0,0,0,0,0,0)
#		stdscr.addstr(6, 0, "Arret du programme.")
#		stdscr.refresh()
#		sleep(2)
#		break


if __name__ == "__main__":
    curses.wrapper(main)
