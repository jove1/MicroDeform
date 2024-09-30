#include <DueTimer.h>

#define Serial Serial

const int STEP = 2;
const int DIR = 3;
const int EN = 4;
const int M1 = 5;
const int M2 = 6;
const int LIM1 = 7;
const int LIM2 = 8;
const int LED = 13;

volatile int pos = 0;
int target = 0;
int vel = 50;

void do_cmd(String cmd) {
  cmd.trim();

  if (cmd.startsWith("rel ")) {
    target = pos + cmd.substring(4).toInt();
  
  } else if (cmd.startsWith("abs ")) {
    target = cmd.substring(4).toInt();

  } else if (cmd.startsWith("vel ")) {
    vel = cmd.substring(4).toInt();
  
  } else if (cmd.startsWith("ustep ")) {
    int val = cmd.substring(6).toInt();
    digitalWrite(M1, val & 1);
    digitalWrite(M2, val & 2);
  }
  if (cmd.endsWith("?") ){  
    String msg = String("pos ") + pos + " target " + target + " vel " + vel + " lim1 " + noisyRead(LIM1) + " lim2 " + noisyRead(LIM2);
    Serial.println(msg);
  }
}

inline int noisyRead(int pin) {
  return digitalRead(pin) + digitalRead(pin) + digitalRead(pin) > 1; 
}

inline void pulse_step() {
  digitalWrite(STEP, HIGH);
  delayMicroseconds(100); // min 30us
  digitalWrite(STEP, LOW);
}

int next = 0;

void make_step(){
  if (next) {
    next--;
    return;
  }
  next = 1000/vel; 

  digitalWrite(LED, !digitalRead(LED)); // blink

  if (pos > target) {
    if (noisyRead(LIM1)) { target = pos = 0; return; }
    if (digitalRead(EN) != HIGH) { digitalWrite(EN, HIGH); return; }
    if (digitalRead(DIR) != LOW) { digitalWrite(DIR, LOW); return; }
    pulse_step();
    pos -= 1;

  } else if (pos < target) {
    if (noisyRead(LIM2)) { target = pos; return; }
    if (digitalRead(EN) != HIGH) { digitalWrite(EN, HIGH); return; }
    if (digitalRead(DIR) != HIGH) { digitalWrite(DIR, HIGH); return; }
    pulse_step();
    pos += 1;
  
  } else {
    digitalWrite(EN, LOW);
  }
}

void setup() {
  pinMode(STEP, OUTPUT); 
  pinMode(EN, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(LED, OUTPUT);
  
  pinMode(LIM1, INPUT_PULLUP);
  pinMode(LIM2, INPUT_PULLUP);

  digitalWrite(STEP, LOW);
  digitalWrite(EN, LOW);
  digitalWrite(DIR, LOW);
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);

  Serial.begin(115200);
  Timer3.attachInterrupt(make_step).setFrequency(1000).start();
}

String cmd = "";
void loop() {  
  while (Serial.available()) {
    char ch = Serial.read();
    cmd += ch;
    if (ch == '\n') {
        do_cmd(cmd);
        cmd = "";
    }
  }
}

