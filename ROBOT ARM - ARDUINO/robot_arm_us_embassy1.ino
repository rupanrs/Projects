// C++ code
// LAPTOP NO 19

#include <Servo.h>

Servo myservo3;
Servo myservo5;
Servo myservo6;

int potpin=0;
int potpin2=1;
int potpin3=2;

int val=0;
int val2=0;
int val3=0;

void setup()
{
  myservo3.attach(9);
  myservo5.attach(10);
  myservo6.attach(11);
}

void loop()
{
  val = analogRead(potpin);
  val = map(val, 3, 1023, 0, 176);
  myservo3.write(val);
  
  delay(25);
  
  val2 = analogRead(potpin2);
  val2 = map(val2, 3, 1023, 0, 176);
  myservo5.write(val2);
  
  delay(25);
  
  val3 = analogRead(potpin3);
  val3 = map(val3, 3, 1023, 0, 175);
  myservo6.write(val3);
  
  delay(25);
}