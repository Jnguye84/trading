#! /usr/bin/Rscript
#install.packages("shiny", type="binary")
#devtools::install_version("RedditExtractoR", version = "2.1.5", repos = "http://cran.us.r-project.org")
#install_github("sachsmc/rclinicaltrials")
library(devtools)
library(rclinicaltrials)
library(RedditExtractoR)


results_sentiment <- function(drug){ #for extracting numbers and sentiment
  y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)$study_results$outcome_data
}

results_participants <- function(drug){ #to see how many unfinished studies a drug has, how many had unsuccessful participants
  y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)$study_results$participant_flow
}

#REDDIT
reddit <- function(drug, company){
  thread_content <- get_thread_content(find_thread_urls(keywords = company, sort_by = "top", period = 'year')$url[1:100])
  threads <- thread_content$threads$text
  score <- thread_content$threads$score
  return(threads)
}
