% Copyright 2023 Tampere University.
% This software was developed as a part of doctroal studies of Mehdi Attar, funded by Fortum and Neste Foundation.
% This source code is licensed under the MIT license. See LICENSE in the repository root directory.
% This software can only be deployed by SimCES platform. (https://simcesplatform.github.io/)
% Author: Mehdi Attar <mehdi.attar@tuni.fi>
%
classdef PredictiveGridOptimization < handle
    
    properties
        
        % Start message
        SimulationSpecificExchange
        SimulationId
        StatePredictorId
        SourceProcessId
        OptimizationHorizon
        MaxVoltage
        MinVoltage
        UpperAmberBandVoltage
        LowerAmberBandVoltage
        OverloadingBaseline
        AmberLoadingBaseline
        MarketId
        MarketOpeningTime
        MarketClosingTime
        GridName
        GR
        GX
        DistancesR
        DistancesX
        
        % Initialization (Epoch 1)
        NIS
        CIS
        ForecastLengthCurrent
        ExpectedNumberOfVoltageForecasts
        ExpectedNumberOfCurrentForecasts
        NumberofBuses
        NominalCurrent
        BranchResistance
        BranchReactance
        Susceptance
        RS
        FNM
        SensitivityMatrixR    % [R] matrix for sensitivity analysis according to DOI: 10.1109/ISIE.2010.5637545
        SensitivityMatrixX    % [X] matrix for sensitivity analysis according to DOI: 10.1109/ISIE.2010.5637545
        SensitivityMatrixZ   % [Z] matrix for sensitivity analysis according to DOI: 10.1109/ISIE.2010.5637545
        NISBranchData       % NISBranchData are stored in this property if branch data comes earlier than bus data
        Zbase
        Ibase
        
        % for testing
        BusNameForTest
        BusNodeForTest
        
        % Epoch
        Epoch
        NumberOfReceivedVoltageValues
        NumberOfReceivedCurrentValues
        StartTime
        EndTime
        Today
        x
        
        % Inbbound/outbound message counter
        InboundMessage
        MessageCounterInbound % Its value is continues between Epoches 
        MessageCounterOutbound % Its value is reset in the beginning of each Epoch
        
        % Forecasted grid flows
        VoltageForecasts
        CurrentForecasts

        % Flex need
        FlexNeedDMS    % Flex need on the DMS side is stored in the "FlexNeedDMS" table 
        FlexNeedMarket % Flex need on the market side is stored in the "FlexNeedMarket" table
        
        % Offer
        TotalOfferCounter % Total num of Offers receivd from LFM including empty offers and non-empty ones
        OfferCounter % counter of non-empty offers received from LFM
        Offer   % Offers provided by LFM are stored in "Offer"
        
        % State
        State   % State of the object can either be "Free" or "Busy"
        
        % Flags
        NISBusFlag          
        NISBranchFlag       
        StatePredictorReadinessFlag   
        FlexNeedFlag        
        FlexNeedSentFlag    
        OfferSelectedFlag   
        OfferReceivedFlag  
        SlectedOfferForwardedFlag 
        OfferSelectionTimeFlag
        CustomerIdExistanceFlag
        ReceivedAllVoltageForecastsFlag
        ReceivedAllCurrentForecastsFlag
        NISBusAnalysisFlag
        NISBranchAnalysisFlag
        CISAnalysisFlag
        EmptyOffersFlag
        LFMOperationFlag
        ReadyMessageFlag
        
        % connector to simulation specific exchange (using ProcemPlus lib)
        AmqpConnector  
        
        % Result
        AbstractResult
    end
 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    methods
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Constructor
        
        function obj = PredictiveGridOptimization(SimulationSpecificExchange,SimulationId,PGOName,MonitoredGridId,RS,FNM,OptimizationHorizon,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline,MarketId,MarketOpeningTime,MarketClosingTime,Grid)  
            obj.SimulationSpecificExchange = SimulationSpecificExchange; % Start message
            obj.SimulationId = SimulationId;
            obj.SourceProcessId = PGOName;
            obj.StatePredictorId = MonitoredGridId;
            obj.RS=RS;
                obj.RS=1-((obj.RS)/100);
            obj.FNM=FNM+1;
            obj.OptimizationHorizon=str2num(OptimizationHorizon(3:end-1)); % Following ISO8601 for duration e.g.: "PT36H"
            obj.MaxVoltage=MaxVoltage; % p.u. value
            obj.MinVoltage=MinVoltage; % p.u. value
            obj.UpperAmberBandVoltage=UpperAmberBandVoltage; % p.u. value
            obj.LowerAmberBandVoltage=LowerAmberBandVoltage; % p.u. value
            obj.OverloadingBaseline=OverloadingBaseline;
            obj.AmberLoadingBaseline=AmberLoadingBaseline; 
            obj.MarketId=MarketId;
            obj.MarketOpeningTime=MarketOpeningTime;
            obj.MarketClosingTime=MarketClosingTime;
            obj.GridName=Grid;

            obj.ExpectedNumberOfVoltageForecasts=0;    % Initialization (Epoch 1)
            obj.ExpectedNumberOfVoltageForecasts=0;

            obj.NumberOfReceivedVoltageValues=0;    % Epoch
            obj.NumberOfReceivedCurrentValues=0;

            obj.MessageCounterInbound=0;    % Inbound/outbound message counter
            obj.MessageCounterOutbound=0;
            obj.OfferCounter=0;
            obj.TotalOfferCounter=0;

            obj.NISBusFlag=0;  % Flag is 1 once the Bus data are receievd
            obj.NISBranchFlag=0;  % Flag is 1 once the Branch data are receievd
            obj.StatePredictorReadinessFlag=0;  % Flag is 1 once the Grid is ready
            obj.FlexNeedFlag=0;      % Flag is 1 once there is a need for flexibility
            obj.CustomerIdExistanceFlag=0; % Flag is 1 once there is at least one CustomerId inside the congestion area
            obj.FlexNeedSentFlag=0;  % Flag is 1 once a flex need is sent to LFM
            obj.OfferReceivedFlag=0;  % Flag is 1 once when the expected number of offers has been received
            obj.OfferSelectionTimeFlag=0; % Flag is 1 once the time for selecting the offer is occured
            obj.OfferSelectedFlag=0;  % Flag is 1 once a flex Offer has been selected for congestion management
            obj.SlectedOfferForwardedFlag=0;  % Flag is 1 once an offer is selcted and LFM is informed about that
            obj.ReceivedAllVoltageForecastsFlag=0;
            obj.ReceivedAllCurrentForecastsFlag=0;
            obj.NISBusAnalysisFlag=0;
            obj.NISBranchAnalysisFlag=0;
            obj.CISAnalysisFlag=0;
            obj.EmptyOffersFlag=0;
            obj.BusNameForTest={};
            obj.BusNodeForTest=0;

            obj.State='Free';   % The object's default State is 'Free'
        end
 
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 1
        
        function Done=Main(obj)
            obj.Subscription;
%             obj.ForecastedDataManagement;
            obj.GetMsg;
            if strcmp(obj.State,'Stopped')
                disp("PGO stopped")
                Done=true;
            end
        end

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 2

        function Subscription(obj)
%             AmqpProps = fi.procemplus.amqp2math.AmqpPropsManager('localhost',obj.SimulationSpecificExchange,'guest','guest'); % Based on what is specified in the Start message, PGO listens to that exchange.
            AmqpProps = fi.procemplus.amqp2math.AmqpPropsManager('localhost',obj.SimulationSpecificExchange,'guest','guest');
           % AmqpProps.setSecure(true);
            AmqpProps.setSecure(false);
            AmqpProps.setPort(5672);   % Default AMQP port
           % AmqpProps.setPort(45671);   % Default AMQP port
            AmqpProps.setExchangeDurable(false);    % Uncomment this line if settings in the AMQP broker is activated
            AmqpProps.setExchangeAutoDelete(true);  % Uncomment this line if settings in the AMQP broker is activated
            
            topicsIn = javaArray('java.lang.String',9); % PGO needs to at least listen to 8 different topics as mentioned below
            topicsIn(1) = java.lang.String('SimState'); % PGO needs to SimState topic published by Simulation Manager
            topicsIn(2) = java.lang.String('Status.Ready'); % PGO needs to listen to Status.Ready topic published by of Grid 
            topicsIn(3) = java.lang.String('Status.Error'); % PGO needs to listen to Status.Error topic published by Grid
            topicsIn(4) = java.lang.String('Epoch');    % PGO needs to listen to Epoch topic published by Simulation manager
                ss=string(obj.GridName);
                ss='NetworkForecastState.'+ss+'.Voltage.#';
            topicsIn(5) = java.lang.String(ss); % PGO needs to listen to NetworkState.Voltage.# topic published by Grid. (# is wild card to receive all voltage data)
%            topicsIn(6) = java.lang.String('NetworkForecastState.Current.#'); % PGO needs to listen to NetworkState.Current.# topic published by Grid. (# is wild card to receive all voltage data)
            topicsIn(6) = java.lang.String('Init.NIS.NetworkBusInfo');  % PGO needs to listen to Init.NIS.NetworkBusInfo topic published by Grid in the Epoch 1 
            topicsIn(7) = java.lang.String('Init.NIS.NetworkComponentInfo');    % PGO needs to listen to Init.NIS.NetworkComponentInfo topic published by Grid in the Epoch 1
            topicsIn(8) = java.lang.String('Init.CIS.CustomerInfo');    % PGO needs to listen to Init.CIS.CustomerInfo topic published by Grid in the Epoch 1 to know the relation between flexibility needs and customerId
                ss = char(strcat('LFMOffering.',string(obj.SourceProcessId)));
            topicsIn(9) = java.lang.String(ss);    % PGO needs to listen to LFMOffering topic to get its required flexibility
            
            obj.AmqpConnector = fi.procemplus.amqp2math.AmqpTopicConnectorSync(AmqpProps, topicsIn); % using procemplus API for RabbitMQ broker connection. it is a synch API
            disp(['connected to the simulation specific exchange:' obj.SimulationSpecificExchange])
            disp(['SimulationId:' obj.SimulationId])
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 3
        
        function Out=GetMsg(obj)    % since we have a synch API, for receiving new messages, we need to call the get function
            while 1>0
                obj.State='Free';
                message = obj.AmqpConnector.getMessage();
                if ~isempty(message)
                    mystr = message.getBody();
                    str = char(mystr)';  %    Making the input into a character array
                    obj.InboundMessage = jsondecode(str); % decoding JSON data. please note that jsondecode for Matlab versions 2018 and later receives only row vectors.(that's why str is str')
                    %a=jsondecode(str);
                    clear message mystr str
                    obj.MessageCounterInbound=obj.MessageCounterInbound+1; % inbound message counter
                    obj.Listener;
                else
                    pause(0.2);   % in order not to over load Matlab
                end
                if strcmp(obj.State,'Stopped')
                   Out=true; 
                end
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 4
        
        function Listener(obj)
            if strcmp(obj.State,'Free')
                obj.State='Busy';
                if strcmp(obj.SimulationId,obj.InboundMessage.SimulationId) % making sure that incoming message belong to the current simulation run

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When SimulationManager publishes the SimState message

                   if strcmp(obj.InboundMessage.Type,'SimState')
                        if strcmp(obj.InboundMessage.SimulationState,'running')
                            obj.AbstractResult.Type='Status';
                            obj.AbstractResult.SimulationId=obj.SimulationId{1};
                            obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                            obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                                s = strcat('PredictedGridOptimization',num2str(obj.MessageCounterOutbound)); % Making the number of outbound messages string to create MessageId
                            obj.AbstractResult.MessageId=s;
                                t = datetime('now', 'TimeZone', 'UTC');
                                t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                            obj.AbstractResult.Timestamp=t;
                            obj.AbstractResult.EpochNumber=0;
                            obj.Epoch=0;         % it sets the Epoch number in the object
                            obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                            obj.AbstractResult.Value='ready';  
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                            disp('PGO reported "ready" message to Simulation Manager as response to SimState message')
                            disp(['SimulationId:' obj.SimulationId])
                            MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                            MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                            obj.AmqpConnector.sendMessage('Status.Ready', MyBytesOut); % The topic is "Status.Ready" that PGO publishes to
                               ss = char(strcat('PgoReady.',string(obj.SourceProcessId))); % just for testing
                            obj.AmqpConnector.sendMessage(ss, MyBytesOut); % The topic is "Status.Ready" that PGO publishes to
                            clear t s MyStringOut MyBytesOut ss
                            obj.AbstractResult=[];
                        elseif strcmp(obj.InboundMessage.SimulationState,'stopped')
                            obj.State='Stopped';    % Turn the PGO state to stopped.
                        end
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes the Status message for Epoches>0

                   if strcmp(obj.InboundMessage.Type,'Status')
                      if strcmp(obj.InboundMessage.SourceProcessId,obj.StatePredictorId)      % just analyse the status message that is published by Grid
                          if obj.InboundMessage.EpochNumber~=0     % For Epoches > 0 
                              disp(['PGO received "ready" message from ',num2str(obj.StatePredictorId)])
                              obj.StatusReadinessGrid; % one of the requirements of PGO readiness is grid's readiness
                          end
                      end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When SimulationManager publishes the Epoch message 

                   if strcmp(obj.InboundMessage.Type,'Epoch')
                       if obj.InboundMessage.EpochNumber>obj.Epoch
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%') % for visualization purposes
                            disp(['Epoch number=' num2str(obj.InboundMessage.EpochNumber)])
                            disp(['Start Time=' obj.InboundMessage.StartTime])
                            disp(['End Time=' obj.InboundMessage.EndTime])
                            disp(['SimulationId:' obj.SimulationId])
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                            obj.Epoch=obj.InboundMessage.EpochNumber;              % Making the Epoch number the Object's property
                            obj.StartTime=char(obj.InboundMessage.StartTime);
                            obj.EndTime=char(obj.InboundMessage.StartTime);
                                x=char(obj.StartTime);
                                today=x(1:10);
                            obj.Today=datetime(today,'InputFormat','yyyy-MM-dd');
                            clear x
                            obj.NumberOfReceivedVoltageValues=0;    % Resetting the number of received forecasted voltage values
                            obj.NumberOfReceivedCurrentValues=0;    % Resetting the number of received forecasted current values
                            obj.MessageCounterOutbound=0;   % Resetting the number of outbound message for each Epoch
                            obj.ForecastLengthCurrent=0; % Resetting the length of the forecasts- current
                            obj.OfferCounter=0;
                            obj.TotalOfferCounter=0;

                            obj.StatePredictorReadinessFlag=0;  % Resetting the grid readiness flag. The default is 0 showing that the grid is not yet ready.
                            obj.OfferReceivedFlag=0; % Resetting the available offer flag. The defalut is 0 showing that, currently, there is no available offer in the market
                            obj.OfferSelectedFlag=0;  % Resetting the offer selected flag. The default is 0 showing that any offer has not yet been selected duting the running Epoch.
                            obj.FlexNeedSentFlag=0;
                            obj.EmptyOffersFlag=0;  % Resetting the Flag. The default is 0 in the start of the Epoch.1 shows that all received offers are empty.
                            obj.OfferSelectionTimeFlag=0; % Resetting the flag. The default is 0 showing that the time for selecting the offers has not occured yet.
                            obj.CustomerIdExistanceFlag=0; % Resetting the Flag. The default is 0 in the start of the Epoch. 1 shows that there is CustomerId within the congestion need. 2 means that there is no CustomerId within the flex need.
                            obj.LFMOperationFlag=0;    % Resetting the Flag. The default is 0 in the start of the Epoch. 1 shows that market is open.
                            obj.ReadyMessageFlag=0;        % Resetting the glag. The default is 0 in the start of the Epoch. 1 shows that the PGO's ready message has been sent.
                            
                            
                            obj.VoltageForecasts=[];
                            obj.VoltageForecasts=struct;
                            obj.Offer=[];       % resetting the offers for in every Epoch.
                            obj.Offer=struct;
                            obj.Offer=struct2table(obj.Offer);
                            
                            if strcmp(class(obj.FlexNeedMarket),"table")
                                for i=1:height(obj.FlexNeedMarket)
                                    obj.FlexNeedMarket(i,:).OfferCount=0;
                                    obj.FlexNeedMarket(i,:).NumOfReceivedOffers=0;                            
                                    obj.FlexNeedMarket(i,:).Status="None";
                                    obj.FlexNeedMarket(i,:).OfferId="None";
                                end
                            end
           
                            x=obj.StartTime(12:13);
                            obj.x=str2double(x);
                            clear x
                            if obj.x>=obj.MarketOpeningTime && obj.x<obj.MarketClosingTime
                               obj.LFMOperationFlag=1;
                               disp('In this epoch, the LFM is open')
                            end
                            if obj.x<obj.MarketOpeningTime || obj.x>obj.MarketClosingTime
                                obj.FlexNeedFlag=0;     % Resetting the flex need flag. The default is 0 when Epoch starts. The value is 1 when there is a need. The value is 2 there is no flex need.
                                obj.FlexNeedDMS=[];
                                obj.FlexNeedDMS=struct;
                            end
                       end
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes Bus data message- NIS

                   if strcmp(obj.InboundMessage.Type,'Init.NIS.NetworkBusInfo')
                       %if strcmp(obj.InboundMessage.SourceProcessId,obj.StatePredictorId)
                           if obj.NISBusAnalysisFlag==0 
                            obj.NISBusAnalysis;
                           end
                       %end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes Branch data message- NIS

                   if strcmp(obj.InboundMessage.Type,'Init.NIS.NetworkComponentInfo')
                       %if (strcmp(obj.InboundMessage.SourceProcessId,obj.StatePredictorId))
                           if obj.NISBranchAnalysisFlag==0
                            obj.NISBranchAnalysis;
                           end
                       %end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes Customer data message- CIS

                   if strcmp(obj.InboundMessage.Type,'Init.CIS.CustomerInfo')
                       %if (strcmp(obj.InboundMessage.SourceProcessId,obj.StatePredictorId))
                           if obj.CISAnalysisFlag==0
                            obj.CISAnalysis;
                           end
                       %end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid published the network's voltage forecasts

                   if strcmp(obj.InboundMessage.Type,'NetworkForecastState.Voltage')
                       %if obj.x==obj.MarketOpeningTime
                       if obj.LFMOperationFlag==1
                           if obj.InboundMessage.Node<4
                               VoltageViolationFlag=0;
                               obj.ReceivedAllVoltageForecastsFlag=0;
                               obj.NumberOfReceivedVoltageValues=obj.NumberOfReceivedVoltageValues+1;
                               disp(['Voltage Num:' string(obj.NumberOfReceivedVoltageValues)])
                               %ReceivedVoltageValues=obj.NumberOfReceivedVoltageValues
                               
                               From=1+(obj.OptimizationHorizon*(obj.NumberOfReceivedVoltageValues-1));
                               To=obj.NumberOfReceivedVoltageValues*obj.OptimizationHorizon;
                               TempStatus=string(zeros(obj.OptimizationHorizon,1));
                               TempViolation=zeros(obj.OptimizationHorizon,1);
                               TempVioDir=string(zeros(obj.OptimizationHorizon,1));

                               BusName=string(obj.InboundMessage.Bus);
%                                if strcmp(BusName,"scd_101990")
%                                    obj.InboundMessage.Forecast.Series.Magnitude.Values=(obj.InboundMessage.Forecast.Series.Magnitude.Values)*1.025;
%                                end
                               Node=obj.InboundMessage.Node;
                               Row = find(string(obj.NIS.OriginalBusNames(:,1)) == obj.InboundMessage.Bus); % finding the Row of the Bus
                               NominalVoltage=obj.NIS.Bus(Row,10);  % kV
                               Vmin1=(obj.MinVoltage+obj.LowerAmberBandVoltage)*NominalVoltage;  % kV
                               Vmax1=(obj.MaxVoltage-obj.UpperAmberBandVoltage)*NominalVoltage; % kV
                               Vmin2=obj.MinVoltage*NominalVoltage;  % kV
                               Vmax2=obj.MaxVoltage*NominalVoltage; % kV
                               %Voltages=obj.InboundMessage.Forecast.Series.Magnitude.Values
                               %%%%% Voltage level analysis
                               for i=1:obj.OptimizationHorizon
                                   VoltageViolationFlag=0;
                                   if (obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)>Vmax1)
                                       if (obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)<Vmax2)
                                           Status="close-to-limits";
                                           Violation=0;
                                           VoltageViolationFlag=1;
                                           VioDir="";
                                       end
                                   end
                                   if obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)>Vmax2
                                       Status="unacceptable";
                                       Violation=((obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)-Vmax2)/NominalVoltage);
                                       VoltageViolationFlag=1;
                                       VioDir="over";
                                   end
                                   if obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)<Vmin1
                                       if obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)>Vmin2
                                           Status="close-to-limits";
                                           Violation=0;
                                           VoltageViolationFlag=1;
                                           VioDir="";
                                       end
                                   end
                                   if obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1)<Vmin2
                                       Status="unacceptable";
                                       Violation=((Vmin2-obj.InboundMessage.Forecast.Series.Magnitude.Values(i,1))/NominalVoltage);
                                       VoltageViolationFlag=1;
                                       VioDir="under";
                                   end
                                   if VoltageViolationFlag==0
                                       Status="acceptable";
                                       Violation=0;
                                       VioDir="";
                                   end
                                   TempStatus(i,1)=Status;
                                   TempViolation(i,1)=Violation;
                                   TempVioDir(i,1)=VioDir;
                               end
                                warning('off')     % this is needed to supress the warning messages in command window. The reason of the warning is that by adding new rows to the VoltageForecast table, some columns still donot have value.
                                obj.VoltageForecasts.Time(From:To,:)=obj.InboundMessage.Forecast.TimeIndex(1:obj.OptimizationHorizon,:);
                                obj.VoltageForecasts.Voltage(From:To,:)=obj.InboundMessage.Forecast.Series.Magnitude.Values(1:obj.OptimizationHorizon,:);
                                obj.VoltageForecasts.Violation(From:To,:)=TempViolation;
                                obj.VoltageForecasts.BusNumber(From:To,:)=Row;
                                obj.VoltageForecasts.BusName(From:To,:)=BusName;
                                obj.VoltageForecasts.Node(From:To,:)=Node;
                                obj.VoltageForecasts.Angle(From:To,:)=obj.InboundMessage.Forecast.Series.Angle.Values(1:obj.OptimizationHorizon,:);
                                obj.VoltageForecasts.Status(From:To,:)=TempStatus;
                                obj.VoltageForecasts.VioDirection(From:To,:)=TempVioDir;
                                obj.VoltageForecasts.CongestionNumber(From:To,:)=0;
