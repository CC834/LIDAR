const float SOUNDSPEED = 343.0; // Speed of sound in m/s

// Define pin connections
const int trigPin = 13;
const int echoPin = 12;
int count = 0;
void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the duration of echo pulse
  float duration = pulseIn(echoPin, HIGH);

  // Convert duration to distance in cm
  float distance = (duration * 0.0343) / 2;  
  count = count + 1;
  Serial.print(count);
  Serial.print(" Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}
