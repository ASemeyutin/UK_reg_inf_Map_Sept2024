# ================================================================================================ #
# libs
from pathlib import Path  
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from drawarrow import fig_arrow
from pyfonts import load_font
from highlight_text import fig_text, ax_text
from datetime import datetime
#
# ================================================================================================ #
# paths
UK_infl = Path(__file__).parent / "UK_infl_reg.csv"
UK_CON_M = Path(__file__).parent / "UK_CON_M.csv"
fname_geo_bndr = Path(__file__).parent / "NUTS1_Jan_2018_UGCB_in_the_UK_2022.geojson"
#
# ================================================================================================ #
# data load
INF = pd.read_csv(UK_infl)
UK_CON = pd.read_csv(UK_CON_M)
geodf = gpd.read_file(fname_geo_bndr)
#
# ================================================================================================ #
# fonts & colors
font = load_font('https://github.com/dharmatype/Bebas-Neue/blob/master/fonts/BebasNeue(2018)ByDhamraType/ttf/BebasNeue-Regular.ttf?raw=true')
other_font = load_font('https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Light.ttf?raw=true')
other_bold_font = load_font('https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Medium.ttf?raw=true')
#
color_1 = '#335c67'
color_2 = '#9e2a2b'
color_3 = '#627276'
#
background_color = '#e9eeef'
text_color = 'black'
#
# ================================================================================================ #
# legacy from shiny UI ... 
YEAR_C = "2024"
MONTH_C = "09"
#
U_choice_date = INF.index[INF["date"]==int(YEAR_C+MONTH_C)][0]
U_choice_infl_benchmark = "infld1"
U_choice_source_1 = "LDN"
U_choice_source_2 = "SE"
#
if U_choice_infl_benchmark == "infld1":
    k=2 
else:
    k=3
#
# ================================================================================================ #
# data play
INFym = INF.iloc[U_choice_date,2:]
INFym = pd.DataFrame({
    "region" : ["London", "South East", "South West", "East of England", 
                "East Midlands", "West Midlands", "Yorkshire and Humber", " North West", 
                "North East", "Wales", "Scotland", "Northern Ireland"],
    "infl" : INFym.iloc[2:].values,
    "infld1" : INFym.iloc[0] - INFym.iloc[2:].values,
    "infld2" : INFym.iloc[1] - INFym.iloc[2:].values
})
#
INForder = [6, 7, 8, 5, 3, 4, 2, 1, 0, 9, 10, 11]
geodf = geodf.loc[INForder].reset_index(drop=True)
geodf = geodf.rename({"nuts118cd": "reg", "nuts118nm": "region"}, axis =1)
geodf["region"] = INFym["region"]
geodf['reg'] = ["LDN", "SE", "SW", "EE", "EM", "WM", "YH", "NW", "NE", "WLS", "SCT", "NI"]
#
INFym_geo = geodf.merge(INFym, on = 'region').set_index('region')
geo_only = geodf[['reg', 'geometry']]
#
data_projected = INFym_geo.to_crs(epsg=3035)
data_projected['centroid'] = data_projected.geometry.centroid
INFym_geo['centroid'] = data_projected['centroid'].to_crs(INFym_geo.crs)
data_projected = geo_only.to_crs(epsg=3035)
data_projected['centroid'] = data_projected.geometry.centroid
geo_only['centroid'] = data_projected['centroid'].to_crs(geo_only.crs)
#
UK_CON_temp_1 = UK_CON.loc[UK_CON['source'] == U_choice_source_1]
UK_CON_temp_2 = UK_CON.loc[UK_CON['source'] == U_choice_source_2]
#
my_color_map_1 = np.where(INFym_geo[U_choice_infl_benchmark]>0, color_1, color_2)
my_color_map_2 = np.where(geo_only['reg'].isin(UK_CON_temp_1["target"]), color_2, color_3)
my_color_map_2 = np.where(geo_only['reg'].isin(UK_CON_temp_2["target"]), color_2, my_color_map_2)
my_color_map_2 = np.where(geo_only['reg'] == U_choice_source_1, color_1, my_color_map_2)
my_color_map_2 = np.where(geo_only['reg'] == U_choice_source_2, color_1, my_color_map_2)
#
regions_to_ann_1 = ["SE", "SW", "EE", "EM", "WM", "YH", "WLS", "SCT", "NI"]
regions_to_ann_2 = geodf['reg'][2:12]
adjustments_1 = {
    "SE"  : (0, -0.2),
    "WLS" : (-0.1, -0.35),
    "SCT": (0.2, 0),
    "WM": (0.05, -0.05)
}
adjustments_2 = {
    "NW"  : (0.1, -0.2),
    "WLS" : (-0.1, -0.35),
    "EM"  : (0.2, 0),
    "EE"  : (0.2, 0)
}
#
arrow_props = dict(width=0.4, head_width=1.5, head_length=4, color=text_color)
#
# ================================================================================================ #
# map 1 and map 2 figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (4,3), dpi =300)
fig.set_facecolor(background_color)
#
ax1.set_ylim(49, 58.725)
ax1.set_xlim(-8.5, 1.9)
ax1.set_axis_off()
ax2.set_ylim(49, 58.725)
ax2.set_xlim(-8.5, 1.9)
ax2.set_axis_off()
#
# Legend
labels_1 = [f"< {INF.iloc[U_choice_date, k]:.2f} UK CPIH" , f"> {INF.iloc[U_choice_date, k]:.2f} UK CPIH"]
labels_2 = ["From LDN & SE", "To Region", "No Spillover"]
# 
rectangle_width = 1
rectangle_height = 0.5
legend_x = -1.65
legend_y_start = 57.75
legend_y_step = 0.575
#
for i in range(len(labels_1)):
   ax1.add_patch(plt.Rectangle((legend_x, legend_y_start - i * legend_y_step), rectangle_width, rectangle_height,
                              color=[color_1, color_2][i], ec = text_color, lw=0.5))
   ax1.text(legend_x + 1.25, legend_y_start - i * legend_y_step + 0.25, labels_1[i],
         fontsize= 4, fontproperties=other_font, color=text_color, va='center')
