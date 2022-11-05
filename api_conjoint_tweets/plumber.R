# plumber.R

#* Echo back the input
#* @param msg The message to echo
#* @get /echo
function(msg=""){
  list(msg = paste0("The message is: '", msg, "'"))
}

#* Endpoint that bypasses serialization
#* @get /random_tweets
function(){
  outputs <- read.csv("list_images.csv") # upload all the image
  image <- outputs$file_name[sample(1:nrow(outputs), 1)] # randomize
  url <- paste0("https://raw.githubusercontent.com/TiagoVentura/conjoints_tweets/main/output/output_api/", image) # get the image
  list(url=url) # output
}
