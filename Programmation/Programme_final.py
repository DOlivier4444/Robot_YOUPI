

#===============================================================================================#
#																								#
#										Robot youpi	- Olivier DANIEL							#
#																								#
#										0) DEFINITION DES VARIABLES								#
#																								#
#===============================================================================================#


# 0.1) chargement des modules

import curses
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


# 0.3) création d'un byte envoyé au robot pour le contrôler

#Utilisation de LEDBoard afin d'envoyer simultanément plusieurs signaux à différents GPIO du RPI, --> https://gpiozero.readthedocs.io/en/stable/recipes.html#ledboard
#byte =         ["bit7",  "bit6",  "bit5",  "bit4",  "bit3",  "bit2",  "bit1",  "bit0"]
byte = LEDBoard("GPIO18","GPIO23","GPIO24","GPIO25","GPIO12","GPIO16","GPIO20","GPIO21")


# 0.4) Définition des menues

def menu_principal(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "|===================================================================|")
    stdscr.addstr(1, 0, "|                        MENU PRINCIPAL                             |")
    stdscr.addstr(2, 0, "|                                                                   |")
    stdscr.addstr(3, 0, "|   Avec les touches Fn, choisir le menu souhaité :                 |")
    stdscr.addstr(4, 0, "|   F1 : Mode manuel et prise de la position initial                |")
    stdscr.addstr(5, 0, "|   F2 : Choix du programme                                         |")
    stdscr.addstr(6, 0, "|                                                                   |")
    stdscr.addstr(7, 0, "|   Q : quitter le programme                                        |")
    stdscr.addstr(8, 0, "|===================================================================|")
    stdscr.refresh()

def menu_choix_programme(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "|===================================================================|")
    stdscr.addstr(1, 0, "|                       CHOIX DU PROGRAMME                          |")
    stdscr.addstr(2, 0, "|                                                                   |")
    stdscr.addstr(3, 0, "|   Avoir fait la position initial avant d'executer un programme !  |")
    stdscr.addstr(4, 0, "|                                                                   |")
    stdscr.addstr(5, 0, "|   Avec les touches Fx, choisir le programme à executer :          |")
    stdscr.addstr(6, 0, "|   F1 : Test des moteurs (veuillez être en position initiale)      |")
    stdscr.addstr(7, 0, "|   F2 : let's dance ! (non_programmé)                              |")
    stdscr.addstr(8, 0, "|                                                                   |")
    stdscr.addstr(9, 0, "|   ESCAPE : Retour au menu précédent                               |")
    stdscr.addstr(10, 0, "|===================================================================|")
    stdscr.refresh()

def menu_mode_manuel(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "|===================================================================|")
    stdscr.addstr(1, 0, "|                           MODE MANUEL                             |")
    stdscr.addstr(2, 0, "|                                                                   |")
    stdscr.addstr(3, 0, "|     F9 (Négatif) et F12 (Positif) servent à contrôler Le sens     |")
    stdscr.addstr(4, 0, "|    de rotation, Les touches F1 à F6 correspondent aux moteurs.    |")
    stdscr.addstr(5, 0, "|                                                                   |")
    stdscr.addstr(6, 0, "|      REMISE EN POSITION INITIAL : La touche ENTREE effectue       |")
    stdscr.addstr(7, 0, "|     un RAZ de la valeur du codeur du dernier moteur utilisé.      |")
    stdscr.addstr(8, 0, "|                                                                   |")
    stdscr.addstr(9, 0, "|       MAJ gauche, CAPS LOCK et TAB servent respectivement à       |")
    stdscr.addstr(10, 0, "|    regler la petite, moyenne et grande vitesse du mode manuel.    |")
    stdscr.addstr(11, 0, "|                                                                   |")
    stdscr.addstr(11, 0, "|                                                                   |")
    stdscr.addstr(12, 0, "|  /!\Barre espace pour l'arrêt d'urgence(pas encore programmé)/!\  |")
    stdscr.addstr(13, 0, "|                                                                   |")
    stdscr.addstr(11, 0, "|                                                                   |")
    stdscr.addstr(14, 0, "|   F1 : base           | Valeur du codeur : {}                      |".format(Codeur_moteur1))
    stdscr.addstr(15, 0, "|   F2 : epaule         | Valeur du codeur : {}                      |".format(Codeur_moteur2))
    stdscr.addstr(16, 0, "|   F3 : coude          | Valeur du codeur : {}                      |".format(Codeur_moteur3))
    stdscr.addstr(17, 0, "|   F4 : poignet        | Valeur du codeur : {}                      |".format(Codeur_moteur4))
    stdscr.addstr(18, 0, "|   F5 : rotation main  | Valeur du codeur : {}                      |".format(Codeur_moteur5))
    stdscr.addstr(19, 0, "|   F6 : pince          | Valeur du codeur : {}                      |".format(Codeur_moteur6))
    stdscr.addstr(20, 0, "|                                                                   |")
    stdscr.addstr(21, 0, "|   ESCAPE : Retour au menu précédent                               |")
    stdscr.addstr(22, 0, "|===================================================================|")
    stdscr.refresh()


