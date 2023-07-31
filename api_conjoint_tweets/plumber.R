# plumber.R

#* Echo back the input
#* @param msg The message to echo
#* @get /echo
function(msg=""){
  list(msg = paste0("The message is: '", msg, "'"))
}

#* Endpoint that bypasses serialization
#* @param issue_query
#* @get /random_tweets
function(issue_query=""){
  outputs <- read.csv("list_images.csv")  %>% 
              dplyr::filter(p_issue==issue_query) %>%
              dplyr::select(file_name=p_output) 
  image <- outputs$file_name[sample(1:nrow(outputs), 1)] # randomize
  url <- paste0("https://raw.githubusercontent.com/TiagoVentura/conjoints_tweets/main/output/out_testing_real_tw/", image) # get the image
  # capture output
  out = list(url=url) # output
  
  # change name
  name <- paste0("url.", issue_query)
  names(out) = name
  # return
  out
}

