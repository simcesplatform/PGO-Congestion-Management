function ManagementCallback(hObject, eventData)
   global NumOfSimRun
   global Handles
   global States
   global SimulationId
   
   mystr = java.lang.String(eventData.message, 'UTF-8');
   str = char(mystr);  %    Making the input into a character array
   InboundMessage = jsondecode(str); % decoding JSON data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if strcmp(InboundMessage.Type,'Start')
        if NumOfSimRun==0
            NumOfSimRun=NumOfSimRun+1;      
            PredictiveGridOptimizationBlock=InboundMessage.ProcessParameters.PredictiveGridOptimization;
            SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
            SimulationId(NumOfSimRun)=cellstr(InboundMessage.SimulationId);

            fields = fieldnames(PredictiveGridOptimizationBlock);
            PGOName = fields{1,1};

            Grid=PredictiveGridOptimizationBlock.(PGOName).MonitoredGridName;
            RS=PredictiveGridOptimizationBlock.(PGOName).RelativeSensitivity;
            FNM=PredictiveGridOptimizationBlock.(PGOName).FlexibilityNeedMargin;
            MaxVoltage=PredictiveGridOptimizationBlock.(PGOName).MaxVoltage;
            MinVoltage=PredictiveGridOptimizationBlock.(PGOName).MinVoltage;
            UpperAmberBandVoltage=PredictiveGridOptimizationBlock.(PGOName).UpperAmberBandVoltage;
            LowerAmberBandVoltage=PredictiveGridOptimizationBlock.(PGOName).LowerAmberBandVoltage;
            OverloadingBaseline=PredictiveGridOptimizationBlock.(PGOName).OverloadingBaseline;
            AmberLoadingBaseline=PredictiveGridOptimizationBlock.(PGOName).AmberLoadingBaseline;

            Object(NumOfSimRun)=PredictiveGridOptimization(SimulationSpecificExchange,SimulationId(NumOfSimRun),PGOName,Grid,RS,FNM,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
%             Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main;
%             States{NumOfSimRun}=parfeval(@() Object.Main,1);
            Object(NumOfSimRun).Main
            
        else
            sum=0;
            for i=1:NumOfSimRun % to assure that start message is for starting up a new simulation run not resending the start message to awake a component
                tf=strcmp(char(SimulationId(i)),InboundMessage.SimulationId);
                sum=sum+tf;
            end
                if sum==0
                    NumOfSimRun=NumOfSimRun+1;
                    PredictiveGridOptimizationBlock=InboundMessage.ProcessParameters.PredictiveGridOptimization;
                    SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
                    SimulationId(NumOfSimRun)=cellstr(InboundMessage.SimulationId);

                    fields = fieldnames(PredictiveGridOptimizationBlock);
                    PGOName = fields{1,1};

                    Grid=PredictiveGridOptimizationBlock.(PGOName).MonitoredGridName;
                    RS=PredictiveGridOptimizationBlock.(PGOName).RelativeSensitivity;
                    FNM=PredictiveGridOptimizationBlock.(PGOName).FlexibilityNeedMargin;
                    MaxVoltage=PredictiveGridOptimizationBlock.(PGOName).MaxVoltage;
                    MinVoltage=PredictiveGridOptimizationBlock.(PGOName).MinVoltage;
                    UpperAmberBandVoltage=PredictiveGridOptimizationBlock.(PGOName).UpperAmberBandVoltage;
                    LowerAmberBandVoltage=PredictiveGridOptimizationBlock.(PGOName).LowerAmberBandVoltage;
                    OverloadingBaseline=PredictiveGridOptimizationBlock.(PGOName).OverloadingBaseline;
                    AmberLoadingBaseline=PredictiveGridOptimizationBlock.(PGOName).AmberLoadingBaseline;

                    Object(NumOfSimRun)=PredictiveGridOptimization(SimulationSpecificExchange,SimulationId(NumOfSimRun),PGOName,Grid,RS,FNM,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
%                     Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main;
%                     States{NumOfSimRun}=parfeval(@() Object.Main,1);
                    Object(NumOfSimRun).Main
                end  
        end       
    end
end
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%InboundMessage.SimulationSpecificExchange="simexe30";
% InboundMessage.SimulationSpecificExchange="simexe30";
% InboundMessage.SimulationId="SimTest30";
% 
% PGOName="PredictiveGridOptimizationA";
% InboundMessage.PredictiveGridOptimization.MonitoredGridName="Grid";
% InboundMessage.PredictiveGridOptimization.RelativeSensitivity=0;
% InboundMessage.PredictiveGridOptimization.MaxVoltage=1.05;
% InboundMessage.PredictiveGridOptimization.MinVoltage=0.95;
% InboundMessage.PredictiveGridOptimization.UpperAmberBandVoltage=0.01;
% InboundMessage.PredictiveGridOptimization.LowerAmberBandVoltage=0.01;
% InboundMessage.PredictiveGridOptimization.OverloadingBaseline=1;
% InboundMessage.PredictiveGridOptimization.AmberloadingBaseline=0.9;
% 
% NumOfSimRun=1;
% Object(NumOfSimRun)=PredictiveGridOptimization("simexe30","SimTest30",PGOName,"Grid",40,1.05,0.95,0.01,0.01,1,0.9);   
% Object(NumOfSimRun).Main;
% InboundMessage.SimulationSpecificExchange='simexe31';
% InboundMessage.SimulationId='SimTest31';
% NumOfSimRun=2;
% Object(NumOfSimRun)=StateMonitoring(InboundMessage.SimulationSpecificExchange,InboundMessage.SimulationId);   

% parfor i=1:NumOfSimRun
%     Object(i).Main;
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% function ManagementCallback(hObject, eventData)
%    global NumOfSimRun
%    global Handles
%    global States
%    
%    mystr = java.lang.String(eventData.message, 'UTF-8');
%    str = char(mystr);  %    Making the input into a character array
%    InboundMessage = jsondecode(str); % decoding JSON data
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     if strcmp(InboundMessage.Type,'Start')
%         if NumOfSimRun==0 
%         NumOfSimRun=NumOfSimRun+1
%         StateMonitoingBlock=InboundMessage.ProcessParameters.StateMonitoring
%         SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
%         SimulationId=InboundMessage.SimulationId;
% 
%         fields = fieldnames(StateMonitoingBlock)
%         GridName = fields{1,1}
%         
%         Grid=StateMonitoingBlock.(GridName).MonitoredGridName;
%         MaxVoltage=StateMonitoingBlock.(GridName).MaxVoltage;
%         MinVoltage=StateMonitoingBlock.(GridName).MinVoltage;
%         UpperAmberBandVoltage=StateMonitoingBlock.(GridName).UpperAmberBandVoltage;
%         LowerAmberBandVoltage=StateMonitoingBlock.(GridName).LowerAmberBandVoltage;
%         OverloadingBaseline=StateMonitoingBlock.(GridName).OverloadingBaseline;
%         AmberLoadingBaseline=StateMonitoingBlock.(GridName).AmberLoadingBaseline;
% 
%         Object(NumOfSimRun)=StateMonitoring(SimulationSpecificExchange,SimulationId,GridName,Grid,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
% %       Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main
% %         States{NumOfSimRun}=parfeval(@() Object.Main,1)
%         parfor i=1:NumOfSimRun
%             Object(i).Main;
%         end
%         end
%     end
% end


