library(plumber)
options(httr_oob_default = TRUE)
root <- pr("/home/rstudio/plumber_api/plumber_api.r")
pr_run(root, host = "0.0.0.0", port = 8000)
