# are-you-the-one-predictor

A program used to solve humanity's greatest questions in 2020 - how quickly can we deduce the most likely winning combinations of perfect matches from a ridiculous MTV reality show?

To use:
* Download the repo and ensure you have argparse and pandas installed via pip3.
* Copy the template folder in the resources sub-directory to a new directory of your choice.
* Add the relevant info to the three csv files that you'd like to view the combinations for.
  * names.csv contains the names and gender of each contestant.
  * truthBooths.csv contains the names of the two contestants that entered the truth booth, and whether or not they were a perfect match.
  * lights.csv contains the number of lights for a given matchup ceremony and each of the matches that were together at the ceremony.
* Run `python3 src/main.py {folder in resources}` to see the stats for the supplied info in the specified folder.
  * For example `python3 src/main.py season1` will run full analysis on the supplied info for the first season by looking in resources/season1.
