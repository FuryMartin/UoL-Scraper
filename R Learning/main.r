library(stm)
data <- read.csv("data.csv")
processed <- textProcessor(data$documents, metadata = data)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
plotRemoved(processed$documents, lower.thresh = seq(1, 200, by = 100))
out <- prepDocuments(processed$documents, processed$vocab,  processed$meta, lower.thresh = 15) # nolint
poliblogPrevFit <- stm(documents = out$documents, vocab = out$vocab, K = 20, prevalence = ~ ViaMobiles, max.em.its = 75, data = out$meta, init.type = "Spectral") # nolint
plot(poliblogPrevFit, type = "summary", xlim = c(0, 0.3))
poliblogContent <- stm(out$documents, out$vocab, K = 20, prevalence =~ ViaMobiles, content =~ ViaMobiles,max.em.its = 75, data = out$meta, init.type = "Spectral") # nolint
plot(poliblogContent, type = "perspectives", topics = 18)