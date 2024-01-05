library(shiny)

ui <- fluidPage(
  titlePanel("Drug Analysis"),
  
  sidebarLayout(
    sidebarPanel(
      textInput("drug", "Drug Name"),
      numericInput("psize", "Portfolio Size", value = 1),
      textInput("company", "Company"),
      actionButton("submit", "Submit")
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Home", textOutput("home")),
        tabPanel("Results Sentiment", textOutput("sentiment")),
        tabPanel("Results Participants", textOutput("participants")),
        tabPanel("Results Reddit", textOutput("reddit"))
      )
    )
  )
)

server <- function(input, output) {
  
  output$home <- renderText({
    "Enter Information"
  })
  
  observeEvent(input$submit, {
    drug <- input$drug
    psize <- input$psize
    company <- input$company

    # Assuming you have R functions for sentiment, participants, and Reddit
    sentiment_results <- call_results_sentiment(drug)
    participants_results <- call_results_participants(drug)
    reddit_results <- call_results_reddit()

    output$sentiment <- renderText({
      # Display sentiment results
      sentiment_results
    })

    output$participants <- renderText({
      # Display participants results
      participants_results
    })

    output$reddit <- renderText({
      # Display Reddit results
      reddit_results
    })
  })
}

shinyApp(ui, server)
