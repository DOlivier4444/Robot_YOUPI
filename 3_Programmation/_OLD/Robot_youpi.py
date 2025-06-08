

#===============================================================================#
#                                                                               #
#                            Robot youpi - Olivier DANIEL                       #
#                                                                               #
#                            0) DEFINITION DES VARIABLES                        #
#                                                                               #
#===============================================================================#


# 0.1) chargement des modules
from gpiozero import LEDBoard #type:ignore
#from gpiozero.pins.pigpio import PiGPIOFactory #install pigpio
#factory = PiGPIOFactory(host='192.168.1.3')
#workaround to execute the code without a Rpi, comment the 2 lines above when executed to the raspberry
from time import sleep
from enum import Enum
import numpy as np #type:ignore
from math import pi


# 0.2) Création d'un byte envoyé au robot pour le contrôler
#LEDBoard("GPIO18") = bit8 = Validation_sens_rotation = D7 
#LEDBoard("GPIO23") = bit7 = Validation_pas_moteur    = D6 
#LEDBoard("GPIO24") = bit6 = moteur6__pince           = D5 = .,.,.,.,.,1,0,1
#LEDBoard("GPIO25") = bit5 = moteur5__rotation_main   = D4 = .,.,.,.,.,1,0,0
#LEDBoard("GPIO12") = bit4 = moteur4__poignet         = D3 = .,.,.,.,.,0,1,1
#LEDBoard("GPIO16") = bit3 = moteur3__coude           = D2 = .,.,.,.,.,0,1,0
#LEDBoard("GPIO20") = bit2 = moteur2__epaule          = D1 = .,.,.,.,.,0,0,1
#LEDBoard("GPIO21") = bit1 = moteur1__base            = D0 = .,.,.,.,.,0,0,0

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

class speed(Enum):
	#sécurité pour ne pas dépasser la vitesse maximale des moteurs --> http://www.alphak.net/news/2009/12/youpi-testons-les-moteurs/
	#T=(1/(40/0.028125)/2) = (0.028125*2)/40 = 0.0015 --> 0.002 pour le moteur de la base
	low = 0.005
	medium = 0.003
	High = 0.0015
	MAX = 0.000


#DH parameters of the Robot Youpi --> https://automaticaddison.com/the-ultimate-guide-to-inverse-kinematics-for-6dof-robot-arms/
#https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
#			                θi (deg)       αi (deg)         ai/ri (cm)	di (cm)		Joint i
dh_params = np.array([[np.deg2rad(180.0), np.deg2rad(90.0),   0.0,	    28.0],			#1
                      [np.deg2rad(90.0),  np.deg2rad(0.0),    16.2,		0.0],			#2
                      [np.deg2rad(0.0),   np.deg2rad(0.0),    16.2,		0.0],			#3
                      [np.deg2rad(90.0),  np.deg2rad(90.0),   0.0,		0.0],			#4
                      [np.deg2rad(0.0),   np.deg2rad(0.0),    0.0,		150.0]])		#5


def sens_rotations(rotations: list[rotation], coders_motors: list[int], thetas: list[float]):
    for i in range(0, 6):
        if i == 2:  # Pour theta[2] (motor3), la condition est inversée
            rotations[i] = rotation.FORWARD if coders_motors[i] >= thetas[i] / 0.028125 else rotation.BACKWARDS
        elif i == 5:  # Pour theta[5] (motor6), la formule est différente
            rotations[i] = rotation.FORWARD if coders_motors[i] >= thetas[i] * (-60) else rotation.BACKWARDS
        else:  # Pour tous les autres moteurs
            rotations[i] = rotation.FORWARD if coders_motors[i] <= thetas[i] / 0.028125 else rotation.BACKWARDS

    # Envoi et confirmation du signal de sens de rotation
    byte.value = [1, 0] + rotations  # envoie du signal de sens de rotation
    byte.value = [0, 0] + rotations  # confirmation du signal de sens de rotation
	
