PSUWxData
=========

This repo holds the code I used for the final project of METEO 498a at Penn State. 

Currently the program will scrape the PSU weather station website, parse the required information, and insert the data into a MySQL database. Currently the program only runs from 1 Jan 1896 to 31 March 2014, but may be modified to include later dates at some point. I can see an easy implementation where we use the current datetime to find the latest date, but that was outside the scope of the project.

The following 5 variables are collected by the program:
*  High Temperature in degrees Fahrenheit
*  Low Temperature in degrees Fahrenheit
*  Amount of Liquid Precipitation in inches
*  Amount of Solid Precipitation in inches
*  Snow Depth in inches

For this project, some code was adapted from drboyer's *[psusnowdepth](https://github.com/drboyer/psusnowdepth/)*.