# 0.5) Définitions des sens de rotations et des moteurs

def sens_rotation_0() :
	global sens_rotation
	sens_rotation = 0
	byte.value = (1,0,0,0,0,0,0,0) #0 normal - envoie du signal de sens de rotation
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,0,0) #0 normal - confirmation du signal de sens de rotation
	sleep(0.0005)

def sens_rotation_1() :
	global sens_rotation
	sens_rotation = 1
	byte.value = (1,0,1,1,1,1,1,1) #1 inverse - envoie du signal de sens de rotation
	sleep(0.0005)
	byte.value = (0,0,1,1,1,1,1,1) #1 inverse - confirmation du signal de sens de rotation
	sleep(0.0005)


# 0.6) Définitions des moteurs

def moteur_1() :
	global moteurX, Codeur_moteur1, sens_rotation
	moteurX = 1
	byte.value = (0,1,0,0,0,0,0,0)  #ordre de rotation du moteur 1
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,0,0)  #confirmation de rotation du moteur 1
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur1 += 1
	if sens_rotation == 1:
		Codeur_moteur1 -= 1

def moteur_2() :
	global moteurX, Codeur_moteur2, sens_rotation
	moteurX = 2
	byte.value = (0,1,0,0,0,0,0,1)  #ordre de rotation du moteur 2
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,0,1)  #confirmation de rotation du moteur 2
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur2 += 1
	if sens_rotation == 1:
		Codeur_moteur2 -= 1

def moteur_3() :
	global moteurX, Codeur_moteur3, sens_rotation
	moteurX = 3
	byte.value = (0,1,0,0,0,0,1,0)  #ordre de rotation du moteur 3
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,1,0)  #confirmation de rotation du moteur 3
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur3 += 1
	if sens_rotation == 1:
		Codeur_moteur3 -= 1

def moteur_4() :
	global moteurX, Codeur_moteur4, sens_rotation
	moteurX = 4
	byte.value = (0,1,0,0,0,0,1,1)  #ordre de rotation du moteur 4
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,1,1)  #confirmation de rotation du moteur 4
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur4 += 1
	if sens_rotation == 1:
		Codeur_moteur4 -= 1

def moteur_5() :
	global moteurX, Codeur_moteur5, sens_rotation
	moteurX = 5
	byte.value = (0,1,0,0,0,1,0,0)  #ordre de rotation du moteur 5
	sleep(0.0005)
	byte.value = (0,0,0,0,0,1,0,0)  #confirmation de rotation du moteur 5
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur5 += 1
	if sens_rotation == 1:
		Codeur_moteur5 -= 1

def moteur_6() :
	global moteurX, Codeur_moteur6, sens_rotation
	moteurX = 6
	byte.value = (0,1,0,0,0,1,0,1)  #ordre de rotation du moteur 6
	sleep(0.0005)
	byte.value = (0,0,0,0,0,1,0,1)  #confirmation de rotation du moteur 6
	sleep(0.0005)
	if sens_rotation == 0:
		Codeur_moteur6 += 1
	if sens_rotation == 1:
		Codeur_moteur6 -= 1


# 0.7) Variables

Menu = 1
Menu_affiché = 0
Mode_manuel = 0
Test_moteurs = 0
Dance_robot = 0
Choix_dance = 0

Codeur_moteur1 = 0
Codeur_moteur2 = 0
Codeur_moteur3 = 0
Codeur_moteur4 = 0
Codeur_moteur5 = 0
Codeur_moteur6 = 0
moteurX = 0
sens_rotation = 0


#def variables() :
#	Menu
#	Menu_affiché
#	Mode_manuel
#	Test_moteurs
#	Dance_robot
#	Choix_dance
#
#	Codeur_moteur1
#	Codeur_moteur2
#	Codeur_moteur3
#	Codeur_moteur4
#	Codeur_moteur5
#	Codeur_moteur6
#	moteurX
#	sens_rotation
    
#===============================================================================================================================================================#
#																																								#
#																		Robot youpi	- Olivier DANIEL															#
#																																								#
#																		PROGRAMME PRINCIPAL																		#
#																																								#
#===============================================================================================================================================================#


# Signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01000111 suivi de 16#0---> Voir "Documentation général.pdf"

