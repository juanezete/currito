#include "AFMotor.h"
#include "Servo.h"

Servo servo;

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

int velocidad = 0;
int angulo = 0;
 
void moverCabeza(int angulo){
  servo.write(angulo);  
}

void setup() {
  Serial.begin(9600);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  servo.attach(10);
}

void loop() {
 

  while(1){
    // Si se recibe dato
    if (Serial.available() > 0) {
      
      // Lee el dato enviado por la Raspberry Pi
      byte datos[sizeof(int) * 3];
    Serial.readBytes(datos, sizeof(int) * 3);

    // Desagrupar los datos
    int dato1, dato2, dato3;
    memcpy(&dato1, &datos[0], sizeof(int));
    memcpy(&dato2, &datos[sizeof(int)], sizeof(int));
    memcpy(&dato3, &datos[2 * sizeof(int)], sizeof(int));
      
      if(dato1>0){
        motor1.run(FORWARD);

      }else{
        motor1.run(BACKWARD);
      }  
      if(dato2>0){
        motor2.run(FORWARD);

      }else{
        motor2.run(BACKWARD);
      } 
      motor1.setSpeed(abs(dato1));
      motor2.setSpeed(abs(dato2));
      servo.write(dato3); 
    }
    else{
      delay(500);
    }
  }
}
