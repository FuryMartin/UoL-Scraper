library(stm)
library(openxlsx)
library(sentimentr)
library(lubridate)
library(patchwork)

load("./AmazonGo.RData")
load("./out_data.RData")
load("./k_selection.RData")

pdf("AmazonGo.pdf")
# plot Topics
plot(stm_model, type = "summary", xlim = c(0, 0.3))
print("Finished Ploting Topics")

# plot sentiment
out_data$meta$processed_date <- as.Date(out_data$meta$review_datetime_utc, "%m/%d/%Y %H:%M:%S")
min_date <- min(out_data$meta$processed_date)
max_date <- max(out_data$meta$processed_date)
out_data$meta$processed_date <- as.numeric(out_data$meta$processed_date - min_date)
prep <- estimateEffect(1:20 ~ sentiment_score + s(processed_date), stm_model, meta = out_data$meta, uncertainty = "Global")
plot(prep,
    covariate = "sentiment_score", topics = c(1:20),
    model = stm_model, method = "difference",
    cov.value1 = "Postive", cov.value2 = "Negative",
    xlab = "More Postive ... More Negative",
    main = "Effect of content sentiment",
    xlim = c(.15, -.15), labeltype = "custom",
    custom.labels = c(
        "Topic 1", "Topic 2", "Topic 3", "Topic 4",
        "Topic 5", "Topic 6", "Topic 7", "Topic 8",
        "Topic 9", "Topic 10", "Topic 11", "Topic 12",
        "Topic 13", "Topic 14", "Topic 15", "Topic 16",
        "Topic 17", "Topic 18", "Topic 19", "Topic 20"
    )
)
print("Finished Ploting Sentiment")

# plot Topic Correlations
coor <- topicCorr(stm_model)
plot(coor)
print("Finished Ploting Topic Correlations")

# plot K Selection
plot(k_selection)
print("Finished Ploting K Selection")

# plot prevalence changes over time
p = c("")
for (i in c(1:20)) {
    monthseq <- seq(from = min_date, to = max_date, by = "month")
    yearnames <- year(monthseq)

    p[i] <- plot(prep, "processed_date", method = "continuous", topics = i, model = stm_model, printlegend = FALSE, xaxt = "n", xlab = paste("Topic ", as.character(i)), ) + axis(1, at = as.numeric(monthseq) - min(as.numeric(monthseq)), labels = yearnames)
}
p0 <- p[1]
for (i in c(2:20)){
    p0 <- p0 + p[i]
}
p0
print("Finished Ploting Prevalence Changes")

# End plot
dev.off()