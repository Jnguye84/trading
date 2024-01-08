#! /usr/bin/Rscript
#install.packages("shiny", type="binary")
#devtools::install_version("RedditExtractoR", version = "2.1.5", repos = "http://cran.us.r-project.org")
#install_github("sachsmc/rclinicaltrials")
library(devtools)
library(rclinicaltrials)
library(RedditExtractoR)
library(dplyr)
library(tidytext)
library(tidyverse)
library(textdata)
library(syuzhet)
library(RColorBrewer)
library(purrr)
library(igraph)

results_sentiment <- function(drug){ #for extracting numbers and sentiment
  data <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)$study_results$outcome_data
  data[is.na(data)] <- 0

  median_superiority <- c()
  median_not_superiority <- c()

  for (unique_id in unique(data$nct_id)) {

    subset_data <- data[data$nct_id == unique_id, ]

  median_superiority[[unique_id]] = as.numeric(subset_data$p_value[subset_data$non_inferiority_type == "Superiority"])
  median_not_superiority[[unique_id]] =  as.numeric(subset_data$p_value[subset_data$non_inferiority_type == "Non-Inferiority"])

  }

  median_superiority <- sapply(median_superiority, function(x) median(x, na.rm = TRUE))
  median_superiority  <- unname(unlist(median_superiority [sapply(median_superiority , is.numeric)], use.names = FALSE, recursive = FALSE))
  median_superiority  <- median(median_superiority , na.rm = TRUE)

  median_not_superiority <- sapply(median_not_superiority, function(x) median(x, na.rm = TRUE))
  median_not_superiority  <- unname(unlist(median_not_superiority [sapply(median_not_superiority , is.numeric)], use.names = FALSE, recursive = FALSE))
  median_not_superiority  <- median(median_not_superiority , na.rm = TRUE)
  median_list <- c(median_superiority, median_not_superiority)
  return(median_list)
}

results_participants <- function(drug){ #to see how many unfinished studies a drug has, how many had unsuccessful participants
  data <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)$study_results$participant_flow
  
  sum_completed <- 0
  sum_not_completed <- 0

  for (unique_id in unique(data$nct_id)) {

    subset_data <- data[data$nct_id == unique_id, ]

    sum_completed <- sum_completed + sum(as.numeric(subset_data$count)[subset_data$status == "COMPLETED"])
    sum_not_completed <- sum_not_completed + sum(as.numeric(subset_data$count)[subset_data$status == "NOT COMPLETED"])
  }

  sum_status <- c(sum_completed, sum_not_completed)
  return(sum_status)
}

#REDDIT
reddit <- function(drug){
  thread_content <- get_thread_content(find_thread_urls(keywords = drug, sort_by = "top", period = 'month')$url[1:300])
  threads <- thread_content$threads$text
  score <- thread_content$threads$score
  data <- data.frame(Threads = threads, Scores = score)
  sentiment_score_lst <- c()

  for (i in seq_len(nrow(data))) {
    current_text <- data$Threads[i]
    tryCatch({
    text_words <- get_tokens(current_text)
    sentiment_scores <- get_nrc_sentiment(text_words, lang="english")
    sentiment_score_lst[[i]] = sentiment_scores
    }, error = function(e) {
      sentiment_score_lst[[i]] <- NA 
      })
  }

  overall_SA <- list(
    "anger" = 0,
    "anticipation" = 0,
    "disgust" = 0,
    "fear" = 0,
    "joy" = 0,
    "sadness" = 0,
    "surprise" = 0,
    "trust" = 0,
    "negative" = 0,
    "positive" = 0
  )

  for (i in seq_len(length(sentiment_score_lst))) {
    current_table <- sentiment_score_lst[[i]]
    overall_SA[['anger']] <- overall_SA[['anger']] + sum(current_table$anger, na.rm = TRUE)
    overall_SA[['anticipation']] <- overall_SA[['anticipation']] + sum(current_table$anticipation, na.rm = TRUE)
    overall_SA[['disgust']] <- overall_SA[['disgust']] + sum(current_table$disgust, na.rm = TRUE)
    overall_SA[['fear']] <- overall_SA[['fear']] + sum(current_table$fear, na.rm = TRUE)
    overall_SA[['joy']] <- overall_SA[['joy']] + sum(current_table$joy, na.rm = TRUE)
    overall_SA[['sadness']] <- overall_SA[['sadness']] + sum(current_table$sadness, na.rm = TRUE)
    overall_SA[['surprise']] <- overall_SA[['surprise']] + sum(current_table$surprise, na.rm = TRUE)
    overall_SA[['trust']] <- overall_SA[['trust']] + sum(current_table$trust, na.rm = TRUE)
    overall_SA[['negative']] <- overall_SA[['negative']] + sum(current_table$negative, na.rm = TRUE)
    overall_SA[['positive']] <- overall_SA[['positive']] + sum(current_table$positive, na.rm = TRUE)
  }

  names_vector <- names(overall_SA)
  values_vector <- unname(unlist(overall_SA))

  png("~/Documents/GitHub/trading/virtenv/static/img/barplot.png")

  barplot(values_vector, 
  names.arg = names_vector, 
  space = 0.2,
  horiz = FALSE,
  las = 1,
  cex.names = 0.7,
  col = brewer.pal(n = 8, name = "Set3"),
  main = "Reddit Sentiment Analysis",
  xlab="Emotions", ylab = NULL)
  

  dev.off()
}

socialnetwork <- function(input){ 
  data <- read.csv("~/Documents/GitHub/trading/outputTemp.csv", header=FALSE)
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
  cleaned_list <- lapply(cleaned_list, function(x) as.list(x))

  sna <- data.frame(Tickers= as.character(tickers), Relationships = as.character(cleaned_list))
  sna$Relationships <- gsub("[^[:alnum:], ]", "", sna$Relationships)
  sna <- separate(sna, col = Relationships, into = paste0("col", 1:14), sep = ",")
  #made dataframe

  long_df <- pivot_longer(sna, cols = -Tickers, names_to = "To", values_to = "From")

  long_df <- subset(long_df, select = -To)
  long_df <- subset(long_df, From != "NA")
  social_network <- graph_from_data_frame(long_df, directed = FALSE)

  # Calculate betweenness centrality
  betweenness_values <- betweenness(social_network)

  betweenness_values <- betweenness_values[order(-betweenness_values)]

  betweenness_dict <- setNames(as.list(betweenness_values), names(betweenness_values))

  percentile <- ecdf(betweenness_values)(betweenness_dict[input]) * 100
  return('The value of',betweenness_dict[input], 'is within the percentile' percentile)
  }

  social_network_graph <- function(input){ #might have to put in shiny itself
  data <- read.csv("~/Documents/GitHub/trading/outputTemp.csv", header=FALSE)
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
  cleaned_list <- lapply(cleaned_list, function(x) as.list(x))

  sna <- data.frame(Tickers= as.character(tickers), Relationships = as.character(cleaned_list))
  sna$Relationships <- gsub("[^[:alnum:], ]", "", sna$Relationships)
  sna <- separate(sna, col = Relationships, into = paste0("col", 1:14), sep = ",")
  #made dataframe

  long_df <- pivot_longer(sna, cols = -Tickers, names_to = "To", values_to = "From")
  #make wide to long format
  long_df <- subset(long_df, Tickers == input)
  long_df <- subset(long_df, select = -To)
  long_df <- subset(long_df, From != "NA")
  social_network <- graph_from_data_frame(long_df, directed = FALSE)
  # Plot the social network graph
  plot(social_network, main = "Social Network Graph")
}

