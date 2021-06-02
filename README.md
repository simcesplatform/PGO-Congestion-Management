****PredictiveGridOptimization (PGO)****
Author
Mehdi Attar
Tampere University
Finland

One of the distribution management system's (DMS) application systems resposible for congestion prediction of distribution network in day ahead time window and addressing any probable congestion using market-based solutions (local flexibility market (LFM)).
workflow of the PGO:
1- In the first epoch, Grid component in the SimCES environment publishes the network information system (NIS) and customerInformation System (CIS) to the rabbitmq broker topics "Init.NIS.#" and "Init.CIS.CustomerInfo" respectively. By listening to the topics, PGO has access to NIS and CIS data.
2- Grid component in the SimCES environment publishes predictive flow state of the distribution network (for the day ahead) to the rabbitmq broker's topic "NetworkForecaststate.#". By listening to the topic, PGO reads the forecasts data.
3- PGO analyse the Network forecasted flows according to the network limitations (inferred from NIS), and discovers any probable network congestions.
4- if a congestion is forseen for the day ahead, PGO makes a flexibility request containing (time, duration, MinRealPower, RealPowerRequest, CustomerIds) to the LFM market using "FlexibilityNeed" topic.
5- ED components in the SimCES environment according to their limitations and interests participate in the LFM by providing some flexibility offers.
6- LFM componenet in the SimCES environment publishes the received offers to the rabbitmq broker's "LFMOffering". By listening to the topic, PGO makes the decsion of taking the most beneficial bid.
7- PGO inform the LFM by publishing the taken bid/bids using "SelectedOffer" topic.


Requirements

Matlab R2020a (has not been tested with versions other than R2020a)
Java: JDK/JRE 8 or newer

Matlab- rabbitmq connection:
To connect Matlab and RabbitMQ please visit the following page:
https://kannisto.github.io/Cocop.AmqpMathToolConnector/
https://git.ain.rd.tut.fi/procemplus/amqpmathtoolintegration

The following libraries were utilised in development. Therefore, all of the libraries should be downloaded and utilized based on instructions given in above webpages.

amqp-client-4.2.2.jar
see https://www.rabbitmq.com/download.html
amqp-client-4.2.2-javadoc.jar
commons-logging-1.2.jar
slf4j-api-1.7.25.jar
slf4j-nop-1.7.25.jar