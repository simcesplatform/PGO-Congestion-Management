**PredictiveGridOptimization (PGO)**

Author:

> Mehdi Attar
>
> Tampere University
>
> Finland

**Introduction**

One of the distribution management system's (DMS) application systems resposible for congestion prediction of distribution network in day ahead time window and addressing any probable congestion using market-based solutions (local flexibility market (LFM)).

**Workflow of the PGO**

**1**- In the first epoch, NIS component in the SimCES environment publishes the network information system ([NIS](https://simcesplatform.github.io/energy_msg-init-nis-networkcomponentinfo/)) and CIS publishes customer information system ([CIS](https://simcesplatform.github.io/energy_msg-init-cis-customerinfo/)) to the RabbitMQ broker topics "Init.NIS.#" and "Init.CIS.CustomerInfo" respectively. By listening to the topics, PGO has access to NIS and CIS data.

**2**- NetworkStatePredictor(NSP) in the SimCES environment publishes predictive flow state of the distribution network (for the day ahead) to the RabbitMQ broker's topic "[NetworkForecaststate](https://simcesplatform.github.io/energy_msg-networkforecaststate-voltage/).#". By listening to the topic, PGO reads the forecasted data.

**3**- PGO analyse the Network forecasted flows according to the network limitations (NIS data), and discovers any probable network congestions.

**4**- if a congestion is forseen for the day ahead, PGO makes a flexibility request containing (time, duration, MinRealPower, RealPowerRequest, CustomerIds) to the LFM market using "[FlexibilityNeed](https://simcesplatform.github.io/energy_msg-flexibilityneed/)" topic.

**5**- Flexibility provider components in the SimCES environment according to their limitations and interests participate in the LFM by providing some flexibility [offers](https://simcesplatform.github.io/energy_msg-offer/).

**6**- LFM componenet in the SimCES environment publishes the received offers to the RabbitMQ broker's "[LFMOffering](https://simcesplatform.github.io/energy_msg-lfmoffering/)". By listening to the topic, PGO makes the decsion of taking the most beneficial bid.

**7**- PGO inform the LFM by publishing the taken bid/bids using "[SelectedOffer](https://simcesplatform.github.io/energy_msg-selectedoffer/)" topic.

**Requirements**

Matlab R2020a (has not been tested with versions other than R2020a)

Java: JDK/JRE 8 or newer

Matlab- rabbitmq connection:

To connect Matlab and RabbitMQ please visit the following page:

https://kannisto.github.io/Cocop.AmqpMathToolConnector

https://git.ain.rd.tut.fi/procemplus/amqpmathtoolintegration

The following libraries were utilised in development. Therefore, all of the libraries should be downloaded and utilized based on instructions given in above webpages [1](https://kannisto.github.io/Cocop.AmqpMathToolConnector) and [2](https://git.ain.rd.tut.fi/procemplus/amqpmathtoolintegration)

amqp-client-4.2.2.jar

amqp-client-4.2.2-javadoc.jar

commons-logging-1.2.jar

slf4j-api-1.7.25.jar

slf4j-nop-1.7.25.jar

**Important Note**

The AMQP connector tool available at [1](https://kannisto.github.io/Cocop.AmqpMathToolConnector) is useful when the receiver (in this case PGO) tend to have no control on arrivals of messages from RabbitMQ broker.

The AMQP connector tool available at [2](https://github.com/simcesplatform/AmqpMathToolIntegration) is useful when the receiver (in this case PGO) requires to control the arrival of messages fron RabbitMQ broker. Since the internal functionality of PGO is demanding, controlling the message arrivals gives the oppurtunity to the PGO to get a new message from the broker only when PGO is done with presessing the previous message (idling).

Depending on the need of PGO, either of connectors might be used. In the current implementation [1](https://kannisto.github.io/Cocop.AmqpMathToolConnector) is used in AmqpConnector.m to listen to management exchange and [2](https://github.com/simcesplatform/AmqpMathToolIntegration) is used in PredictiveGridOptimization.m.
