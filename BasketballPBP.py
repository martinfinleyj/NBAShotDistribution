#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:19:45 2026

@author: finleymartin
"""

## IMPORTING PACKAGES ##


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.optimize import linprog
from scipy import stats


## PLAYER MAPPING ##


pbp_25 = pd.read_csv("pbp2025.csv")
player_data = pd.read_csv("PlayerIndex_nba_stats.csv")
rankings = pd.read_csv("nbarankings.csv")
player_map = player_data.loc[:, ["PERSON_ID", "PLAYER_LAST_NAME", "PLAYER_FIRST_NAME", "POSITION"]]
player_map = player_map.rename(columns={"PERSON_ID": "playerid"})

rankings["Player Name"] = rankings["Player Name"].str.split(",").str[0]

result = pd.merge(pbp_25, player_map, on = "playerid")
result["Player Name"] = result["PLAYER_FIRST_NAME"] + " " + result["PLAYER_LAST_NAME"]


## ADDING COLS TO SHOTS ##


shots = result.loc[:, ["playerid", "Player Name","team", "x", "y","dist", "type", "subtype", "desc", "POSITION"]]
shots = shots[shots["type"].isin(["Made Shot", "Missed Shot"])]

shots["made"] = (shots["type"] == "Made Shot").astype('int')
shots["three"] = np.where(shots["desc"].str.contains("3PT"), True, False)
shots["assisted"] = np.where(shots["desc"].str.contains("AST"), True, False)

shots['court_x'] = shots['x']/10 + 25
shots['court_y'] = shots['y']/10 + 5.25

area_rect = patches.Rectangle(
    (17, 0), 16, 19,
    fill=False,
    linewidth=2
) # creating boundary of paint

rx, ry = area_rect.get_xy()  # bottom-left corner coordinate
rw = area_rect.get_width()
rh = area_rect.get_height()

#  boundary check using court_x and court_y columns
in_x = (shots["court_x"] >= rx) & (shots["court_x"] <= rx + rw)
in_y = (shots["court_y"] >= ry) & (shots["court_y"] <= ry + rh)


shots["inside_paint"] = in_x & in_y
shots["midrange"] = (shots["inside_paint"] == False) & (shots["three"] == False)
shots["above_break_3"] = (shots["three"] == True) & (shots["court_y"] >= 14)
shots["corner_3"] = (shots["three"] == True) & (shots["court_y"] < 14)


## SHOT DF ORGANIZATION ##


shots = shots.groupby("Player Name").filter(lambda x: len(x) >= 0) # filtering for players with 500+ shot attempts
print(len(shots["Player Name"].unique()))

shots_ordered = shots.reindex(columns=["playerid", "Player Name","team", "POSITION","x", "y", "court_x", 
                                       "court_y", "dist", "three", "inside_paint",
                                       "midrange", "above_break_3", "corner_3", "assisted", "subtype", "desc","made"])

player = "Stephen Curry" # player for testings

shots_player = shots_ordered[shots_ordered["Player Name"] == player].copy()


## COURT GRAPH REPRESENATION ##


fig, ax = plt.subplots(figsize=(10,8))


sns.kdeplot(shots_player.loc[shots['made'] == 1], # heatmap
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

ax.set_aspect('equal')
plt.show()


## SHOT DISTRIBUTION ##


zone_cols = ["inside_paint", "midrange", "above_break_3", "corner_3"]

shots["shot_zone"] = shots[zone_cols].idxmax(axis=1)

pos_map = shots[["Player Name", "POSITION"]].drop_duplicates("Player Name")   # <<< ADD (moved up here, built from shots)

agg = (
    shots.groupby(["Player Name", "POSITION", "shot_zone"])
         .agg(shot_count=("shot_zone", "size"), makes=("made", "sum")) #creates columns shot_count which is size of shot_zone
)                                                                      #and makes which is sum of shots made in that zone

agg = agg.reset_index()

full = pd.MultiIndex.from_product(                                        # <<< ADD
    [pos_map["Player Name"], zone_cols], names=["Player Name", "shot_zone"]   # <<< ADD
).to_frame(index=False)                                                   # <<< ADD
agg = (                                                                   # <<< ADD
    full.merge(agg.drop(columns="POSITION"), on=["Player Name", "shot_zone"], how="left")   # <<< ADD
        .merge(pos_map, on="Player Name")                                 # <<< ADD
)                                                                         # <<< ADD
agg[["shot_count", "makes"]] = agg[["shot_count", "makes"]].fillna(0)     # <<< ADD

agg["shot_dist"] = agg["shot_count"] / agg.groupby("Player Name")["shot_count"].transform("sum")
agg["shot_percentage"] = agg["makes"] / agg["shot_count"]

zp = agg.groupby(["POSITION", "shot_zone"])[["makes", "shot_count"]].transform("sum")   # <<< ADD
agg["shot_percentage"] = agg["shot_percentage"].fillna(zp["makes"] / zp["shot_count"]) # <<< ADD

zone_points = {
    "inside_paint": 2,
    "midrange": 2,
    "above_break_3": 3,
    "corner_3": 3,
}

agg["E(p)"] = agg["shot_percentage"] * agg["shot_zone"].map(zone_points) #maps points to each zone type
agg["cE(p)"] = agg["shot_percentage"] * agg["shot_zone"].map(zone_points) * agg["shot_dist"]#maps points to each zone type

agg = agg.loc[:, ["Player Name", "POSITION", "shot_zone", "shot_dist", "shot_count", "shot_percentage", "E(p)", "cE(p)"]]

# create df of each position, each shot type and boundaries of 10 percentile and 90 percentile of shot distribution

pos_df = (
    agg.groupby(["POSITION", "shot_zone"]).agg(league_low_dist=("shot_dist", lambda x: np.percentile(x, 10)),
                                               league_high_dist=("shot_dist", lambda x: np.percentile(x, 90)))
    ).reset_index()

player_dist = pd.merge(agg, pos_df, on=["POSITION", "shot_zone"])
player_dist = player_dist.sort_values("Player Name")
player_dist = player_dist.reset_index(drop=True)


## OPTIMIZATION FRAMEWORK ##


rows = []
for player, g in player_dist.groupby("Player Name"):
    
    g = g.set_index("shot_zone").loc[zone_cols]
    
    c = -g["E(p)"].to_numpy() 
    
    bounds = list(zip(g["league_low_dist"], g["league_high_dist"]))
    
    res = linprog(c, A_eq=[[1, 1, 1, 1]], b_eq=[1], bounds=bounds, method="highs")
    
    rows.append(pd.DataFrame({
        "Player Name": player,
        "shot_zone": zone_cols,
        "optimized_shot_dist": res.x if res.success else np.nan,
    }))
    
opt = pd.concat(rows, ignore_index=True)
player_dist = pd.merge(player_dist, opt, on=["Player Name", "shot_zone"])
player_dist["pE(p)"] = player_dist["shot_percentage"] * player_dist["optimized_shot_dist"] * player_dist["shot_zone"].map(zone_points)

player_dist["gain"] = player_dist["pE(p)"] - player_dist["cE(p)"]

player = player_dist.groupby(["Player Name", "POSITION"]).agg(Ep = ("cE(p)", "sum"), 
                                                              pEp = ("pE(p)", "sum"), 
                                                              gain = ("gain", "sum"),
                                                              shot_count = ("shot_count", "sum"),
                                                              avg_per = ("shot_percentage", "mean"))
player["gain"] = player["gain"] * 100
player = player.reset_index()
player_50 = pd.merge(player, rankings[["Player Name", "Rank", "ESPN POINTS"]], on = "Player Name")

# a negative gain means the player's percentile for shot distribution is outside of the 10, 90 AKA elite players


fig, ax = plt.subplots(figsize=(10,15))

plt.axis('on')

p = player[player["Player Name"].isin(["Stephen Curry", "LeBron James", "James Harden", "Isaiah Stevens", "Bol Bol"])]

player_50 = player_50.sort_values("gain").reset_index(drop=True)

y = np.arange(len(player_50))

for i in range(len(player_50)):
    plt.plot(
        [(player_50.loc[i, "Ep"] *100),
         (player_50.loc[i, "pEp"] * 100)],
        [i, i],
        color = "Blue"
    )

# Current values
plt.scatter(
    player_50["Ep"]*100,
    y,
    label="Current",
    color = "Red"
)

# Optimized values
plt.scatter(
    player_50["pEp"]*100,
    y,
    label="Optimized",
    color="Purple"
)

plt.yticks(y, player_50["Player Name"])


fig, ax = plt.subplots(figsize=(10,8))


ax.scatter(
    player["shot_count"],
    player["gain"],
    alpha=1,
    s=10,
    color = 'green',
    marker = 'x'
)

ax.set_ylim(-1, 120)
ax.set_xlim(-10, 2200)


r_coef, p_value = stats.pearsonr(player["shot_count"], player["gain"])
print(f"Pearson r: {r_coef:.4f}, p-value: {p_value:.4f}")