%                                 if ReceivedVoltageValues==1077
%                                     Expected=obj.ExpectedNumberOfVoltageForecasts
%                                     Received=length(obj.VoltageForecasts.Time)
%                                 end
                                clear Row NominalVoltage Vmin1 Vmax1 Vmin2 Vmax2 TempVioDir TempViolation TempStatus From To VoltageViolationFlag ReceivedVoltageValues  
                                %%%%% Deleting the rows without violation when all the voltage forecasts are received

                                if obj.NumberOfReceivedVoltageValues==(3*obj.NumberofBuses)
                                    disp('All voltage forecasts were received')
                                    obj.ReceivedAllVoltageForecastsFlag=1;
                                    n=length(obj.VoltageForecasts.Time);   % It gives the number of violations
%                                     x=char(obj.StartTime);
%                                     Today=x(1:10);
%                                     Today=datetime(Today,'InputFormat','yyyy-MM-dd');
%                                     NextDayStart=dateshift(Today,'start','day','next');  
%                                     NextDayEnd=dateshift(NextDayStart,'start','day','next');
                                    
%                                     if ~isempty(n)
%                                         for i=1:1:length(obj.VoltageForecasts.Time)
%                                             if obj.VoltageForecasts.Violation(i)~=0
%                                                 x=char(obj.VoltageForecasts.Time(i));
%                                                 x=x(1:10);
%                                                 x=datetime(x,'InputFormat','yyyy-MM-dd');
%                                                 if x>NextDayEnd
%                                                     obj.VoltageForecasts.Violation(i)=0;  % Deleting the rows outsidet the market operation window
%                                                 elseif x<NextDayStart
%                                                     obj.VoltageForecasts.Violation(i)=0;  % Deleting the rows outsidet the market operation window
%                                                 else
%                                                 end
%                                             end
%                                         end
%                                     end

                                    if ~isempty(n)
                                        for i=1:1:length(obj.VoltageForecasts.Time)
                                            if obj.VoltageForecasts.Violation(i)~=0
                                                day=char(obj.VoltageForecasts.Time(i));
                                                %time=str2double(day(12:13));
                                                day=day(1:10);
                                                day=datetime(day,'InputFormat','yyyy-MM-dd');
                                                if day==obj.Today
                                                    %if time<=obj.MarketClosingTime
                                                        obj.VoltageForecasts.Violation(i)=0;
                                                    %end
                                                end
