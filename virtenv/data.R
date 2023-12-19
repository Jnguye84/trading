#install.packages("shiny", type="binary")
library(devtools)
#install_github("sachsmc/rclinicaltrials")
#nctids <- c('NCT01801124')
drug <- 'Exparel'
#drug <- read_csv('drug.csv')
#list_ids <- read_csv('my_NCTIds.csv')
library(rclinicaltrials)

#They are organized into study information, locations, outcomes, interventions, results, and textblocks. Results, where available, is itself a list with three dataframes: participant flow, baseline data, and outcome data.

#for nctid in nctids{
    #y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With', paste('term=',nctid,sep='')), count = #10, include_results = TRUE)
#}

#summary(y$study_results$baseline_data)

y <- clinicaltrials_download(query = c(paste('cond=',drug,sep=''), 'rslt=With'), count = 10, include_results = TRUE)

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


#useful for finding outcomes: y$study_information$outcomes for extracting numbers and sentiment, y$study_results$participant_flow is good to see how many unfinished studies a drug has, how many had unsuccessful participants