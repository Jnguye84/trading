#! /usr/bin/Rscript
#run this once every month
library(RedditExtractoR)

reddit_csv <- function(drug, company){
    if (format(Sys.Date(), "%d") == "1") {
    
    write.csv(data, '/Users/jessicanguyen/Documents/GitHub/trading/virtenv/reddit_data.csv')
    } else {
    }
}

