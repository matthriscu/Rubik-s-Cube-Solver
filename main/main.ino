#include "Stepper.h"
#include <array>
using namespace std;

const int stepsPerRevolution = 2048, speed = 8;

enum Side {
  B, L, R, D, F, U, UNDEFINED
};

Side fromChar(char c) {
  switch (c) {
    case 'B':
      return B;
    case 'L':
      return L;
    cazse 'R':
      return R;
    case 'F':
      return F;
    case 'D':
      return D;
    case 'U':
      return U;
    default:
      return UNDEFINED;
  }
}

array<Stepper, 5> steppers {
  Stepper(stepsPerRevolution, 32, 25, 33, 26),
  Stepper(stepsPerRevolution, 27, 12, 14, 13),
  Stepper(stepsPerRevolution, 23, 1, 22, 21),
  Stepper(stepsPerRevolution, 19, 5, 18, 17),
  Stepper(stepsPerRevolution, 16, 2, 4, 15)
};

void move(char buf[]) {
  if (buf[0] == 'U') {
    buf[0] = 'D';

    // move("R1");
    // move("L1");
    // move("F2");
    // move("B2");
    // move("R3");
    // move("L3");

    steppers[R].step(stepsPerRevolution / 4);
    steppers[L].step(stepsPerRevolution / 4);
    steppers[F].step(stepsPerRevolution / 2);
    steppers[B].step(stepsPerRevolution / 2);
    steppers[R].step(-stepsPerRevolution / 4);
    steppers[L].step(-stepsPerRevolution / 4);
    
    move(buf);

    // move("R1");
    // move("L1");
    // move("F2");
    // move("B2");
    // move("R3");
    // move("L3");

    steppers[R].step(stepsPerRevolution / 4);
    steppers[L].step(stepsPerRevolution / 4);
    steppers[F].step(stepsPerRevolution / 2);
    steppers[B].step(stepsPerRevolution / 2);
    steppers[R].step(-stepsPerRevolution / 4);
    steppers[L].step(-stepsPerRevolution / 4);

    return;
  }

  Side side = fromChar(buf[0]);

  if (buf[1] == '1')
    steppers[side].step(stepsPerRevolution / 4);
  else if (buf[1] == '2')
    steppers[side].step(stepsPerRevolution / 2);
  else if (buf[1] == '3')
    steppers[side].step(-stepsPerRevolution / 4);
}

void setup() {
  Serial.begin(115200);

  for (Stepper &stepper : steppers)
    stepper.setSpeed(speed);
}

void loop() {
  static char buf[2];

  if (Serial.available()) {
    buf[0] = Serial.read();
    buf[1] = Serial.read();
    move(buf);
  }
}