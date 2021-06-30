
import pandas as pd
import numpy as np
import random as rd

data = pd.read_csv("Data/EURO2020xG.csv")

G = input("Which group's results would you like to see?")

group_filter = data["Group"]
filter = group_filter == G
selected = data[filter]

# Recoding the Shot_by column
selected.loc[(selected.Shot_by == "A"), "Shot_by"] = selected.Team_A
selected.loc[(selected.Shot_by == "B"), "Shot_by"] = selected.Team_B

results = pd.DataFrame()
for i in range(0,100):
    df = selected
    df["Sim_ID"] = i+1
    for lab, row in df.iterrows():
        df.loc[lab, "Goal"] = rd.random() <= row["Chance"]/100 # Adding a new column for every shot to see if it is a goal or not
    results = results.append(df)

# Summarizing goals for every match
results["Goal"] = results["Goal"].astype(int) # Convert the column to integer
results2 = results.groupby(["Match_ID", "Shot_by", "Sim_ID"], as_index = False)
results2 = results2.Goal.agg(np.sum)

# Creating match specific ID
results2["Match_Sim_ID"] = results2["Match_ID"].astype(str) + "_" + results2["Sim_ID"].astype(str)


# Adding new columns for winning, losing and drawing
results2["Min_G"] = results2["Goal"].groupby(results2["Match_Sim_ID"]).transform("min")
results2["Max_G"] = results2["Goal"].groupby(results2["Match_Sim_ID"]).transform("max")
results2["Winner"] = results2.eval("Goal == Max_G and Goal > Min_G")
results2["Draw"] = results2.eval("Min_G == Max_G")
results2["Loser"] = results2.eval("Goal == Min_G and Goal < Max_G")

# Converting boolean values to points
results2.loc[(results2.Winner == True), "Winner"] = 3
results2.loc[(results2.Draw == True), "Draw"] = 1
results2.loc[(results2.Loser == True), "Loser"] = 0

results2["Points"] = results2["Winner"].astype(int) + results2["Draw"].astype(int)

final_results = results2.groupby(["Shot_by"], as_index = False)
final_results = final_results.Points.agg(np.mean)
final_results.columns = ["Country", "xP"]
print(final_results.sort_values(["xP"], ascending = False))