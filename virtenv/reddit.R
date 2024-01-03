#! /usr/bin/Rscript
#run this once every month
library(RedditExtractoR)

reddit_csv <- function(drug, company){
    if (format(Sys.Date(), "%d") == "1") {
    thread_content <- get_thread_content(find_thread_urls(keywords = drug, sort_by = "top", period = 'month')$url[1:300])
    threads <- thread_content$threads$text
    score <- thread_content$threads$score
    data <- data.frame(Threads = threads, Scores = score)
    write.csv(data, 'virtenv/reddit_data.csv')
    } else {
    }
}

