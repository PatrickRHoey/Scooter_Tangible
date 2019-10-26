#include <ros.h>
#include <tangible_master/button_leds.h>

int ledArray[] = {0, 0, 0, 0, 0, 0};
int externalArray[] = {0, 0, 0};

void message_callback(const tangible_master::button_leds& recieve_message){
  //digitalWrite(13, HIGH-digitalRead(13));   // blink the led
  for(int i = 0; i < 6; i++){
    ledArray[i] = recieve_message.button[i];
  }
  for(int i = 0; i < 3; i++){
    externalArray[i] = recieve_message.leds[i];
  }
}

//Pin Declarations

//Drive control pin
const int relayControl = A3;

//Joystick potentiometer pins
const int upDownPin = A4;
const int leftRightPin = A5;

//Led Pins
const int ledWait = 0;
const int ledLaser = 1;
const int ledYes = 3;
const int ledNo = 5;
const int ledPick = 6;
const int ledPlace = 9;
const int ledBasket = 10;
const int ledDrive = 11;


//Storage array for all led commands
int ledCommand[] = {0, 0, 0, 0, 0, 0};

//LED Storage Array


//Button Pins
const int butYes = 2;
const int butNo = 4;
const int butPick = 7;
const int butPlace = 8;
const int butBasket = 12;
const int butDrive = 13;

//Storage array for all button statuses
//int butArray[] = {0, 0, 0, 0, 0, 0};
//tangible_master::button_leds butArray;

//Button Names, used when looping through all buttons for updates
int buttonNames[] = {ledYes, ledNo, ledPick, ledPlace, ledBasket, ledDrive};

//button fading
int brightness = 0;
int fadeAmount = 15;

//Storage array for joystick values, these are on a scale of 0-1023
int joyCommand[] = {0, 0};

//ROS STUFF AND THANGS

ros::NodeHandle nh;

tangible_master::button_leds send_message;

tangible_master::button_leds receive_message;

ros::Publisher talker("tangible_interface_send", &send_message);

ros::Subscriber<tangible_master::button_leds> sub("button_leds", &message_callback);

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(9600);

  delay(2000);

  // Led button init
  pinMode(ledYes, OUTPUT);
  pinMode(ledNo, OUTPUT);
  pinMode(ledPick, OUTPUT);
  pinMode(ledPlace, OUTPUT);
  pinMode(ledBasket, OUTPUT);
  pinMode(ledDrive, OUTPUT);
  pinMode(ledWait, OUTPUT);
  pinMode(ledLaser, OUTPUT);
  pinMode(relayControl, OUTPUT);

  pinMode(butYes, INPUT);
  pinMode(butNo, INPUT);
  pinMode(butPick, INPUT);
  pinMode(butPlace, INPUT);
  pinMode(butBasket, INPUT);
  pinMode(butDrive, INPUT);


  //ROS Setup
  nh.initNode();
  nh.advertise(talker);
  nh.subscribe(sub);

  //digitalWrite(ledWait, HIGH);
  //digitalWrite(ledLaser, HIGH);
  
}





void fadeButton(int led){
  analogWrite(led, brightness);

  brightness += fadeAmount;

  if(brightness <= 0 || brightness >= 255){
    fadeAmount = -fadeAmount;
  }
  
  delay(30);
}

void readButton(int butName){
  bool stat = digitalRead(butName);
  if (butName == butYes){
    send_message.button[0] = stat;
    
  } else if (butName == butNo){
    send_message.button[1] = stat;
 
  } else if (butName == butPick){
    send_message.button[2] = stat;

  } else if (butName == butPlace){
    send_message.button[3] = stat;
    
  } else if (butName == butBasket){
    send_message.button[4] = stat;
    
  } else if (butName == butDrive){
    send_message.button[5] = stat;
  }
}


void updateLEDArray(int ledArray[]){
    for(int i = 0; i < 6; i++){
      updateLED(ledArray[i], buttonNames[i]);
  }
}

void updateLED(int newButtonStatus, int pinNumber){
  if(newButtonStatus == 0){
    digitalWrite(pinNumber, LOW);
  } else if (newButtonStatus == 1){
    digitalWrite(pinNumber, HIGH);
  } else if (newButtonStatus == 2){
    fadeButton(pinNumber);
  } 
}

void updateJoystick(){
  send_message.joy[0] = analogRead(upDownPin);
  send_message.joy[1] = analogRead(leftRightPin);
  
}

void updateAllButtons(){
  
  readButton(butYes);
  readButton(butNo);
  readButton(butPick);
  readButton(butPlace);
  readButton(butBasket);
  readButton(butDrive);
}

void updateExternals(){
  if (externalArray[0] == 1){
    digitalWrite(ledWait, HIGH);
  } else {
    digitalWrite(ledWait, LOW);
  }

   if (externalArray[1] == 1){
    digitalWrite(ledLaser, HIGH);
  } else {
    digitalWrite(ledLaser, LOW);
  }

   if (externalArray[2] == 1){
    digitalWrite(relayControl, HIGH);
  } else {
    digitalWrite(relayControl, LOW);
  }
}

void loop() {
  /*
  fadeButton(ledYes);
  fadeButton(ledNo);
  fadeButton(ledPick);
  fadeButton(ledPlace);
  fadeButton(ledBasket);
  */
  updateLEDArray(ledArray);

  
  updateAllButtons();
  updateJoystick();
  updateExternals();
 
  //ROS Stuff
  talker.publish(&send_message);

  nh.spinOnce();
  
  delay(100);
}
