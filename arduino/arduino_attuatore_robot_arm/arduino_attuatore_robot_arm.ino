#include <Servo.h>

// create servo objects to control a servo
Servo myservo_1;  
Servo myservo_2; 

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo_1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo_2.attach(8);  // attaches the servo on pin 8 to the servo object

  // tell servo to go to initial position 
  myservo_1.write(70);  
  myservo_2.write(90);
} 

void loop() {

  if (Serial.available()>0){

    Serial.read();
    
    for (pos = 55; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo_1.write(pos);              // tell servo to go to position in variable 'pos'
        myservo_2.write(pos);
        delay(15);                       // waits 15 ms for the servo to reach the position
      }
    for (pos = 180; pos >= 55; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo_1.write(pos);              // tell servo to go to position in variable 'pos'
        myservo_2.write(pos);
        delay(15);                       // waits 15 ms for the servo to reach the position
    }

    for (pos = 55; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo_1.write(pos);              // tell servo to go to position in variable 'pos'
        myservo_2.write(pos);
        delay(15);                       // waits 15 ms for the servo to reach the position
      }
    for (pos = 180; pos >= 55; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo_1.write(pos);              // tell servo to go to position in variable 'pos'
        myservo_2.write(pos);
        delay(15);                       // waits 15 ms for the servo to reach the position
    }

    myservo_1.write(70);  
    myservo_2.write(90);
  }
}
