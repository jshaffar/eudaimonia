# eudaimonia

This graphs your overall happiness among other things. Please note this README is likely very confusing. I have not finished adding all functionality, and am frequently changing things, so I will likely create better documentation when I am finished. 

## Purpose:
Eudaimonia is how Aristotle described the purpose of humans. It losely translates to something happiness, but not in a short term, implusive way. Rather it is closer to the word flourishing. Obviosuly this cannot be measured objectively "I gained 20 eudamonia units today!!!!" , but I think having a good measure of how your life is going is not a terrible idea. It also helps to put in perspective when I am having a bad day that it could get better.  This is something I started a while ago as a spreadsheet program, and have recently decided to make a python program to enable more features than can be easily supported by libreoffice spreadsheets. After several years it is very cool to see how you were feeling during individual days, weeks, months, and years. Plus visualizations are also very cool!! And I am able to remember what specific days certain things happen!

## Usage:

You first need to get a google spreasheet online with a public link. Put the end of the url in a file called "spreadsheet_url.txt", in the main folder of this repo. You can then run
```shell
python spreadsheet.py
```
This should obtain the spreasheet from google drive and put it in a csv file called pursuit.csv

### Graphing:
"python graph.py": graphs data. See options with "python graph.py -h". 
Type dates in the american format "2/28/2023"

### Calc:
"python calc.py -c command"
This will differ for each condition, and might take some experimentation.
One example is the exists condition. I have a column called "Media" in my spreadsheet. 
"python calc.py -c exists -at Media"
Trait is already in df, no need to add it
The most consecutive rows with the condition exists is 12. This was from 2020-09-04 to 2020-09-15

### Examples:
Graphing total happiness during 2021
```shell
python graph.py -sd 1/1/2021 -ed 1/1/2022
```
![image](Graphs/Total-from_2021-01-01 00:00:00-to_2022-01-01 00:00:00.png)



