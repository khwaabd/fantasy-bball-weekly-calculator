For my fantasy bbal team heres how to run this:

you have to use a terminal sorry

install git - look this up on your os, mac os should come with it

install python3 - again look up for your os.. you also might need to pip install yahoo sports modules, just run the scripts they will tell you whats missing

run this in terminal, this will clone this repo into a folder

      git clone https://github.com/khwaabd/fantasy-bball-weekly-calculator.git  
go into that folder

      cd fantasy-bball-weekly-calculator

to run a single week

    python3 main.py <week number> <year number>

week number is in the fantasy app, year number is the year the season started on so 2022 for 22'-23' season

To run multiple weeks, and output a summary of winners this outputs a file called <year>-week<week>.txt for each week

    ./multi-week-runner <start week> <end week> <year>

Season totals - this will print out all weeks of the season, and a summary of totals at the end - this does write files

    python3 season-totals.py <year number>

