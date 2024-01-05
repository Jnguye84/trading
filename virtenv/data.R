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
reddit <- function(){
  data <- read.csv('/Users/jessicanguyen/Documents/GitHub/trading/virtenv/reddit_data.csv')
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

  png("/Users/jessicanguyen/Documents/GitHub/trading/virtenv/static/img/barplot.png")

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

socialnetwork <- function(graph){

}