#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:19:45 2026

@author: finleymartin
"""

#must input player name in Playerdata:mapping.py first

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# mapping player names in "pbp2025.csv" to full names
pbp_25 = pd.read_csv("pbp2025.csv")
player_map = pd.read_csv("PlayerIndex_nba_stats.csv")
player_map = player_map.loc[:, ["PERSON_ID", "PLAYER_LAST_NAME", "PLAYER_FIRST_NAME"]]
player_map = player_map.rename(columns={"PERSON_ID": "playerid"})

result = pd.merge(pbp_25, player_map, on = "playerid")
result["Player Name"] = result["PLAYER_FIRST_NAME"] + " " + result["PLAYER_LAST_NAME"]

# clean data and filter by actual shots
shots = result.loc[:, ["playerid", "Player Name","x", "y","dist", "type", "subtype", "desc"]]
shots = shots[shots["type"].isin(["Made Shot", "Missed Shot"])]

# specify 3pt shots
shots["made"] = (shots["type"] == "Made Shot").astype('int')
shots["3PT"] = np.where(shots["desc"].str.contains("3PT"), True, False)

shots['court_x'] = shots['x']/10 + 25
shots['court_y'] = shots['y']/10 + 5.25

area_rect = patches.Rectangle(
    (17, 0), 16, 19,
    fill=False,
    linewidth=2
)

rx, ry = area_rect.get_xy()  # Bottom-left corner coordinate
rw = area_rect.get_width()
rh = area_rect.get_height()

# 3. Vectorized boundary check using your DataFrame columns
in_x = (shots["court_x"] >= rx) & (shots["court_x"] <= rx + rw)
in_y = (shots["court_y"] >= ry) & (shots["court_y"] <= ry + rh)


# 4. Save the true/false mask to your DataFrame
shots["inside_paint"] = in_x & in_y
paint_total = len(shots[shots['inside_paint'] == True])
paint_made = len(shots[(shots['made'] == 1) & (shots["inside_paint"] == True)])
paint_percent_league = round((paint_made / paint_total) * 100, 1)

three_total = len(shots[shots['3PT'] == 1])
three_made = len(shots[(shots['made'] == 1) & (shots["3PT"] == True)])
three_pct_league = round((three_made / three_total) * 100, 1)

shots["midrange"] = (shots["inside_paint"] == False) & (shots["3PT"] == 0)

mid_total = len(shots[shots['midrange'] == True])
mid_made = len(shots[(shots['made'] == 1) & (shots["midrange"] == True)])
mid_pct_league = round((mid_made / mid_total) * 100, 1)

shots_ordered = shots.reindex(columns=["playerid", "Player Name", "x", "y", "court_x", 
                                       "court_y", "dist", "3PT", "inside_paint",
                                       "midrange", "subtype", "desc","made"])

shots_player = shots_ordered[shots_ordered["Player Name"] == "Stephen Curry"].copy()




fig, ax = plt.subplots(figsize=(10,8))


sns.kdeplot(shots_player.loc[shots['made'] == 1],
            x = 'court_x',
            y = 'court_y',
            fill = True,
            cmap = "Reds",
            levels = 8)


ax.scatter(
    shots_player.loc[shots['made'] == 1, "court_x"],
    shots_player.loc[shots['made'] == 1, "court_y"],
    alpha=1,
    s=20,
    color = 'green',
    marker = 'o'
)

ax.scatter(
    shots_player.loc[shots['made'] == 0, "court_x"],
    shots_player.loc[shots['made'] == 0, "court_y"],
    alpha=0.5,
    s=20,
    color = 'red',
    marker = 'x'
)

#half court size
ax.add_patch(
    patches.Rectangle(
        (0, 0), 50, 47,
        fill=False,
        linewidth=2
    )
)

#right line
ax.add_patch(
    patches.Rectangle(
        (47, 0), 0, 14,
        fill=False,
        linewidth=2
    )
)

#backboard
ax.add_patch(
    patches.Rectangle(
        (22, 3.7), 6, 0,
        fill=False,
        linewidth=2
    )
)

#left line
ax.add_patch(
    patches.Rectangle(
        (3, 0), 0, 14,
        fill=False,
        linewidth=2
    )
)

#arc
ax.add_patch(
    patches.Arc(
        (25, 5.25), width = 47.3, height = 47.3,
        fill=False,
        linewidth=2,
        theta1 = 21.5,
        theta2 = 158.5
    )
)


#paint
ax.add_patch(
    area_rect
)

#midcourt circle
ax.add_patch(
    patches.Circle(
        (25, 47), 6,
        fill=False,
        linewidth=2
    )
)

#hoop
ax.add_patch(
    patches.Circle(
        (25, 5.25), 1.5,
        fill=False,
        linewidth=2
    )
)

#line left 2
ax.add_patch(
    patches.Rectangle(
        (0, 28), 3, 0, 
        fill=False,
        linewidth=2
    )
)

#line right 2
ax.add_patch(
    patches.Rectangle(
        (47, 28), 50, 0, 
        fill=False,
        linewidth=2
    )
)

#midcourt circle
ax.add_patch(
    patches.Circle(
        (25, 19), 6,
        fill=False,
        linewidth=2
    )
)


ax.set_xlim(0, 50)
ax.set_ylim(0, 47)



plt.title("Stephen Curry 2024-2025 Shot Distribution", loc = 'center')
plt.axis('off')

# 2 shot percent made within an area made


plt.text(25, 8, f"PAINT {paint_percent_league}% | {paint_made}/{paint_total}", backgroundcolor = "black", color = "white")
plt.text(36, 30, f"THREE {three_pct_league}% | {three_made}/{three_total}", backgroundcolor = "black", color = "white")
plt.text(5, 15, f"MIDRANGE {mid_pct_league}% | {mid_made}/{mid_total}", backgroundcolor = "black", color = "white")
ax.set_aspect('equal')
plt.show()

train_df = shots_ordered[shots_ordered["Player Name"] != "Stephen Curry"]

features = ["court_x",
              "court_y",
              "dist",
              "3PT",
              "inside_paint",
              "midrange",
              "subtype"]

X = train_df[features]
X = pd.get_dummies(X, columns=['subtype'], dtype=int).copy()
X_curry = shots_player[features]
X_curry = pd.get_dummies(X_curry, columns=['subtype'], dtype=int).copy()

y = train_df["made"]

X_curry = X_curry.reindex(columns=X.columns, fill_value=0)


model = LogisticRegression(max_iter = 1000)
model.fit(X, y)

shots_player["expected_prob"] = model.predict_proba(X_curry)[:, 1]

expected_meanpct = shots_player["expected_prob"].mean()
print(expected_meanpct)

# since curry shot 40.8% from the field 24-25, that means that curry shoots 4% 
# above the field compared to the predicted percentage