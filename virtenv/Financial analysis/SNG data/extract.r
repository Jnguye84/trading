library(tidyverse)
#data <- read.csv('/Users/jessicanguyen/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/output.csv', header=FALSE)
truncated <- read.csv('/Users/jessicanguyen/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/truncated.csv', header=FALSE)

split_data <- strsplit(as.character(truncated), "\\}", fixed=TRUE)

ticker <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[1]
tickers <- sapply(split_data, function(x) trimws(gsub("c\\(|\\)", "", x)))[1]
ticker <- strsplit(ticker, ",")[[1]]

companies <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[2]

companies_list <- strsplit(as.character(companies), "\\}")
companies_list <- lapply(companies_list, function(x) as.list(strsplit(x, ",")))
for (i in seq_along(companies_list)) {
  companies_list[[i]] <- lapply(companies_list[[i]], function(x) trimws(gsub("[^a-zA-Z0-9 ]", "",x)))
  #delete elements within a list that are not in another list (list of tickers)
  #companies_list[[i]] <- companies_list[[i]][companies_list[[i]] %in% ticker]
}

