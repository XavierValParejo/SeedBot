const int ENA = 11;
const int ENB = 6;

const int IN1E = 9;
const int IN2E = 10;

const int IN1D = 5;
const int IN2D =3 ;

const int wheel_size = 45;
const float cir_wheel = 3.14 * wheel_size;

const int robot_size = 100; //robot width
const float cir_robot = 3.14 * robot_size;

const float dist_to_turn = cir_robot/8;

const float voltes = dist_to_turn / wheel_size;

const float rps = 148/60;

const float segons = (voltes/rps)*1000;

void setup(){
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
  pinMode(IN1E,OUTPUT);
  pinMode(IN2E,OUTPUT);
  pinMode(IN1D,OUTPUT);
  pinMode(IN2D,OUTPUT);  
}

void Gir_esquerra(){
	digitalWrite(IN1E,HIGH);
  	digitalWrite(IN2E,LOW);
  	digitalWrite(IN1D,LOW);
  	digitalWrite(IN2D,HIGH);
  	delay(segons);
  	digitalWrite(IN1E,LOW);
  	digitalWrite(IN2E,LOW);
  	digitalWrite(IN1D,LOW);
  	digitalWrite(IN2D,LOW);

}

void Gir_dreta(){
	digitalWrite(IN1E,LOW);
  	digitalWrite(IN2E,HIGH);
  	digitalWrite(IN1D,HIGH);
  	digitalWrite(IN2D,LOW);
  	delay(segons);
  	digitalWrite(IN1E,LOW);
  	digitalWrite(IN2E,LOW);
  	digitalWrite(IN1D,LOW);
  	digitalWrite(IN2D,LOW);
  
}

void loop(){//codi prova
 analogWrite(ENA,200);
 analogWrite(ENB,200); 
 Gir_esquerra();
 delay(1000);
 Gir_dreta();
 analogWrite(ENA,20);
 analogWrite(ENB,20); 
  
}
