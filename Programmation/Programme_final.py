

#===============================================================================================#
#																								#
#										Robot youpi	- Olivier DANIEL							#
#										Definition des variables								#
#																								#
#===============================================================================================#


# chargement des modules
import threading
import curses
from gpiozero import LEDBoard # type: ignore (ignorer l'"erreur" dans vscode)
import pygame # type: ignore
from pygame.locals import * # type: ignore
from time import sleep


# CREATION DES E/S - VARIABLES - CONSTANTES

# initialisation des sorties
LEDBoard("GPIO18") # bit7 = Validation_sens_rotation = D7 
LEDBoard("GPIO23") # bit6 = Validation_pas_moteur    = D6 
LEDBoard("GPIO24") # bit5 = moteur6__pince           = D5 = .....,1,0,1
LEDBoard("GPIO25") # bit4 = moteur5__rotation_main   = D4 = .....,1,0,0
LEDBoard("GPIO12") # bit3 = moteur4__poignet         = D3 = .....,0,1,1
LEDBoard("GPIO16") # bit2 = moteur3__coude           = D2 = .....,0,1,0
LEDBoard("GPIO20") # bit1 = moteur2__epaule          = D1 = .....,0,0,1
LEDBoard("GPIO21") # bit0 = moteur1__base            = D0 = .....,0,0,0


# création d'un byte envoyé au robot pour le contrôler
#byte =         ["bit7",  "bit6",  "bit5",  "bit4",  "bit3",  "bit2",  "bit1",  "bit0"]
byte = LEDBoard("GPIO18","GPIO23","GPIO24","GPIO25","GPIO12","GPIO16","GPIO20","GPIO21")

def menu_principal(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "|===================================================================|")
    stdscr.addstr(1, 0, "|                        MENU PRINCIPAL                             |")
    stdscr.addstr(2, 0, "|                                                                   |")
    stdscr.addstr(3, 0, "|   Avec le pavé numérique, choisissez le mode de contrôle :        |")
    stdscr.addstr(4, 0, "|   F1 : Mode manuel et mise en position initial                    |")
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
    stdscr.addstr(3, 0, "|   Avec les touches Fx, choisissez le programme à executer :       |")
    stdscr.addstr(4, 0, "|   F1 : Test des moteurs (veuillez être en position initiale)      |")
    stdscr.addstr(5, 0, "|   F2 : let's dance ! (non_programmé)                              |")
    stdscr.addstr(6, 0, "|                                                                   |")
    stdscr.addstr(7, 0, "|   ESCAPE : Retour au menu précédent                               |")
    stdscr.addstr(8, 0, "|===================================================================|")
    stdscr.refresh()

def menu_mode_manuel(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "|===================================================================|")
    stdscr.addstr(1, 0, "|                           MODE MANUEL                             |")
    stdscr.addstr(2, 0, "|                                                                   |")
    stdscr.addstr(3, 0, "|     F9 (Négatif) et F12 (Positif) servent à contrôler Le sens     |")
    stdscr.addstr(4, 0, "|     de rotation, Les touches F1 à F6 correspondent aux moteurs.   |")
    stdscr.addstr(5, 0, "|                                                                   |")
    stdscr.addstr(6, 0, "|  REMISE EN POSITION INITIAL : La touche ENTREE effectue un RAZ    |")
    stdscr.addstr(7, 0, "|         de la valeur du codeur du dernier moteur utilisé,         |")
    stdscr.addstr(8, 0, "|                                                                   |")
    stdscr.addstr(9, 0, "|   /!\ Rien n'arrêtera le robot, veuillez être précautionneux /!\  |")
    stdscr.addstr(10, 0, "|                                                                   |")
    stdscr.addstr(11, 0, "|   F1 : base           | Valeur du codeur : {}                      |".format(Codeur_moteur1))
    stdscr.addstr(12, 0, "|   F2 : epaule         | Valeur du codeur : {}                      |".format(Codeur_moteur2))
    stdscr.addstr(13, 0, "|   F3 : coude          | Valeur du codeur : {}                      |".format(Codeur_moteur3))
    stdscr.addstr(14, 0, "|   F4 : poignet        | Valeur du codeur : {}                      |".format(Codeur_moteur4))
    stdscr.addstr(15, 0, "|   F5 : rotation main  | Valeur du codeur : {}                      |".format(Codeur_moteur5))
    stdscr.addstr(16, 0, "|   F6 : pince          | Valeur du codeur : {}                      |".format(Codeur_moteur6))
    stdscr.addstr(17, 0, "|                                                                   |")
    stdscr.addstr(18, 0, "|   ESCAPE : Retour au menu précédent                               |")
    stdscr.addstr(19, 0, "|===================================================================|")
    stdscr.refresh()


