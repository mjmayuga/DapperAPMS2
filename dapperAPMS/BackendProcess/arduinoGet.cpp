#include <iostream>
#include <SerialStream.h>  // This library might be different depending on your OS

using namespace std;
using namespace LibSerial;

int main() {
  SerialStream arduino("/dev/ttyUSB0", ios_base::out | ios_base::in);  // Open serial port
  arduino.SetBaudRate(SerialStreamBuf::BAUD_9600);  // Set baud rate

  if (!arduino.good()) {
    cerr << "Error opening serial port" << endl;
    return 1;
  }

  string line;
  while (true) {
    getline(arduino, line);  // Read line from Arduino
    cout << "Received: " << line << endl;
  }

  return 0;
}