%                                                 if day==NextDayStart
%                                                     if time>=obj.MarketOpeningTime  
%                                                         obj.VoltageForecasts.Violation(i)=0;  % Deleting the rows outsidet the market operation window
%                                                     end
%                                                 end
                                            end
                                        end
                                    end
                                    RowWithVio=find(obj.VoltageForecasts.Violation~=0);
                                    obj.VoltageForecasts=struct2table(obj.VoltageForecasts);
                                    if ~isempty(RowWithVio)
                                        n=length(RowWithVio);
                                        for k=1:1:n
                                            obj.VoltageForecasts(k,:)=obj.VoltageForecasts(RowWithVio(k),:);
                                        end
                                        s=obj.VoltageForecasts(1:n,:);
                                        obj.VoltageForecasts=struct;
                                        obj.VoltageForecasts=struct2table(obj.VoltageForecasts);
                                        obj.VoltageForecasts=s;
                                        
                                        clear s
                                        % voltages that donot have violation are deleted
                                    end
                                    RowWithVio=find(obj.VoltageForecasts.Violation~=0);
                                    if ~isempty(RowWithVio)
                                        obj.FlexNeedFlag=1; % It means there is a need for flex
                                        clear RowWithVio
                                        if  obj.ReceivedAllCurrentForecastsFlag==1 
                                            disp('Flex is needed- voltage')
                                            
                                            obj.VoltageForecasts=sortrows(obj.VoltageForecasts); % Sorting the rows based on the time first, then violation etc
                                            obj.FlexibilityNeed;
                                        end
                                    else
                                      obj.FlexNeedFlag=2;  % It means that Voltages are received, but there is no flex need
                                      obj.StatusReadiness;
                                    end
                                end
                           end
                       else
                           obj.StatusReadiness;
                       end
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid published the network's current forecasts

                   if strcmp(obj.InboundMessage.Type,'NetworkForecastState.Current')
                       obj.NumberOfReceivedCurrentValues=obj.NumberOfReceivedCurrentValues+1;
                       disp('Current forecast state is coming')
                       ReceivedNumberOfCurrent=obj.NumberOfReceivedCurrentValues
                       obj.ReceivedAllCurrentForecastsFlag=0;

                       obj.ForecastLengthCurrent=length(obj.InboundMessage.Forecast.TimeIndex);
%                            B=obj.ForecastLengthCurrent
                       if obj.ForecastLengthCurrent~=obj.OptimizationHorizon
                           disp('The length of forecasted current is not equal to the length of the forecasted voltage');
                       end
                       From=1+(obj.ForecastLengthCurrent*(obj.NumberOfReceivedCurrentValues-1));
                       To=obj.NumberOfReceivedCurrentValues*obj.ForecastLengthCurrent;
                       TempStatusSendingEnd=string(zeros(obj.ForecastLengthCurrent,1));
                       TempStatusReceivingEnd=string(zeros(obj.ForecastLengthCurrent,1));
                       TempViolationSendingEnd=string(zeros(obj.ForecastLengthCurrent,1));
                       TempViolationReceivingEnd=string(zeros(obj.ForecastLengthCurrent,1));

                       Row = find(strcmp(string(obj.NIS.DeviceId(:,1)),string(obj.InboundMessage.DeviceId)));
                       disp(['DeviceId:' string(obj.InboundMessage.DeviceId)]);
                       NominalCurrent=obj.NominalCurrent(Row,1);
                       Imax1=NominalCurrent*obj.AmberLoadingBaseline;
                       Imax2=NominalCurrent*obj.OverloadingBaseline;


                            %%%%% Current level analysis
                       for i=1:obj.ForecastLengthCurrent
                           if (obj.InboundMessage.Forecast.Series.MagnitudeSendingEnd.Values(i,1)>Imax1)
                               if (obj.InboundMessage.Forecast.Series.MagnitudeSendingEnd.Values(i,1)<Imax2)
                                   StatusSendingEnd="close-to-limits";
                                   ViolationSendingEnd=0;
                               end
                           end
                           if (obj.InboundMessage.Forecast.Series.MagnitudeReceivingEnd.Values(i,1)>Imax1)
                               if (obj.InboundMessage.Forecast.Series.MagnitudeReceivingEnd.Values(i,1)<Imax2)
                                   StatusReceivingEnd="close-to-limits";
                                   ViolationReceivingEnd=0;
                               end
                           end
                           %%
                           if obj.InboundMessage.Forecast.Series.MagnitudeSendingEnd.Values(i,1)>Imax2
                               StatusSendingEnd="unacceptable";
                               ViolationSendingEnd=obj.InboundMessage.Forecast.Series.MagnitudeSendingEnd.Values(i,1)-Imax2;
                           end
                           if obj.InboundMessage.Forecast.Series.MagnitudeReceivingEnd.Values(i,1)>Imax2
                               StatusReceivingEnd="unacceptable";
                               ViolationReceivingEnd=obj.InboundMessage.Forecast.Series.MagnitudeReceivingEnd.Values(i,1)-Imax2;
                           end
                           %%
                           if (obj.InboundMessage.Forecast.Series.MagnitudeSendingEnd.Values(i,1)<Imax1)
                               StatusSendingEnd="acceptable";
                               ViolationSendingEnd=0;
                           end 
                           if (obj.InboundMessage.Forecast.Series.MagnitudeReceivingEnd.Values(i,1)<Imax1)
                               StatusReceivingEnd="acceptable";
                               ViolationReceivingEnd=0;
                           end 
                           TempStatusSendingEnd(i,1)=StatusSendingEnd;
                           TempViolationSendingEnd(i,1)=ViolationSendingEnd;
                           TempStatusReceivingEnd(i,1)=StatusReceivingEnd;
                           TempViolationReceivingEnd(i,1)=ViolationReceivingEnd;

                        end
                        obj.CurrentForecasts.Time(From:To,:)=obj.InboundMessage.Forecast.TimeIndex;
                        obj.CurrentForecasts.DeviceId(From:To,:)=obj.InboundMessage.DeviceId;
                        obj.CurrentForecasts.Phase(From:To,:)=obj.InboundMessage.Phase;
%                             obj.CurrentForecasts.MangnitudeSendingEnd(From:To,:)=obj.InboundMessage.Forecast.Series.MangnitudeSendingEnd.Values;
%                             obj.CurrentForecasts.MangnitudeReceivingEnd(From:To,:)=obj.InboundMessage.Forecast.Series.MangnitudeReceivingEnd.Values;
%                             obj.CurrentForecasts.AngleSendingEnd(From:To,:)=obj.InboundMessage.Forecast.Series.AngleSendingEnd.Values;
%                             obj.CurrentForecasts.AngleReceivingEnd(From:To,:)=obj.InboundMessage.Forecast.Series.AngleReceivingEnd.Values;
                        obj.CurrentForecasts.StatusSendingEnd(From:To,:)=TempStatusSendingEnd;
                        obj.CurrentForecasts.ViolationSendingEnd(From:To,:)=TempViolationSendingEnd;
                        obj.CurrentForecasts.StatusReceivingEnd(From:To,:)=TempStatusReceivingEnd;
                        obj.CurrentForecasts.ViolationReceivingEnd(From:To,:)=TempViolationReceivingEnd;

                        % Deleting the rows without violation

                        if length(obj.CurrentForecasts.Time)==(obj.ExpectedNumberOfCurrentForecasts*obj.ForecastLengthCurrent)
                            disp('All current forecasts were received')
                            ExpectedCurrentValues=obj.ExpectedNumberOfCurrentForecasts*obj.ForecastLengthCurrent
                            ReceivedCurrentValues=length(obj.CurrentForecasts.Time)
                            obj.ReceivedAllCurrentForecastsFlag=1;
                            RowWithoutVioSending=find(obj.CurrentForecasts.ViolationSendingEnd==0);
                            RowWithoutVioReceiving=find(obj.CurrentForecasts.ViolationReceivingEnd==0);

                            A=length(RowWithoutVioSending);
                            B=length(RowWithoutVioReceiving);

                            if A>=B % Assuring that the number of current violations are max
                                RowWithoutVio=RowWithoutVioReceiving;
                            elseif B>A
                                RowWithoutVio=RowWithoutVioSending;
                            end

                            if ~isempty(RowWithoutVio)
                                n=length(RowWithoutVio);
                                for k=1:1:n
                                    obj.CurrentForecasts((RowWithoutVio(k)),:)=[];
                                    RowWithoutVio=RowWithoutVio(:,1)-1;
                                end
                            end

                            % buying flex from LFM will be from 00:00 next day to 23:59

                            x=obj.StartTime;
                            type=class(x);
                            if strcmp(type,"string")
                                x=char(x);
                            end

                            Today=x(1:10);
                            Today=datetime(Today,'InputFormat','yyyy-MM-dd');

                            NextDayStart=dateshift(Today,'start','day','next');     
                            NextDayEnd=dateshift(NextDayStart,'start','day','next');

                            n=length(obj.CurrentForecasts.Time)   % It gives the number of violations
%                                 if ~isempty(n)
%                                     for i=1:1:n
%                                         x=obj.CurrentForecasts.Time(i);
%                                         type=class(x);
%                                         if strcmp(type,"string")
%                                             x=char(x);
%                                         end
%                                         x=x(1:10);
%                                         x=datetime(x,'InputFormat','yyyy-MM-dd');
%                                         if x<=NextDayEnd
%                                             obj.CurrentForecasts(i,:)=[];  % Deleting the rows outsidet the market operation window
%                                         end
%                                         if x>=NextDayStart
%                                             obj.CurrentForecasts(i,:)=[];  % Deleting the rows outsidet the market operation window
%                                         end
%                                     end
%                                 end
                            if  obj.ReceivedAllVoltageForecastsFlag==1
                                if obj.FlexNeedFlag==1
