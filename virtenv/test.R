data <- read.csv('virtenv/results_participants.csv')

sum_completed <- 0
sum_not_completed <- 0

for (unique_id in unique(data$nct_id)) {

  subset_data <- data[data$nct_id == unique_id, ]

  sum_completed <- sum_completed + sum(subset_data$count[subset_data$status == "COMPLETED"])
  sum_not_completed <- sum_not_completed + sum(subset_data$count[subset_data$status == "NOT COMPLETED"])
}

sum_status <- c(sum_completed, sum_not_completed)
