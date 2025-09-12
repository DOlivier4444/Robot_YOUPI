

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            0) DEFINITION DES VARIABLES                        #
#                                                                               #
#===============================================================================#


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


# 0.7) Variables

Menu = 1
Menu_affiché = False
Mode_manuel = False
Test_moteurs = False
Dance_robot = False
Choix_dance = 0

moteurX = 0
Codeur_moteur1 = 0
Codeur_moteur2 = 0
Codeur_moteur3 = 0
Codeur_moteur4 = 0
Codeur_moteur5 = 0
Codeur_moteur6 = 0

sens_rotation = 1
vitesse_manu = 1
bypass_limitations = False


# Signal RESET afin d'initialiser les phases du moteur --> 16#47 donc 2#01000111 suivi de 16#0---> Voir "Documentation général.pdf"

byte.value = (0,1,0,0,0,1,1,1)
print("initialisation en cours, byte = 47")
sleep(0.05)
byte.value = (0,0,0,0,0,0,0,0)
print("initialisation en cours, byte = 0")
sleep(0.05)


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
    stdscr.addstr(3, 0, "|      N (Négatif) et P (Positif) servent à contrôler Le sens       |")
    stdscr.addstr(4, 0, "|     de rotation, Les touches 1 à 6 correspondent aux moteurs.     |")
    stdscr.addstr(5, 0, "|                                                                   |")
    stdscr.addstr(6, 0, "|      REMISE EN POSITION INITIAL : La touche ENTREE effectue       |")
    stdscr.addstr(7, 0, "|     un RAZ de la valeur du codeur du dernier moteur utilisé.      |")
    stdscr.addstr(8, 0, "|                                                                   |")
    stdscr.addstr(9, 0, "|          7, 8, 9, 0 servent respectivement à regler la            |")
    stdscr.addstr(10, 0, "|  très petite, petite, moyenne et grande vitesse du mode manuel.   |")
    stdscr.addstr(11, 0, "|                                                                   |")
    stdscr.addstr(12, 0, "|   Vitesse : {}                                                    |".format(vitesse_manu))
    stdscr.addstr(13, 0, "|   Sens de rotation : {}                                           |".format(sens_rotation))
    stdscr.addstr(14, 0, "|                                                                   |")
    stdscr.addstr(15, 0, "|          /!\Barre espace pour bypass les limitations/!\           |")
    stdscr.addstr(16, 0, "|                                                                   |")
    stdscr.addstr(17, 0, "|                                                                   |")
    stdscr.addstr(18, 0, "|   1 : base           | Valeur du codeur : {}                       |".format(Codeur_moteur1))
    stdscr.addstr(19, 0, "|   2 : epaule         | Valeur du codeur : {}                       |".format(Codeur_moteur2))
    stdscr.addstr(20, 0, "|   3 : coude          | Valeur du codeur : {}                       |".format(Codeur_moteur3))
    stdscr.addstr(21, 0, "|   4 : poignet        | Valeur du codeur : {}                       |".format(Codeur_moteur4))
    stdscr.addstr(22, 0, "|   5 : rotation main  | Valeur du codeur : {}                       |".format(Codeur_moteur5))
    stdscr.addstr(23, 0, "|   6 : pince          | Valeur du codeur : {}                       |".format(Codeur_moteur6))
    stdscr.addstr(24, 0, "|                                                                   |")
    stdscr.addstr(25, 0, "|   ESCAPE : Retour au menu précédent                               |")
    stdscr.addstr(26, 0, "|===================================================================|")
    stdscr.refresh()


# 0.5) Définitions des sens de rotations et des moteurs

def sens_rotation_0() :  # sens négatif
	global sens_rotation
	sens_rotation = 0
	byte.value = (1,0,0,0,0,0,0,0) #0 Négatif - envoie du signal de sens de rotation
	sleep(0.0005)
	byte.value = (0,0,0,0,0,0,0,0) #0 Négatif - confirmation du signal de sens de rotation
	sleep(0.0005)


def sens_rotation_1() :  # sens Positif
	global sens_rotation
	sens_rotation = 1
	byte.value = (1,0,1,1,1,1,1,1) #1 Positif - envoie du signal de sens de rotation
	sleep(0.0005)
	byte.value = (0,0,1,1,1,1,1,1) #1 Positif - confirmation du signal de sens de rotation
	sleep(0.0005)


# 0.6) Définitions des moteurs

# données encore inconnus --> décrassage nécessaire
#340° de liberté - résolution (mode demi-pas) : 0.04°
def moteur_1() : #base
#	key = stdscr.getch()
#	if key != 32:				#Arrêt d'urgence ?
	def rotation_moteur_1():
		global moteurX
		byte.value = (0,1,0,0,0,0,0,0)  #ordre de rotation du moteur 1
		sleep(0.0005)
		byte.value = (0,0,0,0,0,0,0,0)  #confirmation de rotation du moteur 1
		sleep(0.0005)
		moteurX = 1

	global sens_rotation, Codeur_moteur1
	if (sens_rotation == 1) : #and (Codeur_moteur1 <= VALEUR MAX DE DEBATTEMENT):
		rotation_moteur_1()
		Codeur_moteur1 += 1
	if (sens_rotation == 0) : #and (Codeur_moteur1 >= -VALEUR MAX DE DEBATTEMENT):
		rotation_moteur_1()
		Codeur_moteur1 -= 1
