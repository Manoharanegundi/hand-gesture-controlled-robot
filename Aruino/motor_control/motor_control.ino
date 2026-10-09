// Hand Gesture Controlled Robot
// 2WD Robot - Arduino UNO
// Commands received through Serial:
// F = Forward
// B = Backward
// L = Left
// R = Right
// S = Stop

// Motor A
#define ENA 5
#define IN1 8
#define IN2 9

// Motor B
#define ENB 6
#define IN3 10
#define IN4 11

int motorSpeed = 180;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(9600);

  stopRobot();

  Serial.println("Robot ready!");
}

void loop() {

  if (Serial.available() > 0) {

    char command = Serial.read();

    if (command == 'F') {
      forward();
    }

    else if (command == 'B') {
      backward();
    }

    else if (command == 'L') {
      left();
    }

    else if (command == 'R') {
      right();
    }

    else if (command == 'S') {
      stopRobot();
    }
  }
}

// ---------- MOVEMENT FUNCTIONS ----------

void forward() {
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left() {
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  // Left motor backward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  // Right motor forward
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void right() {
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  // Left motor forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  // Right motor backward
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopRobot() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}