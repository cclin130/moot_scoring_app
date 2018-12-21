# University Moot Competition Scoring Application
Moot competitions are a type of public-speaking competition that focuses on legal debate and advocacy. In the undergraduate moot court circuit,
teams of two students face another pair in a mock-appellate court setting. The competition usually consists of one day of randomly-assigned
rounds, followed by a second day for the top-ranking teams.

Not every team will encounter every judge at the competition, and as such, a team's performance can depend on the difficulty with which
their judges evaluate them. The goal of this program is to standardize raw judge scores based on all scores given by that particular judge.
This will (roughly) eliminate the advantage of receiving only "easy" judges.

The normalization process described below was first implemented by Alex Marchi of McGill University.
As well, University of Toronto's Undergraduate Moot Court Team assisted by providing sample data and details.

# How the program works

![alt text](https://github.com/cclin130/moot_scoring_app/blob/master/program_overview.png)

Note that this model only works when judges' scores are in fact normally distributed.
For a competition that has four rounds, we will get 16 scores from each judge (for each round, a judge evaluates 4 participants).
We assume that 16 samples is sufficient to assume a normal distribution.

A more in-depth explanation of the normalization process can be found [here](https://github.com/cclin130/moot_scoring_app/blob/master/UofT_data/StatisticalCorrection.pdf)