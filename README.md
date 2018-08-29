# Guide to install and run Solar Panel Analyzer (SPA) - Beta Version 1.2 (SE-PROJECT-46)

## Getting Started

These instructions will get you a way to install and run SPA in your computer.

SPA works in Linux (Ubuntu 16.04.5 LTS (Xenial Xerus) and later) and Windows (Windows 7 and later) environment.
Nevertheless SPA was developed in Windows 7, then some functionalities in Ubuntu could be a little different than expected.
Best running of SPA is in Windows 7.

During development phase in older versions of Ubuntu, some difficulties about installing Python3 (using apt-get) and other needed libraries have been found.
For this reason, this guide describes how to install SPA in Ubuntu 16.04.5 LTS (Xenial Xerus).

## Installing in Ubuntu 16.04.5 LTS (Xenial Xerus)

Instructions to install needed libraries in Ubuntu 16.04.5 LTS (terminal commands).
Commands and procedure could be different for other versions of Ubuntu and Windows.

### 1) Install Python3

 Update apt-get

> sudo apt-get update

Check version of python3

> python3 -V


If no version is installed, then install python3

> sudo apt-get install python3.6

Upgrade python3

> sudo apt-get upgrade python3

### 2) Install OpenCV

Install pip3 (pip for python3)

> sudo apt-get install -y python3-pip

Check pip3 installing

> pip3 -V

Install opencv

> sudo apt-get install libopencv-dev python-opencv

Upgrade opencv

> sudo pip3 install opencv-python

### 3) Install other libraries

Install wxPython (GUI libraries).
WX has been recently updated, then few used funcionts in SPA are deprecated now (e.g. cursor changings)

> sudo pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

Install libraries needed to mathematical calculations etc.

> sudo pip3 install numpy scipy matplotlib

Install tiff support libraries

> sudo apt-get install python-tifffile

Developing and testing SPA, tifffile libraries gave some problems. To solve this, an other tifffile module was directly added in SPA package.

## Running

Only after above instructions, SPA can be executed only by CLI (Command Line Interface).
There are 2 different modes of running: using GUI and directly from Terminal.

### 1) Using GUI

Open the Terminal and move to SPA folder.
To run SPA, you have to digit he following command:

> python3 main.py

Executing this command, SPA interface will be opened.

### 2) By Terminal

SPA could be run directly from Terminal moving to SPA folder and using following command:

> python3 main_cmd.py PARAMETERS

In this case, SPA needs some parameters.
If you execute SPA without PARAMETERS, it shows you which data and in what order it needs.

### Dataset

SPA needs particular images in input (as showsn in URD and DRS documents).
They can found directly in SPA folder (dataset).
Press **'Help'** in SPA for more info.

## Author

***Jacopo De Luca*** <br />
***Corso di Software Engineering*** <br />
***Corso di Laurea Magistrale in Ingegneria Informatica - DIBRIS*** <br />
***Università degli Studi di Genova***
