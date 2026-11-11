
const int IA_A = 5;
const int IB_A = 6;
const int IA_B = 9;
const int IB_B = 10;
int led_r =12;
int led_b =3;

void stopMotors() {
  digitalWrite(IA_A, LOW);
  digitalWrite(IB_A, LOW);
  digitalWrite(IA_B, LOW);
  digitalWrite(IB_B, LOW);
}

void setup() {
  Serial.begin(9600);

  pinMode(IA_A, OUTPUT);
  pinMode(IB_A, OUTPUT);
  pinMode(IA_B, OUTPUT);
  pinMode(IB_B, OUTPUT);
  pinMode(led_r,OUTPUT);
  pinMode(led_b, OUTPUT);


  stopMotors();
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    // Forward
    if (command == 'F') {
      digitalWrite(IA_A, HIGH);
      digitalWrite(IB_A, LOW);
      digitalWrite(IA_B, HIGH);
      digitalWrite(IB_B, LOW);
      digitalWrite(led_b, HIGH);
      digitalWrite(led_r, HIGH);
    }

    // Backward
    else if (command == 'B') {
      digitalWrite(IA_A, LOW);
      digitalWrite(IB_A, HIGH);
      digitalWrite(IA_B, LOW);
      digitalWrite(IB_B, HIGH);
      digitalWrite(led_b, LOW);
      digitalWrite(led_r, LOW);
    }

    // Left
    else if (command == 'L') {
      digitalWrite(IA_A, LOW);
      digitalWrite(IB_A, HIGH);
      digitalWrite(IA_B, HIGH);
      digitalWrite(IB_B, LOW);
      digitalWrite(led_r, HIGH);
      digitalWrite(led_b, LOW);

    }

    // Right
    else if (command == 'R') {
      digitalWrite(IA_A, HIGH);
      digitalWrite(IB_A, LOW);
      digitalWrite(IA_B, LOW);
      digitalWrite(IB_B, HIGH);
      digitalWrite(led_b, HIGH);
      digitalWrite(led_r, LOW);
    }

    // Stop
    else if (command == 'S') {
      digitalWrite(led_r, LOW);
      digitalWrite(led_b, LOW);
      stopMotors();
    }
  }
}
