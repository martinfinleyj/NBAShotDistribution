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
import numpy as np

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

area_rect = patches.Rectangle(
    (17, 0), 16, 19,
    fill=False,
    linewidth=2
)
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



plt.title(f"{name} 2024-2025 Shot Distribution", loc = 'center')
plt.suptitle(f"3PT %: {threeppct}")
plt.axis('off')

# 2 shot percent made within an area made
'''
create multiple sections on the basketball court:
    - these sections will be the areas of highest concentration
    
    
    - will display stats like percent made, ranking in that area
    - will move to expected point based on location (machine learning)
    - sections either predetermined for all players or player specific:
        if player specific ranking does not apply

'''


rx, ry = area_rect.get_xy()  # Bottom-left corner coordinate
rw = area_rect.get_width()
rh = area_rect.get_height()

# 3. Vectorized boundary check using your DataFrame columns
in_x = (shots_player["court_x"] >= rx) & (shots_player["court_x"] <= rx + rw)
in_y = (shots_player["court_y"] >= ry) & (shots_player["court_y"] <= ry + rh)

# 4. Save the true/false mask to your DataFrame
shots_player["inside_paint"] = in_x & in_y
paint_percent = len(shots_player[(shots_player['made'] == 1) & (shots_player["inside_paint"] == True)]) / len(shots_player[shots_player['inside_paint'] == True])

print(f"Paint%: {paint_percent}")

# 3 better graphics
# 4 get all years csvs- put into one large clean dataset and be able to pick year and player
ax.set_aspect('equal')
plt.show()