byte.value = (0,1,0,0,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(0.2)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(0.2)

#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#																				#
#								1) GESTION DES MENUES ET PROGRAMMES				#
#																				#
#===============================================================================#


def main(stdscr): # ---> le fait que ça soit définit ralentis peut-être le programme ?
	curses.curs_set(0)                  # cache le curseur
	stdscr.nodelay(True)                # éntrées non blocantes
	stdscr.timeout(100)                 # Timeout de 100ms pour getch()
#	global variables
	global Mode_manuel, Test_moteurs, Menu, Codeur_moteur1, Codeur_moteur2, Codeur_moteur3, Codeur_moteur4, Codeur_moteur5, Codeur_moteur6, moteurX, sens_rotation, Menu_affiché, Dance_robot, Choix_dance
	stdscr.clear()
	key = stdscr.getch()

	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !

		if Menu == 1:
			key = stdscr.getch()			# Capturer la touche appuyée
			if key == ord('q') or key == ord('Q'):
				break
			elif Menu_affiché == 0:
				menu_principal(stdscr)
				stdscr.refresh()
				Menu_affiché = 1

			elif key == curses.KEY_F1:		# Mode manuel
				Mode_manuel = 1
				Menu_affiché = 0
				Menu = 0
			elif key == curses.KEY_F2:		# Choix du programme
				Menu_affiché = 0
				Menu = 2

		elif Menu == 2:
			key = stdscr.getch()
			if key == 27:					# ESCAPE - retour au menu principal
				Menu_affiché = 0
				Menu = 1
			elif Menu_affiché == 0:
				menu_choix_programme(stdscr)
				stdscr.refresh()
				Menu_affiché = 1


			elif key == curses.KEY_F1:		#Test des moteurs
				Test_moteurs = 1
				Menu_affiché = 0
				Menu = 0
			elif key == curses.KEY_F2:		# Dance des robot
				Dance_robot = 1
				Menu_affiché = 0
				Menu = 0


#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#																				#
#								2) CONTROLE MANUEL								#
#																				#
#===============================================================================#


		while Mode_manuel == 1:               #--> remplacer par if pour que l'ATU fonctionne ?
			vitesse_manu = 200
			stdscr.refresh()
			menu_mode_manuel(stdscr)
			key = stdscr.getch()

			if key == 27:  # Touche ESC
				Menu = 1
				Mode_manuel = 0

			elif key == 10:	#Touche ENTER
				globals()[f'Codeur_moteur{moteurX}'] = 0
				print(moteurX)

			elif key == curses.KEY_F12:
				sens_rotation_0()
			elif key == curses.KEY_F9:
				sens_rotation_1()

			elif key == curses.KEY_F1:
				moteur_1()
			elif key == curses.KEY_F2:
				moteur_2()

		#	while key == curses.KEY_F2:
		#		for f2 in range (200):
		#			moteur_2()
		#			key = stdscr.getch()  # Vérifie si la touche est toujours enfoncée

		#	elif key == curses.KEY_F2:
		#		for f2 in range (vitesse_manu):
		#			moteur_2()
		#			key = stdscr.getch() # Vérifie si la touche est toujours enfoncée
		#	#		if key != curses.KEY_F2:
		#	#			f2 = vitesse_manu

			elif key == curses.KEY_F3:
				moteur_3()
			elif key == curses.KEY_F4:
				moteur_4()
			elif key == curses.KEY_F5:
				moteur_5()
			elif key == curses.KEY_F6:
				moteur_6()


					#curses.wrapper(main)


#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#																				#
#								3) TEST DES MOTEURS								#
#																				#
#===============================================================================#


		while Test_moteurs == 1:
			Nombre_de_pas_rotation_moteur = 400 # 200 pas = 1 tour moteur
			stdscr.clear()
			for i in range(1, 7):
				Pos_txt = ((i-1)/(6/18)) # Droite affine pour la position des textes
				Pos_txt = int(Pos_txt)

				stdscr.addstr(Pos_txt, 0, "Test de rotation du moteur {} : ".format(i))
				stdscr.refresh()
				sleep(1)
				for Boucle in range(2):
					if Boucle == 0:
						stdscr.addstr(Pos_txt + 1, 0, "- Sens de rotation 0 :")
						stdscr.refresh()
						sens_rotation_0()
					else:
						stdscr.addstr(Pos_txt + 1, 0, "- Sens de rotation 1 :")
						stdscr.refresh()
						sens_rotation_1()
					stdscr.addstr(Pos_txt + 2, 0, " ")
					stdscr.refresh()

					for rotation in range (Nombre_de_pas_rotation_moteur) :
						globals()[f'moteur_{i}']()  # appel de la fonction moteur() en fonction de i
					stdscr.refresh()
					sleep(1)
			stdscr.addstr(Pos_txt + 4, 0, "fin du test des moteurs, retour au menu précédent...")
			stdscr.refresh()
			sleep(3)
			Menu = 2
			Test_moteurs = 0


#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#																				#
#								Dance du robot									#
#																				#
#===============================================================================#


		while Dance_robot == 1:
			stdscr.clear()
			stdscr.addstr(2, 0,  "Pas encore programmé, retour au menu précédent...\n") # --
			stdscr.refresh()
			sleep(2)
			Menu = 2
			Dance_robot = 0
			Menu_affiché = 0
			

#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#																				#
#								Système d'arrêt d'urgence						#
#																				#
#===============================================================================#


#	while key == 32:
#		Mode_manuel = 0
#		Test_moteurs = 0
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
