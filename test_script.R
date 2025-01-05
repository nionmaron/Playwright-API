# Carregar pacotes necessários
library(httr)
library(jsonlite)

# Definir a URL da API e a URL que queremos raspar
api_url <- "http://localhost:8000/scrape"
target_urls <- c("https://www.engenhariacivil.com/primeira-casa-luxo-elementos-3d-mundo-portuguesa")  # Adicione outras URLs conforme necessário

# Construir o payload JSON
payload <- list(urls = as.list(target_urls))
payload_json <- toJSON(payload, auto_unbox = TRUE)

# Enviar a requisição POST para a API
response <- POST(
  url = api_url,
  body = payload_json,
  encode = "json",
  content_type_json()
)


# Verificar se a requisição foi bem-sucedida
if (status_code(response) == 200) {
  # Parsear o conteúdo da resposta
  response_content <- content(response, as = "text", encoding = "UTF-8")
  response_json <- fromJSON(response_content)
  
  for (url in target_urls) {
    markdown_text <- response_json[[url]]
    
    if (grepl("^Erro", markdown_text)) {
      cat(sprintf("Erro ao processar %s: %s\n", url, markdown_text))
    } else {
      # Exibir o texto no console
      cat(sprintf("Texto em Markdown para %s:\n", url))
      cat(markdown_text)
      
      # Opcional: Salvar o texto em um arquivo Markdown
      safe_filename <- gsub("https?://", "", url)
      safe_filename <- gsub("[^a-zA-Z0-9_-]", "_", safe_filename)
      filename <- paste0(safe_filename, ".md")
      #writeLines(markdown_text, con = filename)
      #cat(sprintf("\nO conteúdo foi salvo no arquivo '%s'.\n\n", filename))
    }
  }
  
} else {
  # Caso a requisição falhe, exibir mensagem de erro
  cat("Erro ao acessar a API. Status:", status_code(response), "\n")
  cat("Mensagem de erro:", content(response, as = "text", encoding = "UTF-8"), "\n")
}

