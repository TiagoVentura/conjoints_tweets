# select names for the experiment
pacman::p_load(tidyverse, here, devtools, gender)

# install names packages
devtools::install_github("jaeyk/validatednamesr", dependencies = TRUE)
library(validatednamesr)


# select names
raw_names <- load_data(file_name = "names.rds")

# add gender 
distinct_first_names <- raw_names %>%
                          ungroup() %>%
                          select(first) %>%
                          distinct()


# get gender
distinct_first_names <- bind_cols(distinct_first_names, gender(distinct_first_names$first) %>% 
                                  select(name, proportion_male))


# merge
left_join(raw_names, distinct_first_names, by="first") %>%
  mutate(gender=ifelse(proportion_male>.5, "male", "female")) %>%
  group_by(identity, gender) %>%
  arrange(identity, desc(mean.correct)) %>%
  ungroup() %>%
  group_by(identity, gender) %>%
  write_csv("code_for_application/names_from_validated.csv")


# cleane names
profiles = read_csv("input/profiles.csv")

profiles %>%
  select(-attractiveness) %>%
  distinct() %>%
  pivot_longer(cols=c(-gender, -race), 
               names_to="profile_type", 
               values_to="names") %>%
  mutate(race=str_to_lower(race)) %>%
  mutate(tag=paste0("@", str_replace_all(names, " ", "")))
