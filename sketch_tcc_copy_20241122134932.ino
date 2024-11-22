#include <MQ7.h>

// int dht = A0;
int ldr = A1;
int soil = A2;
int ntc = A3;
int mq7 = A10;


float t0, vr, rt, ln, temp;

void setup() {
  Serial.begin(9600);
  t0 = 25 + 273.15; //Referencia em Kelvin
}

void loop() {
  
  // Leitura dos sensores


  // MQ7
  int coLevel = analogRead(mq7);
  int coPer = map(coLevel, 0, 1023, 0, 100);


  // UMIDADE DE SOLO
  int soilMoisture = analogRead(soil);
  soilMoisture = map(soilMoisture, 0, 1023, 0, 100);

  // LDR
   int valorldr = analogRead(ldr);
   int ldrPer = map(valorldr, 0, 1023, 0, 100);

  // NTC
  float valorntc = analogRead(ntc);
  valorntc = (5.00 / 1023.00) * valorntc;
  vr = 5.00 - valorntc;
  rt = valorntc / (vr/10000);

  ln = log(rt/10000.0);
  temp = 1/((ln/3977) + (1/t0));
  temp = temp - 273.15;

  

  Serial.print("HIGR ");
  Serial.print(soilMoisture);
  Serial.println("%");

  Serial.print("NTC ");
  Serial.println(temp);

    if (coPer > 8) {
      Serial.print("MQ7 ");
      Serial.print(coLevel);
      Serial.print("ppm ");
      Serial.print(coPer);
      Serial.print("% ");
      Serial.println("FUMACA DETECTADA");
    } else {
      Serial.print("MQ7 ");
      Serial.print(coLevel);
      Serial.print("ppm ");
      Serial.print(coPer);
      Serial.print("% ");
      Serial.println("SEM FUMACA");
    }


  Serial.print("LDR ");
  Serial.print(ldrPer);
  Serial.println("%");

  delay(5000); // Intervalo de 30 segundos entre leituras
}