# screenruler

The windows 10 app was created from the Cross platform screen ruler using auto-py-to-exe. 

## Features

- **Reference Line**: Shows how far along ruler the mouse is at any point in time.
- **Rotatable**: Allows rotations of 90° so that ruler ticks are can be shown on bottom, left, top, or right side of ruler.
- **Supported Measurement**: Pixels, Points, Em, Inches, Millimeters, Picas
- **new**: Added transparency to app.
           Added scale calculation.

## How to run

Download the screenruler.exe file, then double click file from the parent directory.

## Commands
- **Left click and drag**: Drags the ruler around the screen
- **Right click**: Open a menu allowing you to rotate the ruler, or select a new measurement unit.

## Scale calculation
- **Select scale from the menu and input the scale factor. Place the ruler between item to be measured and 
    double click the end of length being measured to see calculation. 


## Build instructions

To build an executable from pyinstaller or auto-py-to-exe a few changes must be made.
first: Move the conversions.py module to the root directory of screenruler.py
second: If the default tk icon is going to be changed;
      Add correct path to script for app icon:
        ex.. self = Tk()
             self.iconbitmap(r'E:\screenruler\favicon.ico')
             ** self.iconbitmap(resource_path('favicon.ico')) To ensure correct packaging of binary the resource_path script must be used.
      Add to pyinstaller
             --add-binary "favicon.ico;."


