int current;
void setup() {
  // put your setup code here, to run once:
  pinMode(A5, INPUT);
  Serial.begin(115200);
  Serial.setTimeout(1);

}

void loop() {
  // put your main code here, to run repeatedly:
  current = analogRead(A5);
  while (!Serial.available())
  {
    Serial.print(current);
    }
}
