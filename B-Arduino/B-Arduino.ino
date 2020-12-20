#include <Timer.h>
#include <SPI.h>
#include <SD.h>

Timer t;
int interval = 1; //ms
//File file;
int8_t id;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //SD.begin(4);
  //file = SD.open("D:\faculdade\5º ano\Projeto de Sensores, Sinais e Instrumentação\Labs\Lab_6\b1.txt", FILE_WRITE);         
  t.every(interval, get_value, (void*)0);
}

void loop() {
  // put your main code here, to run repeatedly:
  //id = t.every(sampling_frequency, file.println(analogRead(A0)),(void*)0);
  t.update();
  //t.after(4000, stop, (void*)0);
  
}

/*
void stop(){
  t.stop(id); file.close();
}
*/
void get_value() {
  Serial.println(analogRead(A0));
  }
