bool validate_move(int motorID, int rotation, int codersMotors[]) {
  
  const int FORWARD   = 1;
  const int BACKWARDS = 0;

  const int MOTOR_1 = 0;  //D0 - motor1__base
  const int MOTOR_2 = 1;  //D1 - motor2__shoulder
  const int MOTOR_3 = 2;  //D2 - motor3__elbow
  const int MOTOR_4 = 3;  //D3 - motor4__wrist
  const int MOTOR_5 = 4;  //D4 - motor5__rotation_hand
  const int MOTOR_6 = 5;  //D5 - motor6__gripper


  // Motor coder limits logic
  const int MOTOR_LIMITS[6][2] = {
    {200    , -200  },    // MOTOR_1
    {4500   , -2400 },    // MOTOR_2
    {3200   , -4400 },    // MOTOR_3
    {3200   , -3200 },    // MOTOR_4
    {0      , 0     },    // MOTOR_5 (illimité)
    {0      , -6000 }     // MOTOR_6
  };

  switch (motorID) {
    case MOTOR_1:  // MOTOR_1 - base
      // donnees encore inconnus
      //340degree de liberte - resolution (mode demi-pas) : 0.03degree
      //90degree = --
      //--degree = 1
      //Pour la securite anti collision : une fois le bras en bas, une collision avec la base est possible...
      //(
      //	rotations[motor_id] == rotation.FORWARD
      //	&& (coders_motors[motor.MOTOR_1_base] <= +200) //VALEUR MAX DE DEBATTEMENT A TROUVER...
      //) or (
      //	rotations[motor_id] == rotation.BACKWARDS
      //	&& (coders_motors[motor.MOTOR_1_base] >= -200) //-VALEUR MAX DE DEBATTEMENT
      //)
      return true;  // Pas de restrictions spécifiques encore définies


    case MOTOR_2:  // MOTOR_2 - epaule
      //6900 pas de debattement - Pour etre droit : Se mettre en butee avant puis -4500 pas | 90degree par rapport au 0 : +3200 pas
      //90degree = +3200
      //0.03degree = 1
      //240degree de liberte - resolution (mode demi-pas) : 0.03degree
      return (
        (rotation == FORWARD
        && codersMotors[MOTOR_2] <= MOTOR_LIMITS[MOTOR_2][0]
        && (codersMotors[MOTOR_2] + codersMotors[MOTOR_3]) <= MOTOR_LIMITS[MOTOR_3][0]) 
        || (rotation == BACKWARDS
        && codersMotors[MOTOR_2] >= MOTOR_LIMITS[MOTOR_2][1]
        && (codersMotors[MOTOR_2] + codersMotors[MOTOR_3]) >= MOTOR_LIMITS[MOTOR_3][1])
      );


    case MOTOR_3:  // MOTOR_3 - coude
      //7700 pas de d�battement  - Pour �tre droit : Se mettre en but�e arri�re puis -3200 pas
      //90� = +3200
      //0.03� = 1
      //220� de libert� - r�solution (mode demi-pas) : 0.03�
      return (
        (rotation == FORWARD
        && (codersMotors[MOTOR_2] + codersMotors[MOTOR_3]) <= MOTOR_LIMITS[MOTOR_3][0]
        && (codersMotors[MOTOR_4] + codersMotors[MOTOR_3]) <= MOTOR_LIMITS[MOTOR_4][0])
        ||
        (rotation == BACKWARDS
        && (codersMotors[MOTOR_2] + codersMotors[MOTOR_3]) >= MOTOR_LIMITS[MOTOR_3][1]
        && (codersMotors[MOTOR_4] + codersMotors[MOTOR_3]) >= MOTOR_LIMITS[MOTOR_4][1])
      );


    case MOTOR_4:  // MOTOR_4 - poignet
      //6500 pas de d�battement  --> Le 0 pris en position verticale, le d�battement se fait de 4000 � -4000 --> pince � 90� partant du 0 : +/-3200 pas
      //90� = +3200
      //0.03� = 1
      //l'axe 5 tourne en m�me temps (M�caniquement logique),
      // ordonner les deux moteurs (4+5 pour garder la pince droite car 1 tour de pince = 6400 pas = une rotation 180� main)
      //220� de libert� - r�solution (mode demi-pas) : 0.03�
      return (
        (rotation == FORWARD
        && (codersMotors[MOTOR_4] + codersMotors[MOTOR_3]) <= MOTOR_LIMITS[MOTOR_4][0])
        ||
        (rotation == BACKWARDS
        && (codersMotors[MOTOR_4] + codersMotors[MOTOR_3]) >= MOTOR_LIMITS[MOTOR_4][1])
      );


    case MOTOR_5:  // MOTOR_5 - rotation main
      //12800 pas = 360� de la pince - rotation illimit�
      //90� = +3200
      //0.03� = 1
      //degr� de libert� infini - r�solution (mode demi-pas) : 0.03�
      return true;  // Mouvement illimité


    case MOTOR_6:  // MOTOR_6 - Actuator
      //6000 pas de d�battement
      //90mm = +6000
      //0.015mm = 1
      //Position 0 du codeur : pince ferm�
      return (
        (rotation == FORWARD
        && codersMotors[MOTOR_6] <= MOTOR_LIMITS[MOTOR_6][0])
        ||
        (rotation == BACKWARDS
        && codersMotors[MOTOR_6] >= MOTOR_LIMITS[MOTOR_6][1])
      );


    default:
      return false;  // ID de moteur invalide
  }
}