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

This code is including the gripper
#include <Servo.h>

Servo motor1;  // Right hand, thumb + index
Servo motor2;  // Right hand, thumb + middle
Servo motor3;  // Left hand, thumb + index
Servo motor4;  // Left hand, thumb + middle (gripper)

void setup() {
  Serial.begin(9600);
  motor1.attach(3);
  motor2.attach(5);
  motor3.attach(6);
  motor4.attach(9);  // Choose any free PWM pin
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    if (input.startsWith("M1:")) {
      int angle = input.substring(3).toInt();
      angle = constrain(angle, 0, 180);
      motor1.write(angle);
      Serial.println("Received M1: " + String(angle));
    } else if (input.startsWith("M2:")) {
      int angle = input.substring(3).toInt();
      angle = constrain(angle, 0, 180);
      motor2.write(angle);
      Serial.println("Received M2: " + String(angle));
    } else if (input.startsWith("M3:")) {
      int angle = input.substring(3).toInt();
      angle = constrain(angle, 0, 180);
      motor3.write(angle);
      Serial.println("Received M3: " + String(angle));
    } else if (input.startsWith("M4:")) {
      int angle = input.substring(3).toInt();
      angle = constrain(angle, 0, 30);  // Gripper range only
      motor4.write(angle);
      Serial.println("Received M4 (Gripper): " + String(angle));
    }
  }
}

