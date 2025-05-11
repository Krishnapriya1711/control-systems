# control-systems
control a 4 degree of freedom robotic arm using webcam


This is the arduino code for the 3 motors, don't add the gripper initially
#include <Servo.h>

Servo motor1;  // Right hand, thumb + index
Servo motor2;  // Right hand, thumb + middle
Servo motor3;  // Left hand, thumb + index

void setup() {
  Serial.begin(9600);
  motor1.attach(3);
  motor2.attach(5);
  motor3.attach(6);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    if (input.startsWith("M1:")) {
      int angle = input.substring(3).toInt();
      motor1.write(angle);
    } else if (input.startsWith("M2:")) {
      int angle = input.substring(3).toInt();
      motor2.write(angle);
    } else if (input.startsWith("M3:")) {
      int angle = input.substring(3).toInt();
      motor3.write(angle);
    }
  }
} 