#Sens de rotation inverse et normal
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


#Rotation des moteurs en mode de test manuel :
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


#signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01010111 ---> https://gpiozero.readthedocs.io/en/stable/recipes.html#ledboard
byte.value = (0,1,0,0,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(0.2)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(0.2)


# Variables
Mode_manuel = 0
Test_moteurs = 0
Menu = 1
#Menu_affiché = 0
Codeur_moteur1 = 0
Codeur_moteur2 = 0
Codeur_moteur3 = 0
Codeur_moteur4 = 0
Codeur_moteur5 = 0
Codeur_moteur6 = 0
moteurX = 0
sens_rotation = 0


#===============================================================================================================================================================#
#																																								#
#																		Robot youpi	- Olivier DANIEL															#
#																		Programme Principal																		#
#																																								#
#===============================================================================================================================================================#

#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#								Menu principal									#
#																				#
#===============================================================================#

# MENU PRINCIPAL - Début du programme
def main(stdscr):
	curses.curs_set(0)					# cache le curseur
	stdscr.nodelay(True)				# éntrées non blocantes
	stdscr.timeout(100) 				# Timeout de 100ms pour getch()

	#
	global Mode_manuel, Test_moteurs, Menu, Codeur_moteur1, Codeur_moteur2, Codeur_moteur3, Codeur_moteur4, Codeur_moteur5, Codeur_moteur6, moteurX, sens_rotation		#, Menu_affiché
	key = stdscr.getch()
	stdscr.clear()

	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !

#		if Menu == 1 and Menu_affiché == 0: (test de l'apparition unique du menu)
#			menu_principal()
#			Menu_affiché = 1

		if Menu == 1:
			menu_principal(stdscr)
			stdscr.refresh()
			key = stdscr.getch() 	# Capturer la touche appuyée
			if key == ord('q') or key == ord('Q'):
				break

			elif key == curses.KEY_F1:		# Mode manuel
				Mode_manuel = 1
				Menu = 0

			elif key == curses.KEY_F2:		# Choix du programme
				Menu = 2

		elif Menu == 2:
			stdscr.refresh()
			menu_choix_programme(stdscr)
			key = stdscr.getch()
			if key == curses.KEY_F1:		#Test des moteurs
				stdscr.refresh()
				Test_moteurs = 1
				Menu = 0
			elif key == curses.KEY_F2:		# Dance des robot
				stdscr.clear()
				stdscr.addstr(0, 0,  "Pas encore programmé, retour au menu précédent...\n") #--> \n ?
				stdscr.refresh()
				sleep(2)
			elif key == 27:					# ESCAPE
				Menu = 1



#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#								Contrôle manuel									#
#																				#
#===============================================================================#

# Fonction principale pour le mode manuel
		vitesse_manu = 200
		while Mode_manuel == 1:               #--> remplacer par if pour que l'ATU fonctionne ?
			stdscr.refresh()
			menu_mode_manuel(stdscr)
			key = stdscr.getch()

			if key == 27:  # Touche ESC
				Menu = 1
				Mode_manuel = 0

			elif key == 10:	#Touche ENTER
				globals()[f'Codeur_moteur{moteurX}'] = 0
				print(moteurX)
																	#Pour aider
																	#Codeur_moteur1 = 0
																	#Codeur_moteur2 = 0
																	#Codeur_moteur3 = 0
																	#Codeur_moteur4 = 0
																	#Codeur_moteur5 = 0
																	#Codeur_moteur6 = 0
																	#
																	#moteurX = 0
																	#sens_rotation = 0

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


																													#curses.wrapper(main) --> voir à quoi ça sert



#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#								Test des moteurs								#
#																				#
#===============================================================================#

		while Test_moteurs == 1:
			Nombre_de_pas_rotation_moteur = 400 # 200 pas = 1 tour moteur
			stdscr.clear()
			for i in range(1, 7):
				Pos_txt = ((i-1)/(6/18)) #--> droite affine
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


#===============================================================================#
#																				#
#								Robot youpi	- Olivier DANIEL					#
#								-------------------------						#
#																				#
#===============================================================================#


if __name__ == "__main__":
    curses.wrapper(main)