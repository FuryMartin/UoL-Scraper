library(stm)
library(openxlsx)
library(sentimentr)
library(lubridate)

data <- read.xlsx("NearbyStores.xlsx")
date_paser <- "%m/%d/%Y %H:%M:%S"
date_list <- out_data$meta$review_datetime_utc
stop_words <- c("store", "amazon", "item", "shop", "translated", "by","google")

# remove words and process documents
#remove.words <- c("item", "one", "like", "get")
remove.words <- stop_words
processed <- textProcessor(data$documents, metadata = data, customstopwords = remove.words)
out_data <- prepDocuments(processed$documents, processed$vocab, processed$meta)

# sentiment modeling
senti <- sentiment_by(out_data$meta$documents)
sentiment_score <- senti$ave_sentiment
save(sentiment_score, file = "./RData/sentiment_score.RData")

out_data$meta$sentiment_score <- sentiment_score
save(out_data, file = "./RData/out_data.RData")
print("Finished Sentiment Modeling")

# STM modeling
stm_model <- stm(documents = out_data$documents, vocab = out_data$vocab, K = 20, data = out_data$meta, init.type = "Spectral") # nolint
save(stm_model, file = "./RData/NearbyStores.RData")
print("Finished STM Modeling")

# Start plot
pdf("NearbyStores.pdf")
# plot Topics
plot(stm_model, type = "summary", xlim = c(0, 0.3))
print("Finished Ploting Topics")

# plot sentiment
out_data$meta$processed_date <- as.Date(date_list, date_paser)
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
k_selection <- searchK(
    out_data$documents,
    out_data$vocab,
    K = c(2:20), max.em.its = 48,
    prevalence = ~sentiment_score, data = out_data$meta
)
save(k_selection, file = "./RData/k_selection.RData")
plot(k_selection)
print("Finished Ploting K Selection")

# plot prevalence changes over time
for (i in c(1:20)) {
    plot(prep, "processed_date", method = "continuous", topics = i, model = stm_model, printlegend = FALSE, xaxt = "n", xlab = paste("Topic ", as.character(i)), )
    monthseq <- seq(from = min_date, to = max_date, by = "month")
    yearnames <- year(monthseq)
    axis(1, at = as.numeric(monthseq) - min(as.numeric(monthseq)), labels = yearnames)
}
print("Finished Ploting Prevalence Changes")

# End plot
dev.off()

# Open Workbook
wb <- loadWorkbook("NearbyStores.xlsx")

# Sheet 2 Write
# write topic proportion for each comment
each_proportion <- as.data.frame(stm_model$theta)
writeData(wb, "Sheet2", each_proportion)

# Sheet 3 Write 
# Initialize Title
title <- list("Topic No.", "Topic Proportion", "Topic Labels", "Top 10 Words")
writeData(wb, "Sheet3", title, xy = c(1, 1))
writeData(wb, "Sheet3", c(1:20), xy = c(1, 2))

# label Topics
topics <- labelTopics(stm_model, n = 10)
topics_str <- list("")
for (i in c(1:20)) {
    topic <- paste(topics$prob[i, ], collapse = ",")
    topics_str[i] <- topic
}
topics_str <- unlist(topics_str)
writeData(wb, "Sheet3", unlist(topics_str), xy = c(4, 2))

# get proportion
proportion <- colSums(stm_model$theta / nrow(stm_model$theta)) # nolint
writeData(wb, "Sheet3", proportion, xy = c(2, 2))

# find thoughts
docs <- out_data$documents
meta <- out_data$meta
title <- list("Example1", "Example2", "Example3", "Example4", "Example5", "Example6", "Example7", "Example8")
writeData(wb, "Sheet3", title, xy = c(5, 1))
for (i in c(1:20)) {
    thoughts <- findThoughts(stm_model, texts = as.character(meta$documents), n = 8, topics = i)$docs[[1]]
    # print(class(thoughts))
    for (j in c(1:8)) {
        writeData(wb, "Sheet3", thoughts[j], xy = c(4 + j, i + 1))
    }
}

# Save Workbook
saveWorkbook(wb, file = "NearbyStores.xlsx", overwrite = T)