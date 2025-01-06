
# Load necessary packages
library(httr)
library(jsonlite)

# Define the API URL and the target URL to scrape
api_url <- "http://localhost:8000/scrape"
target_urls <- c("https://www.engenhariacivil.com/primeira-casa-luxo-elementos-3d-mundo-portuguesa")  # Add other URLs as needed

# Build the JSON payload
payload <- list(urls = as.list(target_urls))
payload_json <- toJSON(payload, auto_unbox = TRUE)

# Send the POST request to the API
response <- POST(
  url = api_url,
  body = payload_json,
  encode = "json",
  content_type_json()
)

# Check if the request was successful
if (status_code(response) == 200) {
  # Parse the response content
  response_content <- content(response, as = "text", encoding = "UTF-8")
  response_json <- fromJSON(response_content)
  
  for (url in target_urls) {
    markdown_text <- response_json[[url]]
    
    if (grepl("^Error", markdown_text)) {
      cat(sprintf("Error processing %s: %s\n", url, markdown_text))
    } else {
      # Display the text in the console
      cat(sprintf("Markdown text for %s:\n", url))
      cat(markdown_text)
      
      # Optional: Save the text to a Markdown file
      safe_filename <- gsub("https?://", "", url)
      safe_filename <- gsub("[^a-zA-Z0-9_-]", "_", safe_filename)
      filename <- paste0(safe_filename, ".md")
      #writeLines(markdown_text, con = filename)
      #cat(sprintf("\nThe content has been saved to the file '%s'.\n\n", filename))
    }
  }
  
} else {
  # If the request fails, display an error message
  cat("Error accessing the API. Status:", status_code(response), "\n")
  cat("Error message:", content(response, as = "text", encoding = "UTF-8"), "\n")
}

