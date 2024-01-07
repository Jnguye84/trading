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