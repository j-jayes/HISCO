#' Process HISCO Data
#'
#' This function processes a dataframe containing a 'hisco' column. It performs the following steps:
#' 1. If the 'hisco' column has four characters, it prepends a zero.
#' 2. Creates a new column 'hisco_major_group' which is the first character of the 'hisco' column if it contains five characters; otherwise, sets to missing (NA).
#' 3. Maps the 'hisco_major_group' values to their respective group descriptions, producing a new column named 'hisco_major_group_label'.
#' 
#' @param data A dataframe containing at least the 'hisco' column.
#' @return The input dataframe with two new columns: 'hisco_major_group' and 'hisco_major_group_label'.
process_hisco_data <- function(data) {
  # Assuming you've installed the dplyr package
  library(dplyr)
  
  # Modify the hisco column and create hisco_major_group
  data <- data %>%
    mutate(hisco = ifelse(nchar(hisco) == 4, paste0("0", hisco), hisco),
           hisco_major_group = ifelse(nchar(hisco) == 5, substr(hisco, 1, 1), NA_character_))

  # Create hisco_major_group_label based on classification
  hisco_label_mapping <- data.frame(
    hisco_major_group = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
    group_description = c(
      "Professional, technical and related workers",
      "Professional, technical and related workers",
      "Administrative and managerial workers",
      "Clerical and related workers",
      "Sales Workers",
      "Service workers",
      "Agricultural, animal husbandry and forestry workers, fishermen and hunters",
      "Production and related workers, transport equipment operators and labourers",
      "Production and related workers, transport equipment operators and labourers",
      "Production and related workers, transport equipment operators and labourers"
    )
  )

  data <- left_join(data, hisco_label_mapping, by = "hisco_major_group")

  # Rename columns if needed
  data <- data %>%
    rename(hisco_major_group_label = group_description)
  
  return(data)
}

# Sample usage:
# sample_data <- data.frame(hisco = c("1234", "51234", "9123", "50123", "12345"))
# processed_data <- process_hisco_data(sample_data)
# print(processed_data)
