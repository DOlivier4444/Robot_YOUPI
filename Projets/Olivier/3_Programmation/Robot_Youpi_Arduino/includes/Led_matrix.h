#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;

//  https://ledmatrix-editor.arduino.cc/
//  https://docs.arduino.cc/tutorials/uno-r4-wifi/led-matrix/

void matrix_robot_pick_place() {

  matrix.begin();

  uint32_t robotPickPlaceAnimation[][4] = {
	  {
	  	0x0,
	  	0x1e0200,
	  	0x400400e4,
	  	500
	  },
	  {
	  	0x0,
	  	0x180240,
	  	0x420400e4,
	  	500
	  },
	  {
	  	0x0,
	  	0x180240,
	  	0x440400e4,
	  	150
	  },
	  {
	  	0x0,
	  	0x100280,
	  	0x440440e4,
	  	150
	  },
	  {
	  	0x0,
	  	0x300,
	  	0x480440e4,
	  	150
	  },
	  {
	  	0x0,
	  	0x100280,
	  	0x440440e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x180240,
	  	0x440400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x180240,
	  	0x420400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x1e0200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x200,
	  	0x40180200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x400,
	  	0x40180200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x800800,
	  	0x80100200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x1001001,
	  	0x100200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x2002002,
	  	0x200200,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x4004004,
	  	0x400400,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x8008008,
	  	0x800800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x10010010,
	  	0x1000800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x20020020,
	  	0x1000800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x40040,
	  	0x3000800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x80040,
	  	0x3000800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0xf000800,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x3004808,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x3004804,
	  	0x400400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x1002804,
	  	0x404400e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x1802,
	  	0x404404e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x1002804,
	  	0x404404e0,
	  	150
	  },
	  {
	  	0x0,
	  	0x3004804,
	  	0x400404e0,
	  	150
	  }
  };

  int frameDurations = 100;

  int numFrames = sizeof(robotPickPlaceAnimation) / sizeof(robotPickPlaceAnimation[0]);
  for (int i = 0; i < numFrames; i++) {
    matrix.loadFrame(robotPickPlaceAnimation[i]);
    delay(frameDurations);
  }
}

void matrix_youpi_blinking() {

  matrix.begin();

  uint32_t youpiBlinking[][4] = {
    // YOUPI
  	{
  		0x00,
  		0x00,
  		0x00,
  		150
  	},
		{
  		0xa4aaaa4a,
  		0xa44e3902,
  		0x90390210,
  		150
  	},
  	{
  		0x00,
  		0x00,
  		0x00,
  		150
  	},
  	{
  		0xa4aaaa4a,
  		0xa44e3902,
  		0x90390210,
  		150
  	},
  	{
  		0x00,
  		0x00,
  		0x00,
  		150
  	},
  	{
  		0xa4aaaa4a,
  		0xa44e3902,
  		0x90390210,
  		150
  	},
  	{
  		0x00,
  		0x00,
  		0x00,
  		150
  	},
  	{
  		0xa4aaaa4a,
  		0xa44e3902,
  		0x90390210,
  		150
  	}
  };

  int frameDurations = 250;

  int numFrames = sizeof(youpiBlinking) / sizeof(youpiBlinking[0]);
  for (int i = 0; i < numFrames; i++) {
    matrix.loadFrame(youpiBlinking[i]);
    delay(frameDurations);
  }
}

