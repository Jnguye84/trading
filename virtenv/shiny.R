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
        tabPanel("Results Reddit", textOutput("reddit")),
        tabPanel("Results Social Network", textOutput("socialnetwork")),
        tabPanel("Results Social Network Graph", textOutput("socialnetworkgraph"))
        
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

    source("~/Documents/GitHub/trading/virtenv/data.R")

    # Assuming you have R functions for sentiment, participants, and Reddit
    sentiment_results <- results_sentiment(drug)
    participants_results <- results_participants(drug)
    reddit_results <- reddit(drug)
    social_network <- social_network(company)
    social_network_graph <- social_network_graph(company)

    output$sentiment <- renderText({
      # Display sentiment results
      sentiment_results
    })

    output$participants <- renderText({
      # Display participants results
      participants_results
    })

    output$reddit <- renderImage({
      return(
        list(src = "~/Documents/GitHub/trading/virtenv/static/img/barplot.png",
             contentType = "image/png",
             width = "100%", height = "auto")
      )
    }, deleteFile = FALSE)

    output$socialnetwork <- renderText({
      # Display social network betweenness scores
      social_network
    })

    output$socialnetworkgraph <- renderGraph({
    #display social network graph
    })

  })
}

shinyApp(ui, server)
#shiny::runApp("virtenv/shiny.R")