#Pour la sécurité anti collision : une fois le bras en bas, une collision avec la base est possible...


#6900 pas de débattement - Pour être droit : Se mettre en butée avant puis -4500 pas | 90° par rapport au 0 : +3200 pas
#240° de liberté - résolution (mode demi-pas) : 0.03°
def moteur_2() : #épaule
	def rotation_moteur_2():
		global moteurX
		byte.value = (0,1,0,0,0,0,0,1)  #ordre de rotation du moteur 2
		sleep(0.0015)
		byte.value = (0,0,0,0,0,0,0,1)  #confirmation de rotation du moteur 2
		sleep(0.0015)
		moteurX = 2

	global sens_rotation, Codeur_moteur2, Codeur_moteur3, bypass_limitations
	if (sens_rotation == 1) and ((Codeur_moteur2 <= 4500-1) and ((Codeur_moteur2 + Codeur_moteur3) <= 3200-1) or bypass_limitations):
		rotation_moteur_2()
		Codeur_moteur2 += 1
	if (sens_rotation == 0) and ((Codeur_moteur2 >= -2400+1) and ((Codeur_moteur2 + Codeur_moteur3) >= -4500+1) or bypass_limitations):
		rotation_moteur_2()
		Codeur_moteur2 -= 1


#7700 pas de débattement  - Pour être droit : Se mettre en butée arrière puis -3200 pas
#220° de liberté - résolution (mode demi-pas) : 0.03°
def moteur_3() : #coude
	def rotation_moteur_3():
		global moteurX
		byte.value = (0,1,0,0,0,0,1,0)  #ordre de rotation du moteur 3
		sleep(0.0015)
		byte.value = (0,0,0,0,0,0,1,0)  #confirmation de rotation du moteur 3
		sleep(0.0015)
		moteurX = 3

	global sens_rotation, Codeur_moteur3, Codeur_moteur2, Codeur_moteur4, bypass_limitations
	if (sens_rotation == 1) and (((Codeur_moteur2 + Codeur_moteur3) <= 3200-1) and ((Codeur_moteur4 + Codeur_moteur3) <= 3200-1) or bypass_limitations): #Sécurité anti-collision
		rotation_moteur_3()
		Codeur_moteur3 += 1
	elif (sens_rotation == 0) and (((Codeur_moteur2 + Codeur_moteur3) >= -4400+1) and ((Codeur_moteur4 + Codeur_moteur3) >= -3200+1) or bypass_limitations):
		rotation_moteur_3()
		Codeur_moteur3 -= 1


#6500 pas de débattement (faux ?) --> Le 0 pris en position verticale, le débattement se fait de 4000 à -4000 --> pince à 90° partant du 0 : +/-3200 pas
#l'axe 5 tourne en même temps (Mécaniquement logique), 
# ordonner les deux moteurs (4+5 pour garder la pince droite car 6400 pas = 1 tour de pince et 6400 pas = une rotation 180° main)
#220° de liberté - résolution (mode demi-pas) : 0.03°
def moteur_4() : #poignet
	def rotation_moteur_4():
		global moteurX
		byte.value = (0,1,0,0,0,0,1,1)  #ordre de rotation du moteur 4
		sleep(0.0015)
		byte.value = (0,0,0,0,0,0,1,1)  #confirmation de rotation du moteur 4
		sleep(0.0015)
		moteurX = 4

	global sens_rotation, Codeur_moteur4, Codeur_moteur3, bypass_limitations
	if (sens_rotation == 1) and (((Codeur_moteur4 + Codeur_moteur3) <= 3200-1) or bypass_limitations):
		rotation_moteur_4()
		Codeur_moteur4 += 1
	if (sens_rotation == 0) and (((Codeur_moteur4 + Codeur_moteur3) >= -3200+1) or bypass_limitations):
		rotation_moteur_4()
		Codeur_moteur4 -= 1


#12800 pas = 360° de la pince - rotation illimité
#degré de liberté infini - résolution (mode demi-pas) : 0.03°
def moteur_5() : #rotation main
	def rotation_moteur_5():
		global moteurX
		byte.value = (0,1,0,0,0,1,0,0)  #ordre de rotation du moteur 5
		sleep(0.0015)
		byte.value = (0,0,0,0,0,1,0,0)  #confirmation de rotation du moteur 5
		sleep(0.0015)
		moteurX = 5

	global sens_rotation, Codeur_moteur5, moteurX
	if sens_rotation == 1:
		rotation_moteur_5()
		Codeur_moteur5 += 1
	if sens_rotation == 0:
		rotation_moteur_5()
		Codeur_moteur5 -= 1


