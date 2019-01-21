# University Moot Competition Scoring Application
Moot competitions are a type of public-speaking competition that focus on legal debate and advocacy. In the undergraduate moot court circuit,
teams of two students face another pair in a mock-appellate court setting. The competition usually consists of one day of randomly-assigned
rounds, followed by a second day for the top-ranking teams.

Not every team will encounter every judge at the competition, and as such, a team's performance can depend on the difficulty with which
their judges evaluate them. The goal of this program is to standardize raw judge scores based on all scores given by that particular judge.
This will (roughly) eliminate the advantage of receiving only "easy" judges.

The normalization process described below was first implemented by Alex Marchi of McGill University.
As well, University of Toronto's Undergraduate Moot Court Team assisted by providing sample data and details.

## Running the program
The application requires 2 csv files, one with all participants' names, schools, teamIDs and competitorIDs,
and one with every score a participant received on the first day (with each row representing a different judge's score).
These csv's should be based off the two found in the TEMPLATES folder, and should follow the formats given by the [Templates_instruction textfile](https://github.com/cclin130/moot_scoring_app/blob/master/TEMPLATES/Template_instructions.txt).

To run the program, either run the moot_scorer_GUI.py file or download the moot_scorer executable contained in the following [zipped folder](https://drive.google.com/file/d/17DzAGimxlqDXLask1V-S3GJttERcTW-k/view?usp=sharing).
Running either will open the following application:

![alt text](https://github.com/cclin130/moot_scoring_app/blob/master/app_screenshot.png)

Once this app opens, input the full file path of the two csvs required (one with the team information and one with all the scores)
into the correct text boxes, as well as the file path of where you want the output csv's to be saved. Then, click the "Calculate final scores"
button.

The program will output the following three files:

- scores_full_[date].csv: the same csv as the one with all the scores with an additional column showing adjusted scores
- scores_individual_[date].csv: csv of each individuals' average scores (adjusted and non-adjusted), ordered by score
- scores_team_[date].csv: csv of each teams' average scores (adjusted and non-adjusted), ordered by score

## How the program works

![alt text](https://github.com/cclin130/moot_scoring_app/blob/master/program_overview.png)

Note that this model only works when judges' scores are in fact normally distributed.
For a competition that has four rounds, we will get 16 scores from each judge (for each round, a judge evaluates 4 participants).
We assume that 16 samples is sufficient to assume a normal distribution.

A more in-depth explanation of the normalization process can be found [here](https://github.com/cclin130/moot_scoring_app/blob/master/UofT_data/StatisticalCorrection.pdf)