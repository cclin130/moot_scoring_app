from tkinter import *
import pandas as pd
import numpy as np
import datetime

def build_window():
    window = Tk()
    window.title("Moot Scoring App")
    window.geometry('500x190')

    #add two text boxes for user input
    lbl_teams_csv_path = Label(window, text="File path to teams csv: ")
    lbl_teams_csv_path.grid(column=0, row=0, padx=(10,0), pady=(20,10))
    txt_teams_csv_path = Entry(window, width=50)
    txt_teams_csv_path.grid(column=1, row=0, padx=(10,0), pady=(20,10))

    lbl_scores_csv_path = Label(window, text = "File path to scores csv: ")
    lbl_scores_csv_path.grid(column=0, row=1, padx=(10,0), pady=(10,10))
    txt_scores_csv_path = Entry(window, width=50)
    txt_scores_csv_path.grid(column=1, row=1, padx=(10,0), pady=(10,10))

    lbl_output_path = Label(window, text = "Output file path: ")
    lbl_output_path.grid(column=0, row=2, padx=(10,0), pady=(10,0))
    txt_output_path = Entry(window, width=50)
    txt_output_path.grid(column=1, row=2, padx=(10,0), pady=(10,0))

    btn = Button(window, text='Calculate final scores', \
                 command=(lambda: calculate_scores(txt_teams_csv_path.get(),\
                                                   txt_scores_csv_path.get(),\
                                                   txt_output_path.get())))
    btn.grid(column=1, row=3, pady=(20,0))

    return window

#method that is run when button clicked
def calculate_scores(teams_csv_path, scores_csv_path, output_path):
    print(teams_csv_path)
    print(scores_csv_path)
    print(output_path)

    df_teams = pd.read_csv(teams_csv_path)
    df_scores = pd.read_csv(scores_csv_path)

    #get each judge's avg and std scores
    df_judge_avgs = df_scores.groupby('judgeID')\
        .mean()\
        .reset_index()\
        .drop('competitorID', axis=1)
    df_judge_avgs.columns = ['judgeID', 'judge_avg']

    df_judge_stds = df_scores.groupby('judgeID')\
        .std()\
        .reset_index()\
        .drop('competitorID', axis=1)
    df_judge_stds.columns = ['judgeID', 'judge_std']

    #overall judge average and std
    avg_score = df_scores['score_raw'].mean()
    std_score = df_scores['score_raw'].std()

    #get z-score for each entry in df_scores
    df_scores_new = df_scores.merge(df_judge_avgs, on='judgeID', how='left')\
        .merge(df_judge_stds, on='judgeID', how='left')
    df_scores_new.loc[:, 'score_zscore'] = (df_scores_new.loc[:, 'score_raw']\
                                            - df_scores_new.loc[:,'judge_avg'])\
                                           /df_scores_new.loc[:,'judge_std']

    #calculate final scores
    df_scores_new.loc[:, 'score_final'] = (df_scores_new.loc[:, 'score_zscore']\
                                          *std_score) + avg_score

    #using transformed scores, get individual and team rankings


if __name__ == '__main__':
    #construct dinwo
    window = build_window()

    #display window to user
    window.mainloop()