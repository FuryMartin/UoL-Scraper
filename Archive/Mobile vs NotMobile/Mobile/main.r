library(stm)
library(stminsights)
library(ggraph)
load("./mobile_topics.RData")
#proportion <- as.data.frame(colSums(poliblogPrevFit$theta/nrow(poliblogPrevFit$theta))) # nolint
# print(proportion)
corrs <- get_network(model = poliblogPrevFit, method = 'simple', labels = paste('Topic',1:10), cutoff = 0.01, cutiso = TRUE) # nolint
ggraph(corrs, layout = "auto") +
    geom_edge_link(
        aes(edge_width = weight),
        label_colour = "#fc8d62",
        edge_colour = "#377eb8"
    ) +
    geom_node_point(size = 8, colour = "black") +
    geom_node_label(
        aes(label = name, size = 0.05),
        colour = "black", repel = TRUE, alpha = 0.85
    ) +
    scale_size(range = c(2, 10), labels = scales::percent) +
    labs(size = "Topic Proportion", edge_width = "Topic Correlation") +
    scale_edge_width(range = c(1, 3)) +
    theme_graph(windowsFont('sans'))

