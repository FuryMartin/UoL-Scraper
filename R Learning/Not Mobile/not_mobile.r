library(stm)
data <- read.csv("NotMobile.csv")
processed <- textProcessor(data$documents, metadata = data)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
plotRemoved(processed$documents, lower.thresh = seq(1, 200, by = 100))
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, lower.thresh = 15) # nolint
poliblogPrevFit <- stm(documents = out$documents, vocab = out$vocab, K = 20, data = out$meta, init.type = "Spectral") # nolint
pdf("NotMobile.pdf")
save(poliblogPrevFit, file = "./not_mobile_topics.RData")
plot(poliblogPrevFit, type = "summary", xlim = c(0, 0.3))
dev.off()