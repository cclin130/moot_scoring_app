from tkinter import *
import pandas as pd
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
        .reset_index()
    df_judge_avgs.columns = ['judgeID', 'judge_avg']

    df_judge_stds = df_scores.groupby('judgeID')\
        .std()\
        .reset_index()
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
    # get individual rankings
    df_participant_scores = df_scores_new.groupby('competitorID').mean()\
        .reset_index() \
        .drop(['judge_avg', 'judge_std', 'score_zscore'], axis=1)

    # reformat individual rankings table, with participant names
    df_participant_scores_final = df_participant_scores.merge(df_teams, on='competitorID', how='left') \
        [['competitorID', 'competitor_name', 'competitor_school', 'score_raw', 'score_final']] \
        .sort_values('score_final', ascending=False)

    # get team rankings
    df_team_scores = df_scores_new.drop(['judge_avg', 'judge_std', 'score_zscore'], axis=1) \
        .merge(df_teams, on='competitorID', how='left') \
        .groupby('teamID').mean() \
        .reset_index()

    # reformat df_teams for easier merging later on
    df_teams2 = df_teams.drop_duplicates('teamID').merge(df_teams, on='teamID', how='left', suffixes=('_1', '_2'))
    df_teams2 = df_teams2.loc[df_teams2['competitorID_1'] != df_teams2['competitorID_2'], :] \
        .reset_index(drop=True)

    df_team_scores_final = \
    df_team_scores.merge(df_teams2, on='teamID', how='left').sort_values('score_final', ascending=False)\
        [['teamID', 'competitorID_1', 'competitor_name_1', 'competitorID_2', 'competitor_name_2',\
          'competitor_school', 'score_raw', 'score_final']]

    # output all dataframes to csv's
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d')

    df_scores_new.round(decimals=1).to_csv('{0}\scores_full_{1}.csv'.format(output_path, timestamp), index=False)
    df_participant_scores_final.round(decimals=1).to_csv('{0}\scores_individual_{1}.csv'.format(output_path, timestamp), index=False)
    df_team_scores_final.round(decimals=1).to_csv('{0}\scores_team_{1}.csv'.format(output_path, timestamp), index=False)


if __name__ == '__main__':
    #construct dinwo
    window = build_window()

    #display window to user
    window.mainloop()