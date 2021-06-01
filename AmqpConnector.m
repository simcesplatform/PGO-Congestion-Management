%                        StateMonitoring (SM) Application System
% The application system includes the following sub-programs:
% 1- AmqpConnector . (It listens to the Management exchange)
% 2- ManagementCallback. (It initiates an instance of StateMonitoring class)
% 3- StateMonitoring. (It operates the StateMonitoring functionality for a simulation run)
% Two APIs are used here.
% 1- the API is autonomuos in a sense that it receives incoming messages irrespective of StateMonitoring workload. The API is used to listen to the Management exchange. 
% Please visit https://kannisto.github.io/Cocop.AmqpMathToolConnector/
% 2- the API execution is dependant on the workload of StaeMonitoring. Once the StateMonitoring is idle, a new message could come.
% Please visit https://git.ain.rd.tut.fi/procemplus/amqpmathtoolintegration

global NumOfSimRun     % global variable for the whole Matlab environment specifying the number of simulation runs.
global Handles
global States
global Object
NumOfSimRun=0;
Handles={};
States={};


amqpPropsM = eu.cocop.amqp2math.AmqpPropsManager('localhost','procem-management','guest','guest'); % the specs are for RTDS lab server.
amqpPropsM.setSecure(false);
amqpPropsM.setPort(5672);
amqpPropsM.setExchangeDurable(true); 
amqpPropsM.setExchangeAutoDelete(false);
topicsIn = javaArray('java.lang.String',1);
topicsIn(1) = java.lang.String('Start'); 
amqpConnectorM = eu.cocop.amqp2math.AmqpConnector(amqpPropsM, topicsIn);
disp('Conected to the management exchange')

% Listener
notifier = amqpConnectorM.getNotifierForTopic('Start');
handleObj = handle(notifier, 'CallbackProperties');
set(notifier, 'ListenCallback', @(handleObj, ev)ManagementCallback(handleObj, ev));



