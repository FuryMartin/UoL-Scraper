library(stm)
library(igraph)
load("./not_mobile_topics.RData")
proportion <- as.data.frame(colSums(poliblogPrevFit$theta / nrow(poliblogPrevFit$theta))) # nolint
print(proportion)