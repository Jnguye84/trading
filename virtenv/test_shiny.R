library(shiny)
library(shinydashboard)

ui <- dashboardPage(
  dashboardHeader(title = "Drug Analysis"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Home", tabName = "home"),
      menuItem("Results Sentiment", tabName = "sentiment"),
      menuItem("Results Participants", tabName = "participants"),
      menuItem("Results Reddit", tabName = "reddit")
    )
  ),
  
  dashboardBody(
    tabItems(
      tabItem(tabName = "home",
              fluidRow(
                box(title = "Enter Information",
                    textInput("drug", "Drug Name"),
                    numericInput("psize", "Portfolio Size", value = 1),
                    textInput("company", "Company"),
                    actionButton("submit", "Submit")
                )
              )
      ),
      tabItem(tabName = "sentiment", textOutput("sentiment")),
      tabItem(tabName = "participants", textOutput("participants")),
      tabItem(tabName = "reddit", 
              fluidRow(
                box(title = "Reddit Results", 
                    img(src = "/Users/manas/Documents/GitHub/trading/virtenv/static/img/barplot.png", width = "100%", height = "auto")
                )
              )
      )
    )
  )
)

server <- function(input, output) {
  observeEvent(input$submit, {
    drug <- input$drug
    psize <- input$psize
    company <- input$company
    
    # Assuming you have R functions for sentiment, participants, and Reddit
    # sentiment_results <- results_sentiment(drug)
    # participants_results <- results_participants(drug)
    # reddit_results <- reddit()
    
    output$sentiment <- renderText({
      # Display sentiment results
      "Sentiment Results Here"
    })
    
    output$participants <- renderText({
      # Display participants results
      "Participants Results Here"
    })
    
    output$reddit <- renderImage({
      return(
        list(src = "/Users/manas/Documents/GitHub/trading/virtenv/static/img/barplot.png",
             contentType = "image/png",
             width = "100%", height = "auto")
      )
    }, deleteFile = FALSE)
  })
}

shinyApp(ui, server)

