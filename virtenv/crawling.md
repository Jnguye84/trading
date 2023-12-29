Find within this url, different NCT numbers. Will need to webcrawl. https://www.clinicaltrials.gov/search?intr=exparel

Input NCT number within search bar to find articles that may have the related outcomes (http://arrowsmith.psych.uic.edu/cgi-bin/arrowsmith_uic/TrialPubLinking/trial_pub_link_start.cgi)

data.R
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
