# screenruler
Cross platform screen ruler using tkinter. 

![Picture of program running](https://github.com/LimestoneBob/screenruler/blob/master/ruler.png)


## Features

- **Reference Line**: Shows how far along ruler the mouse is at any point in time.
- **Rotatable**: Allows rotations of 90° so that ruler ticks are can be shown on bottom, left, top, or right side of ruler.
- **Supported Measurement**: Pixels, Points, Em, Inches, Millimeters, Picas
- **Transparency**: <sup>new</sup> Gives the ability to see images under ruler app  _(Windows .exe file only)_
- **Scale factor**: <sup>new</sup> Apply a factor when measuring items that use a scaled ratio. _(Windows .exe file only)_


## How to run

### Method 1:
Download the repo, then from the parent directory run `python3 -m screenruler.main`

### Method 2:
For Windows 10, Download screenruler.exe from Releases and then double click file. The App will run and no installation needed. The first time
the app is run Windows will show "unknown publisher" warning as the app doesn't have a code signing certificate. You will need to select more info and run anyway to use application.


## Commands
- **Left click and drag**: Drags the ruler around the screen
- **Right click**: Open a menu allowing you to rotate the ruler, or select a new measurement unit.

## How to use
- **Scale factor**: 
Select scale from the menu and input the scale factor. Place the ruler between item to be measured and double click the end of length being measured to see calculation. 

    Calculate the scale factor: Using the ruler, measure a known distance of length on screen in pixels. Calculate the factor by dividing the known measurement value by the pixel number and input the result in the scale factor field. After the scale factor has been entered, double clicking on ruler at any point will give the length in desired unit of measure. 



