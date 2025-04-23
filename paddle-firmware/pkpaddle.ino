#include <DacTone.h>
#include <pitches.h>

DacTone audio;

int paddle_dit = 15;
int paddle_dash = 4;

int touch_threshold = 50;

int time_unit = 85;

int dit_duration = time_unit;
int dit_spacing = dit_duration+time_unit;

int dash_duration = 3*time_unit;
int dash_spacing = dash_duration+time_unit;

bool value = 0;
bool last_value = 0;

int dit_timer = 0;
int dash_timer = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("PKPaddle");
  audio.setVolume(100);
}

void loop() {
  if (touchRead(paddle_dash) < touch_threshold && !dit_timer) {
    if (dash_timer+dash_duration < millis()) {
      value = 0;
      if (dash_timer+dash_spacing < millis()) {
        dash_timer = millis();
      }
    } else {
      value = 1;
    }
  } else {
    if (dash_timer+dash_duration < millis() && dash_timer) {
      value = 0;
      if (dash_timer+dash_spacing < millis()) {
        dash_timer = 0;  
      }
    }
  } 
  if (touchRead(paddle_dit) < touch_threshold && !dash_timer) {
    if (dit_timer+dit_duration < millis()) {
      value = 0;
      if (dit_timer+dit_spacing < millis()) {
        dit_timer = millis();
      }
    } else {
      value = 1;
    }
  } else {
    if (dit_timer+dit_duration < millis() && dit_timer) {
      value = 0;  
      if (dit_timer+dit_spacing < millis()) {
        dit_timer = 0;  
      }
    }
  }
  if (!dash_timer && !dit_timer) {
    value = 0;
  }
  if (value != last_value) {
    if (value) {
      audio.tone(); // turn on 523Hz sine wave
      Serial.println(value);
      delay(5);
    } else {
      audio.noTone(); // now turn off audio
      Serial.println(value);
      delay(5);
    }
    last_value = value;
  }
}