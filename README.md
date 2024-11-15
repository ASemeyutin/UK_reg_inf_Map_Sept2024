## UK Regional Inflation Map September 2024
This repo produces the below UK inflation map by region for September 2024 using the ONS Price and Quotes Micro Data database.

![](https://github.com/ASemeyutin/UK_reg_inf_Map_Sept2024/blob/main/AS_September2024.png)

This figure is just a small extension to what is available within my Shiny app that I develop specifically for the UK regional inflation data interactive visualisations.
````
To replicate the map, run:
1. how_UK_INF_interconnects.R
2. join_map.py
````
R file performs simple computations using a Vector Autoregressive Model to estimate how UK inflation across regions is interconnected and produces the UK_CON_M.csv file. It also contains code for below interactive (full) connectedness network that is only fractionally illustrated in the main figure (map on the right).

![](https://github.com/ASemeyutin/UK_reg_inf_Map_Sept2024/blob/main/UK_INF_NET.gif)

Overall, left map points out an interesting perspective on inflation in the UK in September 2024. Its "north" with higher inflation vs "south" with lower inflation than the national CPIH figures. On the other hand, right map suggests regions which followed London and South East lower (higher) inflation historically.

P.S. Even a broken clock is right twice a day. Hence, this is just an interesting observation for September 2024 and not a forecast. I shall make an initial version of the Shiny app available in a separate repo, with all credits and regional inflation computational details available in the app description. 