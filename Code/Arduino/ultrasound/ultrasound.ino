1.	#define Pecho 6
2.	#define Ptrig 7
3.	long duracion, distancia;  
4.	 
5.	void setup() {                
6.	 
7.	  pinMode(Pecho, INPUT);     // define el pin 6 como entrada (echo)
8.	  pinMode(Ptrig, OUTPUT);    // define el pin 7 como salida  (triger) MIDE DISTANCIA
9.	  pinMode(13, 1);            // Define el pin 13 como salida
10.	  pinMode(4, 1);
11.	 
12.	  }
13.	 
14.	void loop() {
15.	 
16.	  digitalWrite(Ptrig, LOW);
17.	  delayMicroseconds(2); //ESPERAR 2 SEGUNDOS ENTRE LAS MEDICIONES
18.	  digitalWrite(Ptrig, HIGH);   // genera el pulso de triger por 10ms
19.	  delayMicroseconds(10);
20.	  digitalWrite(Ptrig, LOW);
21.	  duracion = pulseIn(Pecho, HIGH);
22.	  distancia = (duracion/2) / 29;            // calcula la distancia en centimetros
23.	 
24.	  if (distancia < 500 || distancia > 0){  // si la distancia es MENOR a 500cm o MAYOR a 0cm
25.	  {
26.	    digitalWrite(13, 0);              
27.	    digitalWrite(4, 1);
28.	  }
29.	  else{
30.	   if (distancia <= 10 && distancia >= 1){
31.	    digitalWrite(13, 1);                     // en alto el pin 13 si la distancia es menor a 10cm
32.	    digitalWrite(4, 0);
33.	  }}                                
34.	}
