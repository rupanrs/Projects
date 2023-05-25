// Motor controller
int enaPin = 9;        // Enable pin connected to Arduino pin 9
int in1Pin = 8;        // IN1 pin connected to Arduino pin 8
int in2Pin = 7;        // IN2 pin connected to Arduino pin 7
int irSensorPin = 2;   // IR sensor output pin connected to Arduino pin 2
int buzzerPin = 12;    // Buzzer pin connected to Arduino pin 12

int motorSpeed = 0;    // Variable to store motor speed
int objectCount = 0;   // Variable to store object count

void setup() {
  pinMode(enaPin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(irSensorPin, INPUT_PULLUP); // Configure IR sensor pin as input with internal pull-up resistor
  pinMode(buzzerPin, OUTPUT);         // Configure buzzer pin as output
  
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  if (digitalRead(irSensorPin) == LOW) {
    // Object detected by IR sensor
    objectCount++;
    Serial.print("Object Count: ");
    Serial.println(objectCount);
    beep();        // Call the beep function to make a small beep sound
    delay(3000);   // Delay to avoid multiple counts for a single object
  }

  if (Serial.available()) {
    // Read the incoming speed value from the serial port
    motorSpeed = Serial.parseInt();
    
    // Constrain the speed value to be within the valid range (0-255)
    motorSpeed = constrain(motorSpeed, 0, 255);
    
    // Set the motor direction and speed
    if (motorSpeed >= 0) {
      digitalWrite(in1Pin, HIGH);
      digitalWrite(in2Pin, LOW);
    } else {
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, HIGH);
    }
    
    analogWrite(enaPin, abs(motorSpeed)); // Set the motor speed using analogWrite
  }
}

void beep() {
  digitalWrite(buzzerPin, HIGH); // Turn on the buzzer
  delay(500);                    // Beep duration
  digitalWrite(buzzerPin, LOW);  // Turn off the buzzer
}
