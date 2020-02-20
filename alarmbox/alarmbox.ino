/*
 * SD Card wiring
 * 
 * Original:
 * MOSI - 11
 * MISO - 12
 * CLK - 13
 * CS - 10
 * 
 * 
 * 
 * Button pin - 5
 * 
 * Speaker pin - 6
 * 
 * Ready LED  - 0
 * Running LED - 1
 * 
 * 
 * If random intervalls:
 * int minInterval = 2000; //minimum alarm interval 2 s.
 * int maxInterval = 10000; // maximum alar interval 10 s.
 * 
 */

#include <SPI.h>
#include <SD.h>



// *****************************************************************
int baud = 9600; //                                                *
// set alarm timing:                                               *
unsigned long a1 = 8000; // ms                                     *
unsigned long a2 = 105000; // ms                                     *
unsigned long a3 = 131000; // ms
unsigned long a4 = 169000;
unsigned long a5 = 235000;
unsigned long a6 = 290000;
unsigned long a7 = 347000;
unsigned long a8 = 389000;
unsigned long a9 = 417000;
unsigned long a10 = 581000;
const int nAlarms = 5; //                                          *
//define at what time the alarms shuld go off (ms after start):    *  
unsigned long netAlarmTiming[nAlarms] = {a1, a2, a3, a4, a5}; //           *
//actual alarm timing (netAlarmTiming + startTime offset)          *
unsigned long alarmTiming[nAlarms]; //                             *
// Automatically turn off alarm after timeout period:              *
int timeout = 3 * 1000; //                                        *
//                                                                 *
String filename = "logg.csv";
//******************************************************************
                                   

//**********************************
const int chipSelect = 10; // CS port SD-card adapter.

File logg;

unsigned long duration;
unsigned long performance[nAlarms]; //Needs to be of length number of alarams * 2
int i=0; // performance array index
unsigned long startTime; 

int n = nAlarms-1; // max alarm index
int buttonPin = 5;
int alarmPin = 6;
int readyPin = 4;
int runPin = 2;
//#####################################################################

bool start = 0;
int alarmState = 0;

void(*resetFunc)(void) = 0;

// ------------------- setup() -----------------------------------------
void setup(){

  i = 0;
  start = 0;
  randomSeed(123);
  pinMode(buttonPin, INPUT); // default should be LOW or 0
  pinMode(alarmPin, OUTPUT);
  pinMode(readyPin, OUTPUT);
  pinMode(runPin, OUTPUT);
  digitalWrite(readyPin, HIGH);
  digitalWrite(runPin, LOW);

  
  Serial.begin(baud);
  
  //setup the sd card:
  //Serial.println("Initializing SD card..");
  if(!SD.begin(10)){
    //Serial.println("Failed to initialize SD card..");
  }else{ //Writing column headers:
  
    // Start new line in logfile:
   logg = SD.open(filename, FILE_WRITE);
   if(!logg){
    //Serial.println("Failed to open loggfile for writing (newline");
   }else{
    logg.print("\n");
    logg.close();
   }
  }
  
  //Serial.print("Button state: "); Serial.println(digitalRead(buttonPin));
  //Serial.print("Millis = "); Serial.println(millis());
  //Serial.print(alarmTiming[0]);Serial.print(alarmTiming[1]); Serial.println(alarmTiming[2]);
 // Serial.println("Flip the switch to start the test");
  
}

// øøøøøøøøøøøøøøøøøøøøøøø main loop øøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøøø
void loop(){

  while(!start){
    if(digitalRead(buttonPin)==HIGH){
      //Serial.println("Test Started!");
      start = 1;
      startTime = millis();
      for(int j = 0; j<nAlarms; j++){
        alarmTiming[j] = startTime + netAlarmTiming[j];
      }// end for loop
      digitalWrite(readyPin, LOW); // turn off ready led
      digitalWrite(runPin, HIGH); // turn on running led
      //Serial.print(alarmTiming[0]);Serial.print(", ");Serial.print(alarmTiming[1]); Serial.print(", ");Serial.println(alarmTiming[2]);
      
    }// end if button
  }//while

  // if all alarms are triggered, test is done so do nothing. Else keep run test.
  if(i>n){
    //do nothing
   //Serial.println("Test done");
   //Serial.println("Restting...");

   
   delay(2000);
   resetFunc();
      
  }else{
    // Normal operation:
      // set off the alarm:
    if(millis()>=alarmTiming[i]){
      tone(alarmPin, 500);
      if(alarmState == 0){
        alarmState = 1;
        Serial.print("alarm");
      }
    }
    // Turn off alarm if not done by operator within timout period:
    if(millis()>(alarmTiming[i]+timeout)){
      Serial.print(timeout);
      noTone(alarmPin);
      alarmState = 0;
      //performance[i]=alarmTiming[i];
      performance[i] = timeout;
  
      //write the result to SD:
      logg = SD.open(filename, FILE_WRITE);
      if(!logg){
        //Serial.println("Failed to open loggfile (timeout)");
      }else{
        logg.print(netAlarmTiming[i]/1000); logg.print(","); logg.print(timeout);logg.print(",");
        logg.close();
      }
      i++;
      //Serial.println("Timeout period exceeded");
    }
  
    // Turn off the alarm and record reaction time if button is pushed:
    if(digitalRead(buttonPin)==HIGH && millis()>alarmTiming[i]){
      duration = millis()-alarmTiming[i];
      Serial.print(duration);
      noTone(alarmPin);
      alarmState = 0;
      performance[i]= duration; // reaction time
      //Serial.print("Alarm number: ");Serial.println(i+1);
      //Serial.println(alarmTiming[i]);
      //Serial.println(netAlarmTiming[i]);
      //Serial.println(performance[i]);
      
      
      //logging performance:
      logg = SD.open(filename, FILE_WRITE);
      if(!logg){
        //Serial.println("Failed to open logg file for writing.");
      }else{
        logg.print(netAlarmTiming[i]/1000);logg.print(",");logg.print(performance[i]); logg.print(",");
        logg.close();
      }
      
      i ++; //increment index of performance array
     
    } // end if buttonPin
  } //else "normal operation"

}// void loop
