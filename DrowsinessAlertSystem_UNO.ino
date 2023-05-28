char sleep_status = 0;
int buzzer=10;
int led_red = 9;
int led_green = 11;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buzzer, OUTPUT);
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
  digitalWrite(buzzer, LOW);
  digitalWrite(led_red, LOW);
  digitalWrite(led_green, LOW);  
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0)
  {
    sleep_status = Serial.read();
    if(sleep_status=='a')
    {
     digitalWrite(buzzer,HIGH);    
      digitalWrite(led_red,HIGH);     
      digitalWrite(led_green,LOW);               
    }
    else
    {
      digitalWrite(buzzer,LOW);
      digitalWrite(led_red,LOW);
      digitalWrite(led_green,HIGH);
    }        
  }

}
