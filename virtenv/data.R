#! /usr/bin/Rscript
#install.packages("shiny", type="binary")
library(devtools)
#install_github("sachsmc/rclinicaltrials")
library(rclinicaltrials)

results_sentiment <- function(drug){ #for extracting numbers and sentiment
  y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)
  result <- y$study_information$outcomes
}

results_participants <- function(drug){ #to see how many unfinished studies a drug has, how many had unsuccessful participants
  y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)
  summary(y$study_results$participant_flow)
}

results_somenumber <- function(drug, portsize){
    print(portsize)
}



#They are organized into study information, locations, outcomes, interventions, results, and textblocks. Results, where available, is itself a list with three dataframes: participant flow, baseline data, and outcome data.

#term -> Search Terms
#recr -> Recruitment
#rslt -> Study Results
#type -> Study Type
#cond -> Conditions
#intr -> Interventions

#names(y$study_information)
#[1] "study_info"    "locations"     "arms"          "interventions"
#[5] "outcomes"      "textblocks"   

#> names(y$study_results)
#[1] "participant_flow" "baseline_data"    "outcome_data"    

