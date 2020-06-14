# ELV-GUI

The purpose of this program is to easily visualize the liquid-vapor equilibrium of a binary system 

## Main libraries used

- PyQt5: create the GUI;
- pyqtgraph;
- thermo: Calculate the activit constants and provide some themodinamic's data;
- sqlite3;
- Numpy;
- Pandas.

## Models

UNIFAC - https://en.wikipedia.org/wiki/UNIFAC;

Raoult's law - https://en.wikipedia.org/wiki/Raoult%27s_law;

Antoine's equation - https://en.wikipedia.org/wiki/Antoine_equation#:~:text=The%20Antoine%20equation%20is%20a,Antoine%20(1825%E2%80%931897).;

## Layout
### Main windows
![layout - ELV-GUI](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/Layout.PNG)

## How program working

### 1 - First:
The user select the substances of binary system in the combo box:

![Combobox](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/substances.PNG)

### 2 - Selection the system situation

In Radio buttom selection the system condition:

![Radiobuttom](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/Radiobutton.PNG)

The selection will inform you what the information will you need to give

### 3 - Inform the Pressure or Temperature of the sistem

![Data](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/Data.PNG)

This program work with Temperature in Kelvin and Pressure in bar.

### 4 - Plot the graphs and save the data

With all data, you can plot the graphics pressing the buttom 'Plot' and the graph will plot in two figures in program.
The fist figure will show the gas composition to liquid composition and the second will show the relation between the 
temperature or pressure and composition of system.

![Data](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/button.PNG)

#### Example
![Example](https://github.com/dcbarros1/ELV-GUI/blob/master/Img/plots.PNG)

if all correct, you can save data of this simulation em .xlsx data in tools button  