#6000 pas de débattement
#Position 0 du codeur : pince fermé
def moteur_6() : #pince
	def rotation_moteur_6():
		global moteurX
		byte.value = (0,1,0,0,0,1,0,1)  #ordre de rotation du moteur 6
		sleep(0.0015)
		byte.value = (0,0,0,0,0,1,0,1)  #confirmation de rotation du moteur 6
		sleep(0.0015)
		moteurX = 6

	global sens_rotation, Codeur_moteur6, bypass_limitations
	if (sens_rotation == 1) and ((Codeur_moteur6 <= 0) or bypass_limitations):
		rotation_moteur_6()
		Codeur_moteur6 += 1
	if (sens_rotation == 0) and ((Codeur_moteur6 >= -6000) or bypass_limitations):
		rotation_moteur_6()
		Codeur_moteur6 -= 1


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


def main(stdscr): # ---> le fait que ça soit définit ralentis peut-être le programme ? -- edit Olivier 2025 : Bahahahaha quel con
	curses.curs_set(0)                  # cache le curseur
	stdscr.nodelay(True)                # éntrées non blocantes
	stdscr.timeout(100)                 # Timeout de 100ms pour getch()
#	global variables
	global Menu, Menu_affiché, Mode_manuel, Test_moteurs, Dance_robot, Choix_dance
	global sens_rotation, vitesse_manu, bypass_limitations
	global Test_moteurs, Dance_robot, Choix_dance
	global moteurX, Codeur_moteur1, Codeur_moteur2, Codeur_moteur3, Codeur_moteur4, Codeur_moteur5, Codeur_moteur6
	stdscr.clear()
	key = stdscr.getch()

	while True : #key != 32 : # 32 en ASCII = Touche espace --> Arret d'URGENCE --> N'arettera pas le mouvement si un ordre est déja envoyé !! --> revoir ce système !

		if Menu == 1:
			key = stdscr.getch()			# Capturer la touche appuyée
			if key == ord('q') or key == ord('Q'):
				break
			elif Menu_affiché == False:
				menu_principal(stdscr)
				stdscr.refresh()
				Menu_affiché = True #Input() --> affichage menu 1 seule fois

			elif key == curses.KEY_F1:		# Mode manuel
				Mode_manuel = True
				Menu_affiché = False
				Menu = 0
			elif key == curses.KEY_F2:		# Choix du programme
				Menu_affiché = False
				Menu = 2

		elif Menu == 2:
			key = stdscr.getch()
			if key == 27:					# ESCAPE - retour au menu principal
				Menu_affiché = False
				Menu = 1
			elif Menu_affiché == False:
				menu_choix_programme(stdscr)
				stdscr.refresh()
				Menu_affiché = True


			elif key == curses.KEY_F1:		#Test des moteurs
				Test_moteurs = True
				Menu_affiché = False
				Menu = 0
			elif key == curses.KEY_F2:		# Dance des robot
				Dance_robot = True
				Menu_affiché = False
				Menu = 0


#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            2) CONTROLE MANUEL                                 #
#                                                                               #
#===============================================================================#


		while Mode_manuel == True:               #--> remplacer par if pour que l'ATU fonctionne ?
			stdscr.refresh()
			menu_mode_manuel(stdscr)
			key = stdscr.getch()
			if 100000 <= vitesse_manu <=0: #Empèchement d'une vitesse négative ou trop importante
				vitesse_manu =1
			match key:
			#0 == 48
			#1 == 49
			#....
			#p == 112
			#n == 110
				case 27:  # Touche ESC
					Menu = 1
					bypass_limitations = False
					Mode_manuel = False
			#elif key == 48: #Chiffre 0
			#	vitesse_manu = input()
				case 32:
					bypass_limitations = True
				case 10:	#Touche ENTER
					globals()[f'Codeur_moteur{moteurX}'] = 0
				case 112 | 80: # sens positif
					sens_rotation_1()
				case 110 | 78: # sens négatif
					sens_rotation_0()

				case 49: # 1
					for f1 in range (vitesse_manu):
						moteur_1()
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
			stdscr.clear()
			for i in range(1, 7):
				Pos_txt = ((i-1)/(6/18)) # Droite affine pour la position des textes
				Pos_txt = int(Pos_txt)

				stdscr.addstr(Pos_txt, 0, "Test de rotation du moteur {} : ".format(i))
				stdscr.refresh()
				sleep(1)
				for Boucle in range(2):
					if Boucle == 0:
						stdscr.addstr(Pos_txt + 1, 0, "- Sens de rotation Négatif :")
						stdscr.refresh()
						sens_rotation_0()
					else:
						stdscr.addstr(Pos_txt + 1, 0, "- Sens de rotation Positif :")
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