%                                         if isempty(n)
%                                             obj.FlexNeedFlag=0;    % since no congestion exist, flex need is not required at all :)
%                                             disp('Flex is not needed- current')
%                                             obj.StatusReadiness;
%                                         else
                                        disp('Flex is needed- current')
                                        obj.VoltageForecasts=sortrows(obj.VoltageForecasts); % Sorting the rows based on the time first, then violation etc
                                        obj.FlexibilityNeed;
%                                         end
                                end
                            end


%                                 if isempty(obj.CurrentForecasts)
%                                     obj.FlexNeedFlag=0;    % since no congestion exist, flex need is not required at all :)
%                                 else
%                                     obj.FlexNeedFlag=1;
%                                     obj.VoltageForecasts=sortrows(obj.VoltageForecasts); % Sorting the rows based on the time first, then violation etc
%                                     obj.FlexibilityNeed;
%                                 end
                        end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When LFM publishes the available offers of energy communities (ECs)

                   if strcmp(obj.InboundMessage.Type,'LFMOffering')
                       obj.LFMOffers;
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                else   % Sending a warning if the inbound message doesnot match the SimulationId- error handling feature
                    obj.State='Free';
                    obj.AbstractResult.Type='FlexibilityNeed';
                    obj.AbstractResult.SimulationId=obj.SimulationId{1};
                    obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                    obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
                    obj.AbstractResult.MessageId=s;
                    obj.AbstractResult.EpochNumber=obj.Epoch;
                    obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    obj.AbstractResult.Timestamp=t;
                    obj.AbstractResult.Warnings='warning.input';
                    MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                    MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                    obj.AmqpConnector.sendMessage('DMSNetworkStatus', MyBytesOut);
                    clear s t MyStringOut MyBytesOut
                    obj.AbstractResult=[];
                end
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 5
        
        function NISBusAnalysis(obj)
            obj.State='Busy'; % The NIS structure is inspired by Power System Toolbox format. Please refer to that to know how data are organized in Bus and Branch matrixes.  
            obj.NumberofBuses=numel(obj.InboundMessage.BusName);
            obj.ExpectedNumberOfVoltageForecasts=obj.NumberofBuses*3*obj.OptimizationHorizon;  % Bus*Node*length of time series. change the Node value if the network is not three phase
            NumberofBusColumn=14;
            obj.NIS.BusUnits=cell(obj.NumberofBuses,NumberofBusColumn); 
            obj.NIS.OriginalBusNames=cell(obj.NumberofBuses,1);

            %%%%% Bus name and Number

            RootBusRow=find(strcmp(obj.InboundMessage.BusType(:,1),"root"));
            if RootBusRow>1    % bring the root bus to row number 1 
                obj.InboundMessage.BusType([1 RootBusRow],1)=obj.InboundMessage.BusType([RootBusRow 1],1);
                obj.InboundMessage.BusName([1 RootBusRow],1)=obj.InboundMessage.BusName([RootBusRow 1],1);
                obj.InboundMessage.BusVoltageBase.Values([1 RootBusRow],1)=obj.InboundMessage.BusVoltageBase.Values([RootBusRow 1],1);
            end
            obj.NIS.OriginalBusNames=cellstr(obj.InboundMessage.BusName);
            obj.NIS.Bus(:,1)=(1:length(obj.InboundMessage.BusName));

            %%%%% Bus Type

            for i=1:1:obj.NumberofBuses   % Enumeration
                if strcmp(string(obj.InboundMessage.BusType(i,1)),"root")
                    obj.InboundMessage.BusType(i,1)=cellstr('3');
                elseif strcmp(string(obj.InboundMessage.BusType(i,1)),"dummy")
                    obj.InboundMessage.BusType(i,1)=cellstr('1');
                elseif strcmp(string(obj.InboundMessage.BusType(i,1)),"usage-point")
                    obj.InboundMessage.BusType(i,1)=cellstr('1');
                end
            end

            obj.NIS.Bus(:,2)=str2double(obj.InboundMessage.BusType);

             %%%%% Unit of measure

            if strcmp(obj.InboundMessage.BusVoltageBase.UnitOfMeasure,'kV')
                obj.NIS.BusUnits(:,10)=cellstr('kV');
                elseif strcmp(obj.InboundMessage.BusVoltageBase.UnitOfMeasure,'V')
                    obj.NIS.BusUnits(:,10)=cellstr('V');
            end

            %%%%% Bus voltage base

            obj.NIS.Bus(:,10)=obj.InboundMessage.BusVoltageBase.Values; % kV values

            %%%%% Voltage min and max

            obj.NIS.Bus(:,12)=obj.MinVoltage; % p.u. values
            obj.NIS.Bus(:,13)=obj.MaxVoltage; % p.u. values
            disp('Network initialization of the Bus matrix was done')
            obj.NISBusAnalysisFlag=1;
            disp(['SimulationId:' obj.SimulationId])
            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            obj.NISBusFlag=1;
            if obj.NISBranchFlag==1 % Assuring that first obj.NIS.Bus is created and after that obj.NIS.Branch is created 
                obj.NISBranchAnalysis;
            else
                obj.State='Free';
                obj.StatusReadiness;
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 6        
        
        function NISBranchAnalysis(obj)
            obj.State='Busy';
            if obj.NISBusFlag==1
               if obj.NISBranchFlag==1 % It means that NIS.NetworkBusInfo message has arrived earlier than NIS.NetworkBusInfo message
                   obj.InboundMessage=obj.NISBranchData;
               end
                obj.NIS.Sbase.Value=obj.InboundMessage.PowerBase.Value;
                obj.NIS.Sbase.UnitofMeasure=obj.InboundMessage.PowerBase.UnitOfMeasure;
                NumberofBranches=length(obj.InboundMessage.SendingEndBus);
                if NumberofBranches~=obj.NumberofBuses-1
                   disp("The distribution network is not radial") 
                end
                obj.ExpectedNumberOfCurrentForecasts=NumberofBranches*3;

                obj.NumberOfReceivedCurrentValues= obj.ExpectedNumberOfCurrentForecasts; % just for testing since now PGO donot listen to current forecasts
                obj.ReceivedAllCurrentForecastsFlag=1;

                NumberOfBranchColumn=12;
                obj.NIS.Branch=zeros(NumberofBranches,NumberOfBranchColumn);
                obj.NIS.BranchUnits=cell(NumberofBranches,NumberOfBranchColumn);
                obj.NIS.DeviceId=cell(NumberofBranches,1);
                obj.NIS.OriginalNameofSendingEndBus=cell(NumberofBranches,1);
                obj.NIS.OriginalNameofReceivingEndBus=cell(NumberofBranches,1);

                SourceBusName=obj.NIS.OriginalBusNames(1);
                RootBusRow=find(string(obj.InboundMessage.SendingEndBus(:))==string(SourceBusName));
                if RootBusRow>1 % Assuring that the first line of the NIS.NetworkComponenetInfo starts with root bus (the change is needed because sensitivity analysis assumes that the first row contains the root bus)
                    obj.InboundMessage.DeviceId([1 RootBusRow],1)=obj.InboundMessage.DeviceId([RootBusRow 1],1);
                    obj.InboundMessage.SendingEndBus([1 RootBusRow],1)=obj.InboundMessage.SendingEndBus([RootBusRow 1],1);
                    obj.InboundMessage.ReceivingEndBus([1 RootBusRow],1)=obj.InboundMessage.ReceivingEndBus([RootBusRow 1],1);
                    obj.InboundMessage.Resistance.Values([1 RootBusRow],1)=obj.InboundMessage.Resistance.Values([RootBusRow 1],1);
                    obj.InboundMessage.Reactance.Values([1 RootBusRow],1)=obj.InboundMessage.Reactance.Values([RootBusRow 1],1);
                    obj.InboundMessage.ShuntAdmittance.Values([1 RootBusRow],1)=obj.InboundMessage.ShuntAdmittance.Values([RootBusRow 1],1);
                    obj.InboundMessage.ShuntConductance.Values([1 RootBusRow],1)=obj.InboundMessage.ShuntConductance.Values([RootBusRow 1],1);
                    obj.InboundMessage.RatedCurrent.Values([1 RootBusRow],1)=obj.InboundMessage.RatedCurrent.Values([RootBusRow 1],1);
                end
                obj.NIS.OriginalNameofSendingEndBus=cellstr(obj.InboundMessage.SendingEndBus);
                obj.NIS.OriginalNameofReceivingEndBus=cellstr(obj.InboundMessage.ReceivingEndBus);
                %%%%% 

                for i=1:NumberofBranches  % since buses are named when NetworkBusInfo is arrived, then the same bus names for branches are used.
                    A=string(obj.NIS.OriginalNameofSendingEndBus(i,1));
                    row=find(strcmp(string(obj.NIS.OriginalBusNames),A)); % function "find" only acts on string arrays
                    obj.NIS.Branch(i,1)=row;
                    B=string(obj.NIS.OriginalNameofReceivingEndBus(i,1));
                    row=find(strcmp(string(obj.NIS.OriginalBusNames),B));
                    obj.NIS.Branch(i,2)=row;
                end

                obj.NIS.Branch(:,3)=obj.InboundMessage.Resistance.Values;
                obj.NIS.BranchUnits(:,3)=cellstr(obj.InboundMessage.Resistance.UnitOfMeasure);

                obj.NIS.Branch(:,4)=obj.InboundMessage.Reactance.Values;
                obj.NIS.BranchUnits(:,4)=cellstr(obj.InboundMessage.Reactance.UnitOfMeasure);

                obj.NIS.Branch(:,5)=obj.InboundMessage.ShuntAdmittance.Values;
                obj.NIS.BranchUnits(:,5)=cellstr(obj.InboundMessage.ShuntAdmittance.UnitOfMeasure);

                obj.NIS.Branch(:,6)=obj.InboundMessage.ShuntConductance.Values;
                obj.NIS.BranchUnits(:,6)=cellstr(obj.InboundMessage.ShuntConductance.UnitOfMeasure);

                obj.NIS.Branch(:,12)=obj.InboundMessage.RatedCurrent.Values;
                obj.NIS.BranchUnits(:,12)=cellstr(obj.InboundMessage.RatedCurrent.UnitOfMeasure);
                obj.NIS.DeviceId=cellstr(obj.InboundMessage.DeviceId);

                %%%%% Calculation of the base values of current and impedance

                Ibase=zeros(NumberofBranches,1);
                obj.NominalCurrent=zeros(NumberofBranches,1);
                Zbase=zeros(NumberofBranches,1);
                obj.BranchResistance=zeros(NumberofBranches,1);

                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'kV.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'V')
                        for i=1:1:NumberofBranches
                            Ibase(i,1)=1000*(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10))); %Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);
                            Zbase(i,1)=obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1)); %Zbase
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'V.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'kV')
                         for i=1:1:NumberofBranches
                            Ibase(i,1)=0.001*(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10))); % Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12); % Ibase*ReatedCurrent
                            Zbase(i,1)=1000*(obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1))); %Zbase
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                         end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'V.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'V')
                        for i=1:1:NumberofBranches
                            Ibase(i,1)=(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10)));  % Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);
                            Zbase(i,1)=(obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1)));
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'kV.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'kV')
                        for i=1:1:NumberofBranches % Sbase="kV.A", Vbase="kV"
                            SendingEndBusName=obj.InboundMessage.SendingEndBus(i);
                            BusNumber=find(strcmp(obj.NIS.OriginalBusNames,SendingEndBusName));
                            obj.Ibase(i,1)=(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(BusNumber,10)));  % Ibase(A)=Sbase/sqrt(3)*BusVoltageBase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);  % NominalCurrent(A)=Ibase(A)*RatedCurrent(p.u.)
                            obj.Zbase(i,1)=1000*(obj.NIS.Bus(BusNumber,10)/(sqrt(3)*Ibase(i,1))); %Zbase=1000(BusVoltageBase(kV)/sqrt(3)*Ibase(A))
                            %obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3); % Branch resistance in Ohm
                            obj.BranchResistance(i,1)=obj.NIS.Branch(i,3); % Branch resistance in p.u.                           
                            obj.BranchReactance(i,1)=obj.NIS.Branch(i,4); % Branch reactance in p.u.
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                format long
%                 Branchresistancepu=obj.BranchResistance(:,1);
%                 BranchReactance=obj.BranchReactance(:,1);
%                 From=obj.NIS.OriginalNameofSendingEndBus(:,1);
%                 To=obj.NIS.OriginalNameofReceivingEndBus(:,1);
%                 Zbase=Zbase

