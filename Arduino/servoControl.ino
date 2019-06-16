#include <Servo.h> //используем библиотеку для работы с сервоприводом
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6; //объявляем переменную servo типа Servo
String b = "a";
String a;
void setup() //процедура setup
{
  Serial.begin(9600);
  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);//привязываем привод к порту 10
  servo4.attach(9);
  servo5.attach(8);
  servo6.attach(7);
  servo1.write(70);
  servo2.write(70);
  servo3.write(70);
  servo4.write(70);
  servo5.write(70);
  servo6.write(70);
}
void loop() //процедура loop
{
  if (Serial.available() > 0) {

    Serial.print(" I received:");
    char c = Serial.read();// read the incoming data as string
    a += c;
    Serial.println(a);
    if (a == "3"){
        servo6.write(30);
        delay(1000);
        servo6.write(70);
        delay(1000);
        servo1.write(0);
        delay(1000);
        servo1.write(70);
        delay(1000);
//      Serial.println("Servo 1");
//      servo1.write(80); //ставим вал под 0
//      delay(2000); //ждем 2 секунды
//      servo1.write(0); //ставим вал под 180
//      delay(2000); //ждем 2 секунды
    }
    if (a.equals("1")){
        servo4.write(30);
        delay(1000);
        servo4.write(70);
        delay(1000);
        servo2.write(0);
        delay(1000);
        servo2.write(70);
        delay(1000);
//      servo2.write(160); //ставим вал под 0
//      delay(2000); //ждем 2 секунды
//      servo2.write(30); //ставим вал под 180
//      delay(2000); //ждем 2 секунды
    }
    if (a.equals("2")){
        servo5.write(30);
        delay(1000);
        servo5.write(70);
        delay(1000);
        servo3.write(0);
        delay(1000);
        servo3.write(70);
        delay(1000);
//      servo3.write(120); //ставим вал под 0
//      delay(2000); //ждем 2 секунды
//      servo3.write(0); //ставим вал под 180
//      delay(2000); //ждем 2 секунды
    }
    a= "";

  }

}
