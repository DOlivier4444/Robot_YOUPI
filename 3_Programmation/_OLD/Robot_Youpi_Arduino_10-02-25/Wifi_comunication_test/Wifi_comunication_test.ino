
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.println("Arduino prêt pour la communication série !");
}


void loop(){
  int Delay = 1500;
  int motor_id = 2;

  if (Serial.available() > 0){

    String receivedData = Serial.readStringUntil('\n');
    receivedData.trim(); // leading and trailing whitespace removed

    // Sending the rotation direction
    PORTD = ((11111111 << 2) & B11111100);  // set the direction of rotations
    PORTB = B00000010;
    delayMicroseconds(Delay);
    PORTB = B00000000;  // send the direction of rotations

    while (receivedData == "0"){
      String receivedData = Serial.readStringUntil('\n');
      receivedData.trim(); // leading and trailing whitespace removed

      PORTD = ((motor_id << 2) & B00011100);  // Send the byte to prepare for the rotation of the chosen motor
      PORTB = B00000001;
      delayMicroseconds(Delay);  // Send the byte to order the rotation
      PORTB = B00000000;
    }
  }
}




/* ---------------------- 1ers test communication série -------------------------

void loop() {
  
  if (Serial.available() > 0) {

    String receivedData = Serial.readStringUntil('\n');
    receivedData.trim(); // leading and trailing whitespace removed

    Serial.print("Données reçues : ");
    Serial.println(receivedData);

    // Réponse en fonction du type de données reçues
    if (receivedData.toInt() != 0 || receivedData == "0") {
      Serial.println(receivedData.toInt() + 1); // Retourne un entier incrémenté

    } else if (receivedData.toFloat() != 0.0 || receivedData == "0.0") {
      Serial.println(receivedData.toFloat() + 1.1); // Retourne un flottant incrémenté

    } else if (receivedData.length() == 1) {
      char receivedChar = receivedData[0];
      Serial.println((char)(receivedChar + 1)); // Retourne le caractère suivant

    } else {
      Serial.println("Texte : " + receivedData); // Retourne le texte reçu avec un préfixe
    }
  }
}
*/