%                BranchResistancepu=obj.NIS.Branch(:,3)
%                 FromBus=obj.NIS.OriginalNameofSendingEndBus
%                 ToBus=obj.NIS.OriginalNameofReceivingEndBus
%                BranchResistanceohm=obj.BranchResistance


                clear NumberofBranches NumberOfBranchColumn Ibase Zbase     % Freeing up memory


                disp('Network initialization of the Branch matrix was done')
                obj.NISBranchAnalysisFlag=1;
                disp(['SimulationId:' obj.SimulationId])
                disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                if obj.CISAnalysisFlag==1
                    obj.SensitivityAnalysis;
                else
                    obj.StatusReadiness;
                end
           else
               obj.NISBranchData=obj.InboundMessage;
               obj.NISBranchFlag=1;
               disp('NIS.NetworkBusInfo was received earlier than NIS.NetworkBusInfo')
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 7         
                       
        function SensitivityAnalysis(obj)
            SourceNode=obj.NIS.Branch(:,1);
            TargetNode=obj.NIS.Branch(:,2);
            EdgeWeightsR=obj.BranchResistance;
            EdgeWeightsX=obj.BranchReactance;
            obj.GR=graph(SourceNode,TargetNode,EdgeWeightsR);
            obj.GX=graph(SourceNode,TargetNode,EdgeWeightsX);
            clear SourceNode TargetNode EdgeWeightsR EdgeWeightsX
            SensitivityMatrixR=zeros(obj.NumberofBuses,obj.NumberofBuses);
            SensitivityMatrixX=zeros(obj.NumberofBuses,obj.NumberofBuses);
            obj.DistancesR=distances(obj.GR);
            obj.DistancesX=distances(obj.GX);
%             h=plot(obj.GR);
%             NameWithscd=~cellfun('isempty',strfind(obj.NIS.OriginalBusNames,"scd"))
%             NameWithscd1=~cellfun('isempty',strfind(obj.NIS.OriginalBusNames,"pohja"))            
%              for aa=1:obj.NumberofBuses
%                  BusName=string(obj.NIS.OriginalBusNames(aa))
%                  if NameWithscd(aa,1)==1 || strcmp(BusName,"ovspt1") || NameWithscd1(aa,1)==1
%                      labelnode(h,aa,aa);
%                  end
%                  if strcmp(BusName,"scd_101990") || strcmp(BusName,"scd_101818")|| strcmp(BusName,"scd_101852")|| strcmp(BusName,"scd_101961")|| strcmp(BusName,"scd_101962")|| strcmp(BusName,"scd_101965")|| strcmp(BusName,"scd_101985")|| strcmp(BusName,"scd_101986")|| strcmp(BusName,"scd_101990")|| strcmp(BusName,"scd_101996")|| strcmp(BusName,"scd_103911")
%                      highlight(h,aa,'NodeColor','red')
% %                      labelnode(h,aa,aa);
%                  end
%                   if strcmp(BusName,"scd_101988") || strcmp(BusName,"scd_101995") || strcmp(BusName,"scd_102001")
%                       highlight(h,aa,'NodeColor','green')
% %                       labelnode(h,aa,aa);
%                   end
%              end
%             
            a=obj.NIS.Bus(1,1);
            ShortPathR=struct;
            for aa=1:1:obj.NumberofBuses
                b=obj.NIS.Bus(aa,1);
                ShortPathR(aa).BusNumbers=shortestpath(obj.GR,a,b);
            end
            % For Non-diagonal elements
            for aa=1:1:obj.NumberofBuses
                for j=1:1:obj.NumberofBuses
                    if j>aa
                        CommonResistance=0;
                        bb=ShortPathR(aa).BusNumbers;
                        cc=ShortPathR(j).BusNumbers;
%                         n=length(cc);
%                         Counter=0;
%                         for k=1:1:n
%                             common=find(cc(k)==bb,1);
%                             if ~isempty(common)
%                                 Counter=Counter+1;
%                                 CommonNodes(Counter,1)=cc(k);
%                             end
%                         end
                        CommonNodes=intersect(bb,cc);
                        if isempty(CommonNodes)                    %Counter==0
                            CommonResistance=0;
                        else
                            c=length(CommonNodes);
                            DistR=zeros(c,1);
                            DistX=zeros(c,1);
                            for w=1:1:c
                                DistR(w,1)=obj.DistancesR(a,CommonNodes(w));
                                DistX(w,1)=obj.DistancesX(a,CommonNodes(w));
                            end
                            CommonResistance=max(DistR);
                            CommonReactance=max(DistX);
                        end
                    SensitivityMatrixR(aa,j)=CommonResistance;
                    SensitivityMatrixX(aa,j)=CommonReactance*i;
                    clear CommonNodes
                    end
                end
            end
            TransR=transpose(SensitivityMatrixR);
            TransX=transpose(SensitivityMatrixX);
            
            % For diagonal elements
            for yy=1:1:obj.NumberofBuses
                b=obj.NIS.Bus(yy,1);
                r=obj.DistancesR(a,b);
                SensitivityMatrixR(yy,yy)=r;
                x=obj.DistancesX(a,b);
                SensitivityMatrixX(yy,yy)=x*i;
            end
            SensitivityMatrixR=SensitivityMatrixR+TransR;
            SensitivityMatrixX=SensitivityMatrixX+TransX;
            obj.SensitivityMatrixR=SensitivityMatrixR;
            obj.SensitivityMatrixX=SensitivityMatrixX;
            for www=1:1:obj.NumberofBuses
                Rth(www,1)=SensitivityMatrixR(www,www);
                Xth(www,1)=SensitivityMatrixX(www,www);
                Zth=abs(Rth(www,1)+Xth(www,1));
                ZthTotal(www,1)= Zth;
            end
            obj.SensitivityMatrixZ=ZthTotal;
            clear Rth Xth ZthTotal SensitivityMatrixR SensitivityMatrixX TransR TransX a b r x
            clear CommonNodes CommonResistance CommonReactance DistR DistX ShortPathR
            disp('sensitivity analysis was done')
            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            obj.State='Free';
            obj.StatusReadiness;
       end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 8
        
        function CISAnalysis(obj)
                obj.State='Busy';
                obj.CIS.ResourceId=obj.InboundMessage.ResourceId;
                obj.CIS.CustomerId=obj.InboundMessage.CustomerId;
                obj.CIS.BusName=obj.InboundMessage.BusName;

                disp('Initialization of the Customer Information system was done')
                disp(['SimulationId:' obj.SimulationId])
                disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                obj.CISAnalysisFlag=1;
                obj.State='Free';
            if obj.NISBranchAnalysisFlag==1 && obj.NISBusAnalysisFlag==1
                obj.SensitivityAnalysis;
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 9         
                        
        function FlexibilityNeed(obj)
           
           %%%%% Numbering the violations based on Time
           VolVioNum=length(obj.VoltageForecasts.Time);
           k=0;
           for i=1:1:VolVioNum   
               VolVioSameTime=find(string(obj.VoltageForecasts.Time(i))==string(obj.VoltageForecasts.Time(:)));
               FirstRow=VolVioSameTime(1,1);
               if i==1
                  FirstRowOld=0;
               end
               if FirstRowOld~=FirstRow
                   k=k+1;
                   obj.VoltageForecasts.CongestionNumber(i)=k;
               else
                   obj.VoltageForecasts.CongestionNumber(i)=k;
               end
               FirstRowOld=FirstRow;
           end
           
           %%%%% numbering of the violations based on Time + VioDirection
            
           First1=0;
           for i=1:1:VolVioNum   
               VolVioSameTime=find(string(obj.VoltageForecasts.Time(i))==string(obj.VoltageForecasts.Time(:)));
               First=VolVioSameTime(1,1);
               End=VolVioSameTime(end,1);
               if ~isequal(First,First1)
                   over=find(obj.VoltageForecasts.VioDirection=="over");
                   if ~isempty(over)
                       b=length(over);
                       for k=1:b
                          if over(k)>End || over(k)<First
                              over(k)=0;  % used for deleting the over voltages belong to other times
                          end
                       end
                       over(over==0)=[]; % delete the rows with 0 value
                   end
                   over1=zeros(length(VolVioSameTime),1);
                   
                   if ~isempty(over)
                       for n=1:length(VolVioSameTime)
                            a=find(VolVioSameTime(n,1)==over(:,:), 1);
                            if ~isempty(a)
                                over1(n,1)=VolVioSameTime(n,1);
                            end
                       end
                      over=over1;
                      if ~isequal(over,VolVioSameTime)
                        under=VolVioSameTime-over;
                        k=VolVioSameTime(1,1);
                        Number=obj.VoltageForecasts.CongestionNumber(k)+1;
                        a=find(under~=0);
                        rows=under(a,1);
                        for j=1:1:length(rows)
                            obj.VoltageForecasts.CongestionNumber(rows(j,1))=Number;
                        end
                        rows=find(obj.VoltageForecasts.CongestionNumber(:)>=Number);
                        for p=1:1:length(rows)
                           if  obj.VoltageForecasts.Time(rows(p))~=obj.VoltageForecasts.Time(First)
                             obj.VoltageForecasts.CongestionNumber(rows(p))=obj.VoltageForecasts.CongestionNumber(rows(p))+1;
                           end 
                        end                         
                      end  
                   end
               end
               First1=First;
           end
            
           %Temporary=obj.VoltageForecasts
            %%%%% numbering of the violations based on Time + VioDirection+ Congestion zone
            
            CNumber=max(obj.VoltageForecasts.CongestionNumber)
            Counter=0;
            i=1;
            while i<=CNumber
                if Counter>0
                    Counter=Counter-1;
                else
                   Counter=0;
                   Rows=find(obj.VoltageForecasts.CongestionNumber==i);
                   for k=1:length(Rows)
                       Congestion(k,:)=obj.VoltageForecasts(Rows(k),:);
                   end
                   Congestion=sortrows(Congestion);
                   CongestionLength=length(Congestion.CongestionNumber);
                   Change="False";

                   BusNumber=Congestion.BusNumber(1);    % we take the bus with the highest violation
                   BasicCongestionNum=Congestion.CongestionNumber(1);
                   RS=zeros(obj.NumberofBuses,1);
                   for k=1:1:obj.NumberofBuses   % relative sensitivity calculation needed for determining the size of network suitable for flexibility need
                       RS(k,1)=obj.SensitivityMatrixR(k,BusNumber)/obj.SensitivityMatrixR(BusNumber,BusNumber);
                   end

                   for k=1:1:obj.NumberofBuses  % Determining buses that has impact on congestion area
                       if RS(k,1)<obj.RS
                           RS(k,1)=0; % outside the congestion zone
                       else
                           RS(k,1)=1; % inside the congestion zone
                       end
                   end

                   InsideZoneIndexes=find(RS>0);
                   for kk=1:1:CongestionLength
                      Row=find(InsideZoneIndexes==Congestion.BusNumber(kk));
                      if isempty(Row)
                          Congestion.CongestionNumber(kk)=Congestion.CongestionNumber(kk)+1;
                          Change="True"; 
                      end
                   end
                   %%% Second round
                   if strcmp(Change,"True")
                      while strcmp(Change,"True")
                        Change="False";
                        Counter=Counter+1;
                        BasicCongestionNum=BasicCongestionNum+1;
                        Row=find(Congestion.CongestionNumber==BasicCongestionNum);
                        BusNumber=Congestion.BusNumber(Row(1));
                        RS=zeros(obj.NumberofBuses,1);
                        for k=1:1:obj.NumberofBuses   % relative sensitivity calculation needed for determining the size of network suitable for flexibility need
                            RS(k,1)=obj.SensitivityMatrixR(k,BusNumber)/obj.SensitivityMatrixR(BusNumber,BusNumber);
                        end
                        for k=1:1:obj.NumberofBuses  % Determining buses that has impact on congestion area
                           if RS(k,1)<obj.RS
                               RS(k,1)=0; % outside the congestion zone
                           else
                               RS(k,1)=1; % inside the congestion zone
                           end
                        end
                        InsideZoneIndexes=find(RS>0);
                        for kk=1:1:length(Row)
                          ss=find(InsideZoneIndexes==Congestion.BusNumber(Row(kk)), 1);
                          if isempty(ss)
                              Congestion.CongestionNumber(Row(kk))=Congestion.CongestionNumber(Row(kk))+1;
                              Change="True"; 
                          end
                        end
                      end
                   end
                   CNumber=CNumber+Counter; 
                   for k=1:length(Rows)
                     obj.VoltageForecasts(Rows(k),:)=Congestion(k,:);
                   end
                   %Temporary=obj.VoltageForecasts;
                   %lengthofcongesiton=length(obj.VoltageForecasts.CongestionNumber);
                   %Rows=Rows
                   for w=1:1:length(obj.VoltageForecasts.CongestionNumber)
                       exist=find(w==Rows, 1);
                       if isempty(exist)
                           if w>max(Rows)
                               obj.VoltageForecasts.CongestionNumber(w)=obj.VoltageForecasts.CongestionNumber(w)+Counter;
                           end
                       end
                   end
                end
                i=i+1;
                clear Congestion Rows Temporary
            end 
            
           disp("Numbering was completed")
           %Temporary=obj.VoltageForecasts
           CNumber=max(obj.VoltageForecasts.CongestionNumber) 
           for i=1:1:CNumber   % processing each congestion number, one by one
                Rows=find(obj.VoltageForecasts.CongestionNumber==i);
               for k=1:length(Rows)
                   Congestion(k,:)=obj.VoltageForecasts(Rows(k),:);
               end
               Congestion=sortrows(Congestion);
               % Finding BusName and its number (heart of the congestion)
               
               if (Congestion.VioDirection(1)=="over")  % since the table is already sorted by time and violation values, for over voltage situations, the last row has the highest violation magnitude
                   VoltageViolation=Congestion.Violation(end);
                   BusName=Congestion.BusName(end);
                   BusNumber=Congestion.BusNumber(end);
               else
                   VoltageViolation=Congestion.Violation(1); % since the table is already sorted by time and violation values, for over voltage situations, the first row has the lowest violation magnitude
                   BusName=Congestion.BusName(1);
                   BusNumber=Congestion.BusNumber(1);
               end
               
               
               % Finding RealPowerMin and RealPowerRequest
               
               Row = find(strcmp(string(obj.NIS.OriginalBusNames(:,1)),BusName)); % finding the Row of the Bus
               NominalVoltage=(obj.NIS.Bus(Row,10))/sqrt(3);  % kV
