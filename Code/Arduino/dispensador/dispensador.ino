1.	#include <Servo.h>
2.	Servo servoMotor;
3.	 
4.	void setup() {                
5.	 
6.	  servoMotor.attach(9); 
7.	  }
8.	 
9.	void loop() {
10.	 
11.	  servoMotor.write(0);
12.	  delay (1000);    
13.	  servomotor.write(90);
14.	  delay(1000);
15.	  servomotor.write(180);
16.	  delay(1000);
