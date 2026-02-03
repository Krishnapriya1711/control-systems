# control-systems
Control a 4 degree of freedom robotic arm using webcam

This is my control systems project for the 4th semester. The arm can be made by 3d printing/ can be bought.
It has 4 degrees of freedom:
1. Rotation of the base
2. Move the arm forward and backward
3. Move the elbow up and down
4. Movement of the gripper - open and close

It has been implemented in the following manner -
1. movement of base - right hand, thumb + index
2. movement of arm i.e up and down - right hand, thumb + middle
3. movement of arm i.e forward and backward - left hand, thumb and index
4. movement of gripper - left hand, thumb + middle

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


Videos of the demo can be found in the media file.

