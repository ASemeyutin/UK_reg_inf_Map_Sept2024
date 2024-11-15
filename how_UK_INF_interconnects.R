# ============================================================================= #
# load packages (and install if you run this for the first time)
#
my_libs = c("ConnectednessApproach", "data.table", "xts", "tidyverse", "networkD3")
# install.packages(my_libs)
lapply(my_libs, require, character.only = TRUE)
# ============================================================================= #
# load data (change path to data accordingly)
#
UK_infl_reg = fread("UK_infl_reg.csv")
UK_infl_reg = as.data.frame(UK_infl_reg)[,-c(1,3,4)]
UK_infl = as.xts(UK_infl_reg[,-1], order.by = as.Date(UK_infl_reg[,1]))
# ============================================================================= #
# compute Diebold & Yilmaz (2012) connectedness measures;
# I use basic ad hoc spec, standard VAR and 12 lags since data is monthly ...
#
n_cors = 10
n_lags = 12 
dca = ConnectednessApproach(UK_infl, nlag = n_lags, nfore = n_cors)
#
# my main target is to build upon the basic figure in the "ConnectedessApproach"
# library to visualise how UK inflation across regions is interconnected (historically)
# so I just blindly follow package maintainer approach though I have questions ...
#
CON_m = dca$NPDC
CON_m = t(apply(CON_m[ , , 1], 1:2, mean)) # e.g. here ... why? may be in specific applications ...
CON_m[CON_m < 0] = 0
diag(CON_m) = 0
CON_m = CON_m - min(CON_m) # e.g. here ... why? if set the lowest value to zero ... 
CON_m = CON_m/max(CON_m)
CON_m[CON_m<0.25] = 0 # used their default threshold ... can be changed (impacts figure substantially)
#
UK_region_names = c("LDN", "SE", "SW", "EE", "EM", "WM", 
                    "YH", "NW", "NE", "WLS", "SCT", "NI")
colnames(CON_m) = UK_region_names
row.names(CON_m) = UK_region_names
CON_m = data.frame(CON_m)
#
CON_m = CON_m %>%
        rownames_to_column() %>%
        gather(key = 'key', value = 'value', -rowname) %>%
        filter(value > 0)
colnames(CON_m) = c("source", "target", "value")
nodes = data.frame(name=c(as.character(CON_m$source), 
                          as.character(CON_m$target)) %>% unique())
# 
CON_m$IDsource=match(CON_m$source, nodes$name)-1
CON_m$IDtarget=match(CON_m$target, nodes$name)-1
#
# write.csv(CON_m, "UK_CON_M.csv", row.names = F)
#
# my main target was to obtain the above .csv for my python plotting;
# but below is a simple and yet improved version on how you could visualise 
# inflation interconnections among regions in the UK 
#
ColourScal ='d3.scaleOrdinal() .range(["#9e2a2b","#335c67", "#627276"])'
sankeyNetwork(Links = CON_m, Nodes = nodes,
              Source = "IDsource", Target = "IDtarget",
              Value = "value", NodeID = "name",
              sinksRight=FALSE, colourScale=ColourScal, 
              nodeWidth=50, fontSize=18, nodePadding=20)
#
# the default network plot, is just too crowded and not presentable
# PlotNetwork(dca)
# ============================================================================= #