def validate_move(coders_motors:list[int], rotations:list[rotation], motor_id:motor) -> bool:
	match motor_id:
		case motor.MOTOR_1_base : #base
		# données encore inconnus --> décrassage nécessaire
		#340° de liberté - résolution (mode demi-pas) : 0.03°
		#90° = --
		#--° = 1
		#Pour la sécurité anti collision : une fois le bras en bas, une collision avec la base est possible...
			return True #(
			#	rotations[motor_id] == rotation.FORWARD
			#	and (coders_motors[motor.MOTOR_1_base] <= +200) #VALEUR MAX DE DEBATTEMENT A TROUVER...
			#) or (
			#	rotations[motor_id] == rotation.BACKWARDS
 			#	and (coders_motors[motor.MOTOR_1_base] >= -200) #-VALEUR MAX DE DEBATTEMENT
			#)
		case motor.MOTOR_2_shoulder : #épaule
		#6900 pas de débattement - Pour être droit : Se mettre en butée avant puis -4500 pas | 90° par rapport au 0 : +3200 pas
		#90° = +3200
		#0.03° = 1
		#240° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and (coders_motors[motor.MOTOR_2_shoulder.value] <= 4500)
				and ((coders_motors[motor.MOTOR_2_shoulder.value] + coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS 
				and (coders_motors[motor.MOTOR_2_shoulder.value] >= -2400)
				and ((coders_motors[motor.MOTOR_2_shoulder.value] + coders_motors[motor.MOTOR_3_elbow.value]) >= -4500)
			)
		case motor.MOTOR_3_elbow : #coude
		#7700 pas de débattement  - Pour être droit : Se mettre en butée arrière puis -3200 pas
		#90° = +3200
		#0.03° = 1
		#220° de liberté - résolution (mode demi-pas) : 0.03°
			return (
				rotations[motor_id.value] == rotation.FORWARD
				and ((coders_motors[motor.MOTOR_2_shoulder.value] + coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
				and ((coders_motors[motor.MOTOR_4_wrist_tilt.value] + coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
			  and ((coders_motors[motor.MOTOR_2_shoulder.value] + coders_motors[motor.MOTOR_3_elbow.value]) >= -4400)
			  and ((coders_motors[motor.MOTOR_4_wrist_tilt.value] + coders_motors[motor.MOTOR_3_elbow.value]) >= -3200)
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
				and ((coders_motors[motor.MOTOR_4_wrist_tilt.value] + coders_motors[motor.MOTOR_3_elbow.value]) <= 3200)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
				and ((coders_motors[motor.MOTOR_4_wrist_tilt.value] + coders_motors[motor.MOTOR_3_elbow.value]) >= -3200)
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
				and (coders_motors[motor.MOTOR_6_actuator.value] <= 0)
			) or (
				rotations[motor_id.value] == rotation.BACKWARDS
				and (coders_motors[motor.MOTOR_6_actuator.value] >= -6000)
			)
def step_motor(motor_id:motor, coders_motors:list[int], rotations, speed_value:speed):
	if validate_move(coders_motors, rotations, motor_id):

		#bin_id = bin(motor_id)[::-1]
		#bit_1 = (bin_id & (1 << 0)) >> 0
		#bit_2 = (bin_id & (1 << 1)) >> 1
		#bit_3 = (bin_id & (1 << 2)) >> 2
		#byte.value = (0,1,0,0,0,bit_1, bit_2, bit_3)  #ordre de rotation du moteur
		#byte.value = (0,0,0,0,0,bit_1, bit_2, bit_3)  #confirmation de rotation du moteur

		bin_motor = bin(motor_id.value)[2:]  #Convertir en binaire et enlever le "0b"
		bin_motor = bin_motor.zfill(3)  #Compléter avec 3 zéros pour garantir la longueur désirée
		bin_motor = [int(digit) for digit in bin_motor]  #Convertir en liste d'entiers
		#--> pas forcément optimisé : int --> bin --> list[int] ... le mieux serait int --> bin
		byte.value = ([0,1,0,0,0,] + bin_motor)  #envoie du signal de sens de rotation
		byte.value = ([0,0,0,0,0,] + bin_motor)  #confirme le sens de rotation || #byte.value = (0,0,0,0,0, *bin_motor) aurait pu être utilisé : *bin_motor sers à décompacter la liste [x,x,x] --> x,x,x
		sleep(speed_value)


#..........................................................................................................................................................................................................
#..........................................................................................................................................................................................................
		match rotations[motor_id.value]:
			case rotation.FORWARD :
				coders_motors[motor_id.value] += 1
				# change the codor value of the n+1 arm depending on the n arm : this make the n arm the reference frame of the movement of the n+1 arm
				# because of the technical limitation 
				#if motor_id != motor.MOTOR_1_base and motor_id != motor.MOTOR_5_wrist_rotation :
				#	coders_motors[motor_id.value+1] += 1

			case rotation.BACKWARDS :
				coders_motors[motor_id.value] -= 1
				#if motor_id != motor.MOTOR_1_base and motor_id != motor.MOTOR_5_wrist_rotation :
				#	coders_motors[motor_id.value+1] -= 1
		return coders_motors
#..........................................................................................................................................................................................................
#..........................................................................................................................................................................................................


def forward_kinematic_solver(dh_params, thetas:list[float], joints_position:list[float]):
	r1 = ((np.sin(dh_params[1,0]) * dh_params[1,2]) + 
		  (np.sin(dh_params[2,0]) * dh_params[2,2]) +
		  (np.sin(dh_params[3,0]) * dh_params[4,3])
		  )
	x = np.cos(dh_params[0,0]) * r1
	y = np.sin(dh_params[0,0]) * r1
	z = dh_params[0,3] + (
		(np.cos(dh_params[1,0]) * dh_params[1,2]) +
		(np.cos(dh_params[2,0]) * dh_params[2,2]) +
		(np.cos(dh_params[3,0]) * dh_params[4,3])
		)
	ry = thetas[3]
	rz = thetas[0] + thetas[3] + thetas[4]
	joints_position = [x, y, z, ry, rz]
	return joints_position

def inverse_kinematic_solver():
	pass


def goto_xyzabc(): # [x,y,z,a,b,c] go to a desired position, using inverse kinematics
	inverse_kinematic_solver()
	pass

def goto_joints_angle(coders_motors:list[int], joints_position:list[float], rotations:list[rotation], thetas:list[float], speed_value:speed):
	#[θ1, θ2, θ3, θ4, θ5, 100%] go to a desired angle, using forward kinematics (the actuator is 0 - 100%)
	sens_rotations(rotations, coders_motors, thetas)

	#conversion from angle° to step (0.028125°/step) - (from percentage to step for the motor 6)
	coders_motors_target = [
							thetas[0] / 0.028125,
							thetas[1] / 0.028125,
							thetas[2] / 0.028125,	#Note : The sens in reversed for this one
							thetas[3] / 0.028125,
							thetas[4] / 0.028125,
							thetas[5] * (-60)		#Note : 100% == -6000 // 0% == 0
							]

	for _ in range(int(max(coders_motors_target))) :
		for i in range(0, 6):
			step_motor(motor(i), coders_motors, rotations, speed_value)
			forward_kinematic_solver(dh_params, thetas, joints_position)
			print(coders_motors, joints_position)


def main():
#	speed_manu = speed.zero
	coders_motors = [0] *6 # Initialisation des codeurs à 0
	rotations = [rotation.FORWARD] *6
	joints_position = [0] *5
	thetas=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	joints_position = forward_kinematic_solver(dh_params, thetas, joints_position)

	goto_joints_angle(
		thetas=[0.0, 45.0, 0.0, 0.0, 0.0, 0.0],
		speed_value=speed.MAX
	)

	print(rotations)
	print(joints_position)

if __name__ == "__main__":
	main()