for i in range(len(labels_2)):
   ax2.add_patch(plt.Rectangle((legend_x, legend_y_start - i * legend_y_step), rectangle_width, rectangle_height,
                              color=[color_1, color_2, color_3][i], ec = text_color, lw=0.5))
   ax2.text(legend_x + 1.25, legend_y_start - i * legend_y_step + 0.25, labels_2[i],
         fontsize= 4, fontproperties=other_font, color=text_color, va='center')
#
INFym_geo.plot(column = "infl", ax = ax1, color=my_color_map_1, edgecolor=text_color, linewidth=0.25)
#
for reg in regions_to_ann_1:
    centr = INFym_geo.loc[INFym_geo["reg"] == reg, "centroid"].values[0]
    x, y = centr.coords[0]
    rate = INFym_geo.loc[INFym_geo['reg'] == reg, 'infl'].values[0]
    try:
        x += adjustments_1[reg][0]
        y += adjustments_1[reg][1]
    except KeyError:
        pass
    ax_text(
      x=x, y=y, s=f"<{reg.upper()}>: {rate:.2f}", fontsize= 3.5, font=other_font, color=text_color,
      ha='center', va='center', ax=ax1, highlight_textprops=[{'font': other_bold_font}]
   )
#
geo_only.plot(ax=ax2, color=my_color_map_2, edgecolor=text_color, linewidth=0.25)
#
for reg in regions_to_ann_2:
    centr = geo_only.loc[geo_only["reg"] == reg, "centroid"].values[0]
    x, y = centr.coords[0]
    try:
        x += adjustments_2[reg][0]
        y += adjustments_2[reg][1]
    except KeyError:
        pass
    ax_text(
      x=x, y=y, s=f"<{reg.upper()}>", fontsize= 3.5, font=other_font, color=text_color,
      ha='center', va='center', ax=ax2, highlight_textprops=[{'font': other_bold_font}]
   )
#
# Left panel arrows and anotations 
fig_arrow(tail_position=(0.18, 0.33), head_position=(0.42, 0.31), radius=0.2, **arrow_props) # LND
fig_arrow(tail_position=(0.385, 0.65), head_position=(0.335, 0.58), radius=-0.3, **arrow_props) # NE
fig_arrow(tail_position=(0.235, 0.475), head_position=(0.325, 0.535), radius=0.3, **arrow_props) # NW
#
LDN = INFym_geo.loc[INFym_geo['reg'] == 'LDN', 'infl'].values[0]
NE = INFym_geo.loc[INFym_geo['reg'] == 'NE', 'infl'].values[0]
NW = INFym_geo.loc[INFym_geo['reg'] == 'NW', 'infl'].values[0]
#
fig_text(s=f"<LDN>: {LDN:.2f}", x=0.18, y=0.34, highlight_textprops=[{'font': other_bold_font}],
        color=text_color, fontsize=3.5, font=other_font, ha='center', va='center', fig=fig)
fig_text(s=f"<NE>: {NE:.2f}", x=0.39, y=0.65, highlight_textprops=[{'font': other_bold_font}],
        color=text_color, fontsize=3.5, font=other_font, ha='center', va='center', fig=fig)
fig_text(s=f"<NW>: {NW:.2f}", x=0.215, y=0.475, highlight_textprops=[{'font': other_bold_font}],
        color=text_color, fontsize=3.5, font=other_font, ha='center', va='center', fig=fig) 
#
# Right panel arrows
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.62, 0.55), radius=0.15, **arrow_props) #  to NI
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.775, 0.575), radius=0.3, **arrow_props) #  to NE
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.735, 0.275), radius=0.15, **arrow_props) # to SW
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.86, 0.365), radius=0.15, **arrow_props) # to EE
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.71, 0.3475), radius=0.15, **arrow_props) # to WLS
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.71, 0.65), radius=0.05, **arrow_props) # to SCT
fig_arrow(tail_position=(0.825, 0.30), head_position=(0.815, 0.4225), radius=0.15, **arrow_props) # to EM
#
# Figure Title
fig_text(
   s=f"UK Inflation (Micro CPI) for September {YEAR_C} & Historical Inflation Spillovers From SE and London", x=0.5, y=0.15,
   color=text_color, fontsize=8, font=font, ha='center', va='top', ax=ax1
)
# Authors
fig_text(
   s="by <Artur> Semeyutin", x=0.5, y=0.1,
   color=text_color, fontsize=6, font=other_font, ha='center', va='top', ax=ax1,
   highlight_textprops=[{'font': other_bold_font}]
)
#
# plt.savefig('./AS_September2024.png', dpi=600)
plt.show()
#
# ================================================================================================ #