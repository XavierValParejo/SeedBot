1.	const int pinENA = 9;
2.	const int pinIN1 = 11;
3.	const int pinIN2 = 13;
4.	int speed = 200;
5.	void setup() {                
6.	 
7.	  pinMode(pinIN1, OUTPUT); 
8.	  pinMode(pinIN2, OUTPUT);
9.	  pinMode(pinENA, OUTPUT); 
10.	  }
11.	 
12.	void loop() {
13.	  digitalWrite(pinIN1, HIGH);
14.	  digitalWrite(pinIN2, LOW);
15.	  analogWrite(pinENA, speed);    
16.	  delay(1000);
17.	   }
