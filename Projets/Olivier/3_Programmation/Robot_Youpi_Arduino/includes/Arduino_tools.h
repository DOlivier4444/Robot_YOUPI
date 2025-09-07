#include <stdio.h>

void reboot() { // Software reboot using the watchdog
  constexpr int RESET_PIN_JMPR = 12;
  pinMode(RESET_PIN_JMPR, OUTPUT);

  digitalWrite(RESET_PIN_JMPR, LOW);
  delay(200);
  digitalWrite(RESET_PIN_JMPR, HIGH);

}