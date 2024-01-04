library(tidyverse)
#data <- read.csv('/Users/jessicanguyen/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/output.csv', header=FALSE)
truncated <- read.csv('/Users/jessicanguyen/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/truncated.csv', header=FALSE)

split_data <- strsplit(as.character(truncated), "\\}", fixed=TRUE)

ticker <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[1]
tickers <- sapply(split_data, function(x) trimws(gsub("[\\\\\"]", "", x)))[1]
tickers <- trimws(strsplit(tickers, ",")[[1]])
tickers <- gsub("^c\\(|\\)$", "", tickers)
#tickers done
test_lst <- c('SEC', 'DOJ') #this is where all the tickers should be

companies <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[2]
companies_list <- strsplit(as.character(companies), "\\}")
companies_list <- lapply(companies_list, function(x) as.list(strsplit(x, ",")))
companies_list[[1]] <- lapply(companies_list[[1]], function(x) trimws(gsub("[^a-zA-Z0-9 ]", "",x)))

for (i in seq_along(companies_list)) {
  for (j in seq_along(companies_list[[i]])){
    for (k in seq_along(companies_list[[i]][[j]])){
      if (companies_list[[i]][[j]][[k]] %in% test_lst == TRUE){
        companies_list[[i]][[j]][[k]] <- companies_list[[i]][[j]][[k]]
      }
      else {
         companies_list[[i]][[j]][[k]] <- NA
      }
    }
  }
}
