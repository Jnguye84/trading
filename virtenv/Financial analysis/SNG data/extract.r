library(tidyverse)
library(tidyr)
library(purrr)
data <- read.csv("/Users/jessicanguyen/Documents/GitHub/trading/outputTemp.csv", header=FALSE)
extra_companies <- readLines("companyNames.txt", warn = FALSE)
extra_companies <- sapply(extra_companies, function(line) strsplit(line, ","))
extra_companies <- sapply(extra_companies, function(x) trimws(gsub("\'", "", x)))
extra_companies <- as.list(extra_companies)

split_data <- strsplit(as.character(data), "\\}", fixed=TRUE)

ticker <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[1]
tickers <- sapply(split_data, function(x) trimws(gsub("[\\\\\"]", "", x)))[1]
tickers <- trimws(strsplit(tickers, ",")[[1]])
tickers <- as.list(gsub("^c\\(|\\)$", "", tickers))
combined_tickers <- c(tickers, extra_companies, "Mirati Therapeutics", "Jazz Pharmaceuticals")
#tickers done

companies <- sapply(split_data, function(x) trimws(gsub("\"", "", x[1])))[2]
companies_list <- strsplit(as.character(companies), "\\}")
companies_list <- lapply(companies_list, function(x) as.list(strsplit(x, ",")))
companies_list[[1]] <- lapply(companies_list[[1]], function(x) trimws(gsub("[^a-zA-Z0-9 ]", "",x)))

for (i in seq_along(companies_list)) {
  for (j in seq_along(companies_list[[i]])){
    for (k in seq_along(companies_list[[i]][[j]])){
      if (companies_list[[i]][[j]][[k]] %in% combined_tickers == TRUE){
        companies_list[[i]][[j]][[k]] <- companies_list[[i]][[j]][[k]]
      }
      else {
         companies_list[[i]][[j]][[k]] <- NA
      }
    }
  }
}

cleaned_list <- lapply(companies_list[[1]], function(sublist) sublist[!is.na(sublist)])
cleaned_list <- cleaned_list[-length(cleaned_list)]
cleaned_list <- lapply(cleaned_list, function(x) if (length(x) == 0) "" else x)

sna <- data.frame(Tickers= as.character(tickers), Relationships = as.character(cleaned_list))
sna <- unnest(sna, cols = Relationships)
df_unnested <- separate(sna, col = Relationships, into = c("col1", "col2", "col3", "col4"), sep = ",")