%                VoltageViolation=1000*VoltageViolation*NominalVoltage; % Voltage violation per volt
               
               R=obj.SensitivityMatrixR(BusNumber,:); % Relative sensitivity value corresponding to the BusNumber
               X=obj.SensitivityMatrixX(BusNumber,:);
               Z=obj.SensitivityMatrixZ;
%                Z(254,1)=0.1463
               Z=Z.';
%                for h=1:1:length(R)
%                    Z(1,h)=abs(R(1,h)+X(1,h)*i)
%                end

               DeltaV=zeros(1,length(R));
%               DeltaV(1,:)=VoltageViolation;  % per volt
               DeltaV(1,:)=VoltageViolation;  % per unit
               DeltaI=zeros(1,length(R));

               %DeltaI(1,:)=DeltaV(1,:)./Z(1,:) % per unit
               DeltaI(1,:)=DeltaV(1,:)./R(1,:); % per unit
               DeltaI(1,1)=0.0000002;   % Using a small value (0.002) to avoid inf because the first value of DeltaI is always inf (root bus)
               
%                PowerNeed=zeros(1,length(DeltaV));
%                VoltageBase(:,1)=obj.NIS.Bus(:,10); % kV
%                PowerNeed(:,:)=1000*sqrt(3).*(VoltageBase'.*DeltaI(1,:)); % Power need per W (Although the flex need should be calculated in kW, but here for more accuracy W is used)
               
               Ibase=obj.Ibase;
                
%                Voltage=zeros(length(DeltaV),1);
%                Voltage(:,:)=1;
               PowerNeed=zeros(1,obj.NumberofBuses);
               PowerNeed(:,:)=(obj.NIS.Sbase.Value)*1000*sqrt(3).*(DeltaI(1,:)); % Power Need per Watt
               %
               Rth=obj.SensitivityMatrixR(BusNumber,BusNumber);
               Xth=obj.SensitivityMatrixX(BusNumber,BusNumber);
               Iscpu=1/abs(Rth+Xth);
               MinDeltaI=DeltaI(1,BusNumber);
               MinIbase=Ibase(BusNumber);
               
               MinPowerNeed=PowerNeed(1,BusNumber);
               PowerNeed(1,1)=0;

               RS=zeros(obj.NumberofBuses,1);
               for k=1:1:obj.NumberofBuses   % relative sensitivity calculation needed for determining the size of network suitable for flexibility need
                   RS(k,1)=obj.SensitivityMatrixR(k,BusNumber)/obj.SensitivityMatrixR(BusNumber,BusNumber);
               end
               for k=1:1:obj.NumberofBuses  % Determining buses that has impact on congestion area
                   if (RS(k,1)<obj.RS)
                       RS(k,1)=0;
                   else
                       RS(k,1)=1;
                   end
               end
               PowerNeed=abs(RS'.*PowerNeed);    % absolute is needed to avoid having negative values
               Column=find(PowerNeed(1,:)~=0);
               PowerNeed(PowerNeed==0)=[];
               [RealPowerMin,RealPowerMinIndex]=min(PowerNeed);  % related to risk policy of DSO
               %RealPowerMinBusName=obj.NIS.OriginalBusNames(RealPowerMinIndex)
               RealPowerMin=round(RealPowerMin);        % Applying over purchase, under purchase or nutural bidding strategy
               RealPowerMin=roundn(RealPowerMin,1); %round to the nearest 10
               
               [RealPowerRequest,RealPowerRequestIndex]=max(PowerNeed); % related to risk policy of DSO
               %RealPowerRequestBusName=obj.NIS.OriginalBusNames(RealPowerRequestIndex)
               RealPowerRequest=round(RealPowerRequest);         % Applying over purchase, under purchase or nutural bidding strategy
               RealPowerRequest=roundn(RealPowerRequest,1); %round to the nearest 10
               if RealPowerRequest==inf
                   RealPowerRequest=RealPowerMin;
               end
               if RealPowerMin==0
                   RealPowerMin=10;
               end
               if RealPowerRequest==0
                   RealPowerRequest=10;
               end
               
               Counter=0;
               
               %%%%% 2- CustomerIds
               ss=obj.CIS.BusName;
               for k=1:1:length(Column)
                    BusNames(k,1)=obj.NIS.OriginalBusNames(Column(1,k),1);
                    Rows=find(strcmp(ss,string(BusNames(k,1))));
                    if ~isempty(Rows)
                        for j=1:1:length(Rows)
                            Counter=Counter+1;
                            CustomerIds(Counter,1)=obj.CIS.CustomerId(Rows(j),1);
                        end
                    end
               end
               clear ss
               CustomerIds=string(CustomerIds);
               %%%%% Storing the flex need
               
                Rows=find(obj.VoltageForecasts.CongestionNumber==i);
                obj.FlexNeedDMS(i).ActivationTime=string(obj.VoltageForecasts.Time(Rows(1)));
                obj.FlexNeedDMS(i).Duration.Value=60; % assuming that flex duration is always 60 Mins
                obj.FlexNeedDMS(i).Duration.UnitOfMeasure="Minute";
                if obj.VoltageForecasts.VioDirection(Rows(1))=="over"
                    obj.FlexNeedDMS(i).Direction="downregulation";
                else
                    obj.FlexNeedDMS(i).Direction="upregulation";
                end
                obj.FlexNeedDMS(i).RealPowerMin.Value=RealPowerMin/1000; % Divided by 1000 to make it kW
%                 obj.FlexNeedDMS(i).RealPowerMin.Value=1; % just for testing with Olli

                obj.FlexNeedDMS(i).RealPowerMin.UnitOfMeasure="kW";
                
                obj.FlexNeedDMS(i).RealPowerRequest.Value=RealPowerRequest/1000; % Divided by 1000 to make it kW
%                 obj.FlexNeedDMS(i).RealPowerRequest.Value=1; % just for testing with Olli
               
                obj.FlexNeedDMS(i).RealPowerRequest.UnitOfMeasure="kW";
                
                
                if Counter>0
                    obj.FlexNeedDMS(i).CustomerIds=CustomerIds;
                else
                    obj.FlexNeedDMS(i).CustomerIds="None";   % It means there is no CustomerId inside the congestion Zone
                end
                obj.FlexNeedDMS(i).MainBus=BusName;
                obj.FlexNeedDMS(i).VoltageViolation=VoltageViolation;
                pause(0.01);   % to make sure that time is unique because it is used for congestion Id
                    t = datetime('now', 'TimeZone', 'UTC');
                    t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    s = strcat(obj.SourceProcessId,'-',t);
%                 s=num2str(i)
                obj.FlexNeedDMS(i).CongestionId=s;
%                 obj.FlexNeedDMS(i).BidResolution.Value=5;
                obj.FlexNeedDMS(i).BidResolution.Value=3;
                obj.FlexNeedDMS(i).BidResolution.UnitOfMeasure="kW"; 
                obj.FlexNeedDMS(i).OfferId="None";
                
                clear Congestion CustomerIds BusNames
           end
           
           
            %%%%% Deleting the CustomerIds that are common between flexibility needs with a same activation time but opposite direction using relative sensitivity calculation
            
            NumOfNeeds=length(obj.FlexNeedDMS);
            B="0";
            for i=1:1:NumOfNeeds
               if ~strcmp(B,obj.FlexNeedDMS(i).ActivationTime)
                    A=obj.FlexNeedDMS(i).ActivationTime;
                    B=A;
                    Flag=0;
                    SameTime=[];
                    for m=1:NumOfNeeds
                        if strcmp(A,obj.FlexNeedDMS(m).ActivationTime)
                            if ~strcmp(obj.FlexNeedDMS(i).Direction,obj.FlexNeedDMS(m).Direction)
                                SameTime(m)=m;
                                Flag=1;
                            end
                        end
                    end
                    if Flag==1
                        SameTime(SameTime==0)=[];
                        if length(SameTime)==0
                            SameTime=[];           % it means there is no same activation time
                        end
                    end
                    if ~isempty(SameTime)
                        rows=length(SameTime)
                        for k=1:1:length(rows)
                            Flag=0;
                            First=obj.FlexNeedDMS(i).CustomerIds;
                            FirstBusName=obj.FlexNeedDMS(i).MainBus;
                            FirstBusNumber=find(obj.NIS.OriginalBusNames==FirstBusName);

                            Second=obj.FlexNeedDMS(rows(k)).CustomerIds;
                            SecondBusName=obj.FlexNeedDMS(rows(k)).MainBus;
                            SecondBusNumber=find(strcmp(obj.NIS.OriginalBusNames,SecondBusName));
                            
                            if SecondBusNumber==1
                                Second(:)=cellstr('0');
                                Flag=1;
                            elseif SecondBusNumber==1
                                First(:)=cellstr('0');
                                Flag=1;
                            else
                                FirstRS=zeros(obj.NumberofBuses,1);
                                for f=1:1:obj.NumberofBuses   % relative sensitivity calculation
                                    FirstRS(f,1)=obj.SensitivityMatrix(f,FirstBusNumber)/obj.SensitivityMatrix(FirstBusNumber,FirstBusNumber);
                                end 
                                SecondRS=zeros(obj.NumberofBuses,1);
                                for f=1:1:obj.NumberofBuses   % relative sensitivity calculation
                                    SecondRS(f,1)=obj.SensitivityMatrix(f,SecondBusNumber)/obj.SensitivityMatrix(SecondBusNumber,SecondBusNumber);
                                end
                                for r=1:1:length(First)
                                   ID=string(First(r,1));
                                   IDs=string(Second);
                                   row=find(strcmp(IDs,ID));
                                   if ~isempty(row)
                                       CustomerIdRow=find(strcmp(ID,obj.CIS.CustomerId));
                                       CustomerIdBus=obj.CIS.BusName(CustomerIdRow);
                                       BusNumber=find(strcmp(obj.NIS.OriginalBusNames,CustomerIdBus));
                                       FirstRSBusNumber=FirstRS(BusNumber,1);
                                       SecondRSBusNumber=SecondRS(BusNumber,1);
                                       if FirstRSBusNumber<=SecondRSBusNumber
                                           First(r)=cellstr('0');
                                           Flag=1;
                                       else
                                           Second(r)=cellstr('0');
                                           Flag=1;
                                       end
                                   end
                                end
                            end
                            if Flag==1
                                First=string(First);
                                Second=string(Second);
                                
                                FirstRow=find(strcmp(First,"0"));
                                while ~isempty(FirstRow)
                                    First(FirstRow(1,1))=[];
                                    FirstRow=find(strcmp(First,"0"));
                                end
                                
                                SecondRow=find(strcmp(Second,"0"));
                                while ~isempty(SecondRow)
                                    First(SecondRow(1))=[];
                                    SecondRow=find(strcmp(Second,"0"));
                                end
   
                                obj.FlexNeedDMS(i).CustomerIds=First;
                                obj.FlexNeedDMS(rows(k)).CustomerIds=Second;
                            end
                        end
                    end
                end 
            end
            obj.FlexNeedMarket=[];
            obj.FlexNeedMarket=obj.FlexNeedDMS;
            for i=1:1:length(obj.FlexNeedMarket)% there is a difference between flex needs in DMS and what is asked from Market
                obj.FlexNeedMarket(i).RealPowerMin.Value=3; % It allows participation of small scale Flex.
                obj.FlexNeedMarket(i).RealPowerRequest.Value=(obj.FNM)*(obj.FlexNeedDMS(i).RealPowerRequest.Value);
                obj.FlexNeedMarket(i).OfferCount=0;
                obj.FlexNeedMarket(i).NumOfReceivedOffers=0;
                obj.FlexNeedMarket(i).Status="Not received offers yet";
                if obj.FlexNeedMarket(i).RealPowerRequest.Value<3
                    obj.FlexNeedMarket(i).RealPowerRequest.Value=3;
                end
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% just
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% testing
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% with
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OLLI
%             for i=1:1:length(obj.FlexNeedMarket)% there is a difference between flex needs in DMS and what is asked from Market
%                 obj.FlexNeedMarket(i).RealPowerMin.Value=1; % It allows participation of small scale Flex.
%                 obj.FlexNeedMarket(i).RealPowerRequest.Value=1;
%                 obj.FlexNeedMarket(i).OfferCount=0;
%                 obj.FlexNeedMarket(i).NumOfReceivedOffers=0;
%                 obj.FlexNeedMarket(i).Status="Not received offers yet";
%                 obj.FlexNeedMarket(i).OfferIds="None";
% %                 if obj.FlexNeedMarket(i).RealPowerRequest.Value<5
% %                     obj.FlexNeedMarket(i).RealPowerRequest.Value=5;
% %                 end
%             end
            
            try
                obj.FlexNeedMarket=struct2table(obj.FlexNeedMarket);   % when structure is only 1*1, the struct2table throws an error. follow here: https://se.mathworks.com/matlabcentral/answers/277584-possible-bug-in-struct2table
            catch
               largeStruct = repmat(obj.FlexNeedMarket,2,1);  % in order to avoid an error for 1*1 structures, then we add another row and after making a table remove the second row
               table = struct2table(largeStruct);
               obj.FlexNeedMarket = table(1,:);
               clear table
            end
            
            for i=1:length(obj.FlexNeedDMS)   
                if ~strcmp(obj.FlexNeedDMS(i).CustomerIds,"None")
                   obj.CustomerIdExistanceFlag=1;   % there are CustomerIds within the congestion area
                else
                   obj.CustomerIdExistanceFlag=2;   % there isnot any CustomerId within the congestion area
                end
            end
            
            %FlexNeedsssss=struct2table(obj.FlexNeedDMS)
            %SavedFlexNeed=jsonencode(obj.FlexNeedDMS);
            a=jsonencode(obj.FlexNeedMarket) % just to show on the screen
            
            if obj.CustomerIdExistanceFlag==1
                disp('flex need calculation was done and ready to be forwarded')
                FlexibilityNeedForwarding(obj);   %  forwarding the flex needs to LFM
            else
                disp('flex need calculation was done but there is no customerId within the congestion zone')
                obj.StatusReadiness;    
            end
       end
       
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 10          
       
        function FlexibilityNeedForwarding(obj)
            for i=1:length(obj.FlexNeedDMS)
                CustomerIdNonExistance=find(strcmp(obj.FlexNeedDMS(i).CustomerIds,"None"),1);  % To avoid sending flexibility need when there is no CustomerId inside congestion area
                if isempty(CustomerIdNonExistance) 
                    obj.AbstractResult.Type='FlexibilityNeed';
                    obj.AbstractResult.SimulationId=obj.SimulationId{1};
                    obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                    obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('PGO',num2str(obj.MessageCounterOutbound));
                    obj.AbstractResult.MessageId=s;
                    obj.AbstractResult.EpochNumber=obj.Epoch;
                    obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    obj.AbstractResult.Timestamp=t; % abstract result end

                    obj.AbstractResult.ActivationTime=obj.FlexNeedMarket(i,:).ActivationTime;
                    obj.AbstractResult.Duration=obj.FlexNeedMarket(i,:).Duration;
                    obj.AbstractResult.Direction=obj.FlexNeedMarket(i,:).Direction;
                    obj.AbstractResult.RealPowerMin=obj.FlexNeedMarket(i,:).RealPowerMin;
                    obj.AbstractResult.RealPowerRequest=obj.FlexNeedMarket(i,:).RealPowerRequest;
                        a=numel(obj.FlexNeedDMS(i).CustomerIds);
                    if a==1
                        obj.AbstractResult.CustomerIds={obj.FlexNeedDMS(i).CustomerIds};
                    else
                        obj.AbstractResult.CustomerIds=obj.FlexNeedDMS(i).CustomerIds;
                    end
                    obj.AbstractResult.CongestionId=string(obj.FlexNeedMarket(i,:).CongestionId);
                    obj.AbstractResult.BidResolution=obj.FlexNeedMarket(i,:).BidResolution;

                    MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                    MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                        a=strcat('FlexibilityNeed.',obj.MarketId);
                    obj.AmqpConnector.sendMessage(a, MyBytesOut);
                    clear a MyBytesOut MyStringOut t s CustomerIdNonExistance
                    obj.AbstractResult=[];
                end
            end
            obj.FlexNeedSentFlag=1;
            disp('Flex needs were sent')
            obj.StatusReadiness;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 11
        
        function LFMOffers(obj)
            obj.State='Busy';
            ReceivedOffer=struct;
            
            NextDayStart=dateshift(obj.Today,'start','day','next');
            
            if obj.InboundMessage.OfferCount>0
                OfferDay=char(obj.InboundMessage.ActivationTime);
                OfferDay=OfferDay(1:10);
                OfferDay=datetime(OfferDay,'InputFormat','yyyy-MM-dd');
            else
                OfferDay = NextDayStart;
            end
            
            if NextDayStart==OfferDay && obj.LFMOperationFlag==1
                if obj.OfferCounter==0
                    existance=[]; % existance is set empty
                else
                    existance=find(strcmp(obj.Offer.OfferId,obj.InboundMessage.OfferId));  % To assure that this is a new offer
                end
                if isempty(existance) % Only new Offers are stored
                    obj.TotalOfferCounter=obj.TotalOfferCounter+1;
                    Row=find(strcmp(obj.FlexNeedMarket.CongestionId,string(obj.InboundMessage.CongestionId)));
                    if ~isempty(Row)
                        if obj.InboundMessage.OfferCount>0 % When OfferCount is 0, it means there is no offer for that congestion
                            disp('Non-empty offer is coming')
                            obj.OfferCounter=obj.OfferCounter+1;
                            i=obj.OfferCounter;
                            ReceivedOffer.CongestionId=string(obj.InboundMessage.CongestionId); %
                            ReceivedOffer.Price=obj.InboundMessage.Price; %
                            ReceivedOffer.OfferId=string(obj.InboundMessage.OfferId); %
                            ReceivedOffer.ActivationTime=obj.InboundMessage.ActivationTime; %
                            ReceivedOffer.Duration=obj.InboundMessage.Duration; %
                            ReceivedOffer.Direction=string(obj.InboundMessage.Direction); %
                            ReceivedOffer.OfferCount=obj.InboundMessage.OfferCount; %
                            ReceivedOffer.RealPower=obj.InboundMessage.RealPower;
%                             num = numel(obj.InboundMessage.CustomerIds);
%                             if num > 1
%                                 for w=1:num
%                                     ReceivedOffer.CustomerIds(w)=string(obj.InboundMessage.CustomerIds(w))
%                                 end
%                             else
                            ReceivedOffer.CustomerIds=obj.InboundMessage.CustomerIds;
% %                             end
                            ReceivedOffer.OfferCount=obj.InboundMessage.OfferCount;
                            ReceivedOffer.PricePerkW=0;


%                             try
                            obj.Offer(i,:)=struct2table(ReceivedOffer);
%                             catch
%                                 aa = repmat(ReceivedOffer,2,1);
%                                 class(aa)
%                                 bb = struct2table(aa)
%                                 class(bb)
%                                 obj.Offer(i,:) = bb(1,:)
%                             end

%                             Row=find(strcmp(obj.FlexNeedMarket.CongestionId,string(obj.Offer(i,:).CongestionId)))
                            obj.FlexNeedMarket(Row,:).OfferCount=obj.Offer(i,:).OfferCount;
                            obj.FlexNeedMarket(Row,:).NumOfReceivedOffers=obj.FlexNeedMarket(Row,:).NumOfReceivedOffers+1;
                            if obj.FlexNeedMarket(Row,:).OfferCount==obj.FlexNeedMarket(Row,:).NumOfReceivedOffers
                                obj.FlexNeedMarket(Row,:).Status="All offers have been received";                            
                            end
                        else
                            disp('Empty offer is coming')
%                             Row=find(strcmp(obj.FlexNeedMarket.CongestionId,string(obj.InboundMessage.CongestionId)));
%                             if ~isempty(Row)
                            obj.FlexNeedMarket(Row,:).OfferCount=0;
                            obj.FlexNeedMarket(Row,:).NumOfReceivedOffers=obj.FlexNeedMarket(Row,:).NumOfReceivedOffers+1;
                            obj.FlexNeedMarket(Row,:).Status="All offers have been received";
%                             end
                        end
                    end
                end

                Rows=find(strcmp(obj.FlexNeedMarket.Status,"All offers have been received"));
                if length(Rows)==height(obj.FlexNeedMarket)
                    obj.OfferReceivedFlag=1;
                    if obj.OfferCounter==0
                        disp('All received offers are empty!');
                        obj.EmptyOffersFlag=1;
                    end
                    if obj.x==(obj.MarketOpeningTime)          
                        obj.OfferSelectionTimeFlag=1;
                        if obj.EmptyOffersFlag==0
                            obj.OfferSelection;   % Decision making
                        else
                            obj.StatusReadiness;
                        end
                    else
                        obj.OfferSelectionTimeFlag=2;
                        obj.StatusReadiness;
                    end
                end
                clear Rows
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 12
        
        function OfferSelection(obj)
            for i=1:1:height(obj.FlexNeedMarket)
                if obj.FlexNeedMarket(i,:).OfferCount>0  % empty offers are not analysed
                   Rows=find(strcmp(obj.Offer.CongestionId,obj.FlexNeedMarket(i,:).CongestionId));
                   if ~isempty(Rows)
                       NumOfOffers=length(Rows);
                       TempOffer=table;
                       if NumOfOffers>1
                           for k=1:1:NumOfOffers
                               obj.Offer(Rows(k),:).PricePerkW=obj.Offer(Rows(k),:).Price.Value/obj.Offer(Rows(k),:).RealPower.Series.Regulation.Values;
                               TempOffer(k,:)=obj.Offer(Rows(k),:);
                           end
                           TempOffer=sortrows(TempOffer,10);  % the table is sorted only based on the values og column 10 (flex price per kW)
                           OfferedRealPower=0;
                           for m=1:1:NumOfOffers
                                OfferedRealPower=TempOffer(m,:).RealPower.Series.Regulation.Values+OfferedRealPower;
                                if OfferedRealPower>=obj.FlexNeedDMS(i).RealPowerRequest.Value
                                    OfferId(m,1)=TempOffer(m,:).OfferId;
                                    obj.FlexNeedDMS(i).OfferId=OfferId; % selection of the cheapest offer
                                    obj.OfferSelectedFlag=1;
                                    break;
                                else
                                    OfferId(m,1)=TempOffer(m,:).OfferId;
                                    obj.FlexNeedDMS(i).OfferId=OfferId;
                                %   OfferedRealPower=Offer(m).RealPower.Series.Regulation.Values+OfferedRealPower;
                                    obj.OfferSelectedFlag=1;
                                end
                           end
                       else % in this case, there is only one offer that will be taken. something is better than nothing!
                           obj.FlexNeedDMS(i).OfferId=obj.Offer(Rows(1),:).OfferId;
                           obj.OfferSelectedFlag=1;
                       end
                   end
                end
                clear OfferId
            end
            
            
            if obj.OfferSelectedFlag==1
                obj.OfferSelectionForwading;
            else
                obj.OfferSelectedFlag=2;
                obj.StatusReadiness;
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 13
        
        function OfferSelectionForwading(obj)
            for i=1:1:length(obj.FlexNeedDMS)
               if ~strcmp(obj.FlexNeedDMS(i).OfferId,"None")
                    obj.AbstractResult.Type='SelectedOffer';
                    obj.AbstractResult.SimulationId=obj.SimulationId{1};
                    obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                    obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('PGO',num2str(obj.MessageCounterOutbound));
                    obj.AbstractResult.MessageId=s;
                    obj.AbstractResult.EpochNumber=obj.Epoch;
                    obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    obj.AbstractResult.Timestamp=t; % abstract result end
                        a=numel(obj.FlexNeedDMS(i).OfferId);
                    if a==1
                        obj.AbstractResult.OfferIds={obj.FlexNeedDMS(i).OfferId};
                    else
                        obj.AbstractResult.OfferIds=obj.FlexNeedDMS(i).OfferId; % array of OfferIds
                    end
                                        
                    %obj.FlexNeedDMS(i).OfferId
                    obj.FlexNeedDMS(i).ActivationTime
                    
                    MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                    MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                        a=strcat('SelectedOffer.',obj.MarketId);                        
                    obj.AmqpConnector.sendMessage(a, MyBytesOut);
                    obj.SlectedOfferForwardedFlag=1;
                    clear a MyBytesOut MyStringOut t s
                    obj.AbstractResult=[];
                end
            end
            obj.StatusReadiness;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 14

        function StatusReadinessGrid(obj)
           if (obj.InboundMessage.EpochNumber==obj.Epoch)
                ErrorFlag=0;
                WarningFlag=0;

                %%%%%

                if strcmp(obj.InboundMessage.Value,'ready')
                    obj.StatePredictorReadinessFlag=1;
                    disp('Grid Forecaster is ready')
                end
                if strcmp(obj.InboundMessage.Value,'error')
                    obj.StatePredictorReadinessFlag=0;
                    obj.AbstractResult.Value='error';
                    ErrorFlag=1;
                    obj.AbstractResult.Description='Grid reported Error';
                    disp('PGO reported "error" message to Simulation Manager because an error occured on Grid')
                    disp(['SimulationId:' obj.SimulationId])
                end
                
%                 % Warning
%                 
%                 if obj.StatePredictorReadinessFlag==1
%                     if ((obj.NumberofBuses*3)~=obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentForecasts==obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='warning';
%                             WarningFlag=1;
%                             obj.AbstractResult.Description='Forecasted Voltage values werenot received completely';
%                             disp('PGO reported "warning" message to Simulation Manager because it seems that communication is unstable due to arrival of ready message when all voltage values are not received yet')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end
%                 if obj.StatePredictorReadinessFlag==1
%                     if ((obj.NumberofBuses*3)==obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentForecasts~=obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='warning';
%                             WarningFlag=1;
%                             obj.AbstractResult.Description='Forecasted current values werenot received completely';
%                             disp('PGO reported "warning" message to Simulation Manager because it seems that communication is unstable due to arrival of ready message when all current values are not received yet')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end
%                 if obj.StatePredictorReadinessFlag==1
%                     if ((obj.NumberofBuses*3)~=obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentForecasts~=obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='warning';
%                             WarningFlag=1;
%                             obj.AbstractResult.Description='Neither forecasted votage nor current values were received completely';
%                             disp('PGO reported "warning" message to Simulation Manager because it seems that communication is unstable due to arrival of ready message when all voltage and current values are not received yet')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end
                %%%%%

                if ErrorFlag==1
                    obj.AbstractResult.Type='Status';
                    obj.AbstractResult.SimulationId=obj.SimulationId{1};
                    obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                    obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('PredictedGridOptimization',num2str(obj.MessageCounterOutbound));
                    obj.AbstractResult.MessageId=s;
                    obj.AbstractResult.EpochNumber=obj.Epoch;
                    obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    obj.AbstractResult.Timestamp=t;
                    MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                    MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                    obj.AmqpConnector.sendMessage('Status.Error', MyBytesOut);
                    obj.State='Stopped';
                    clear MyStringOut MyBytesOut t s
                    obj.AbstractResult=[];
                    obj.State='Stopped';
                else
                    obj.StatusReadiness;
                end
                clear ErrorFlag WarningFlag
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 15
        
        function StatusReadiness(obj) 
           ReadyFlag=0;
           %%%
           if obj.StatePredictorReadinessFlag==1 % Grid is ready
               
               if obj.LFMOperationFlag==0
                   ReadyFlag=1;
                   disp(['LFM is not open yet. It only works between market opening time and market closing time.'])
               end

               if obj.FlexNeedFlag==2 
                   ReadyFlag=1;
                   disp('There is no need for flex.')
               end
          
           %%%
                if obj.CustomerIdExistanceFlag==2 % there is no CustomerId within the congestion area
                    ReadyFlag=1;
                    disp('There is no customerId inside the congesiton zones.')
                end
           %%%
           
%                 if obj.FlexNeedSentFlag==1 
%                     ReadyFlag=1; 
%                     disp('Needs have been sent')
%                 end
           %%%
           
                 if obj.OfferReceivedFlag==1 && obj.OfferSelectionTimeFlag==2
                    ReadyFlag=1;
                    disp('offers have been received but time for offer selection has not yet occured.')
                 end
           %%%
           
                if obj.OfferSelectionTimeFlag==1 && obj.EmptyOffersFlag==1
                    ReadyFlag=1;
                    disp('Although time for offer selection has occured, since all received offers are empty, selection doesnot happen.')
                end   
           %%%
           
                if obj.OfferSelectedFlag==2
                    ReadyFlag=1;
                    disp('Although time for offer selection has occured, no offer were selected in the decision making (OfferSelection).')
                end
                      
                if obj.OfferSelectedFlag==1 && obj.SlectedOfferForwardedFlag==1
                    ReadyFlag=1;
                    disp('Offer was selected and forwarded to LFM.')
                end
           end
           
           %%%

           if ReadyFlag==1
               if obj.ReadyMessageFlag==0
                   obj.ReadyMessageFlag=1;
                   obj.AbstractResult.Value='ready';
                   obj.AbstractResult.Type='Status';
                   obj.AbstractResult.SimulationId=obj.SimulationId{1};
                   obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                   obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('PredictedGridOptimization',num2str(obj.MessageCounterOutbound));
                   obj.AbstractResult.MessageId=s;
                   obj.AbstractResult.EpochNumber=obj.Epoch;
                   obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                   obj.AbstractResult.Timestamp=t;
                   MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                   MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                   obj.AmqpConnector.sendMessage('Status.Ready', MyBytesOut);
                       ss = char(strcat('PgoReady.',string(obj.SourceProcessId))); % just for testing
                   obj.AmqpConnector.sendMessage(ss, MyBytesOut);
                   clear MyBytesOut MyStringOut t s ReadyFlag ss
                   obj.AbstractResult=[];
                   disp('PGO sends a ready message')
               end
           end
        end
    end % End of methods
end % End of class
