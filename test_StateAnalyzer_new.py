# Phase Analyzer re-write:

# 1) Create a class called StateAnalyzer which will do the following:
   # * Read in the logged data
   # * Scan the data to detect when the different phases start and stop
   # * Package up the collected data into State classes
   
# Example:
import os
absFilePath = os.path.abspath(__file__)
os.chdir( os.path.dirname(absFilePath) )
import numpy as np

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def make_time(unix_time):
    return matplotlib.dates.date2num()
def COLUMN(matrix, i):
    return [row[i] for row in matrix]
        
        
class State:
    def __init__(self,name,start,end,state):
        self.start_time = start
        self.end_time   = end
        self.barrel     = name
        self.state_name = state
        self.beater=0
    def __str__(self):
        return self.barrel
        
    def length(self):
        return self.end_time - self.start_time    

        
        
        
class StateAnalyzer:
    def __init__(self, log_file):
        #condition_data() # Sometimes there are data transmission errors in tera term so you'll need to detect and ignore invalid data
        # self.data=[]
        # inp=open(log_file,'r')
        # for line in inp.readlines():
            # self.data.append([])
            # for i in line.split():
                # self.data[-1].append(int(i))
        
        self.data = np.fromfile(log_file, int, -1, "\t")
        self.columns=39#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- I actually went and counted the number of columns in the output data
        self.data=np.reshape(self.data,(np.size(self.data)/self.columns,self.columns))#-------------------------------------------------------------------------------------------------------------------------- to reshape the newly aqcuired dataset to represent the output data
        self.time=COLUMN(self.data,1)#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- the data columns IS 1 because 0 in the output refers to the unit's serial number.
        self.time_easy=self.time-min(self.time)
    
    
    
    
    
    
    def bar_counter(self):
        import time
        self.number_of_data=7 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is the number of columns of data per barrel.
        
        self.number_of_barrels=(np.size(self.data,1)-11)/self.number_of_data       
        lack_data=0
        for barrel in range(self.number_of_barrels):
            print "Barrel: %s"%(barrel+1)#---------------------------------------------------------------------------
            
            run=0
            for row in range(100,150):
                print self.data[row][11+7*barrel]
                if self.data[row][11+7*barrel]==0:
                    run+=1
            if run!=0:
                print "BARREL %s IS NON-EXISTENT. REDUCING NUMBER OF BARRELS BY 1."%(barrel+1)
                ###time.sleep(5)
                lack_data+=1
                print self.number_of_barrels-lack_data
                ###time.sleep(5)
                self.number_of_barrels+=-1
                print self.number_of_barrels
                ###time.sleep(5)
        return self.number_of_barrels
    
    
    
    
    
    
    def StatePopulator(self,num_barr):
        self.number_of_data=7 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is the number of columns of data per barrel.
        #self.number_of_barrels=4#--------------------------------------------------------------- CRITICAL HARDCODE VALUE. DO NOT CHANGE . -------------------------------------------------------------------------------------------------------- this is a CRITICAL HARDCODED VALUE. 
        
        self.state_data=self.data
        #self.state_data=np.append(self.state_data,self.time)
        self.state_data=np.delete(self.state_data,0,axis=1)
        self.state_data=np.delete(self.state_data,np.s_[1:14],axis=1)
        #print self.state_data[1019:1023]
        print self.number_of_barrels
        import time
        for i in range(self.number_of_barrels):
            self.state_data=np.delete(self.state_data,np.s_[(3+2*i):(8+2*i)],axis=1)
            #print np.transpose(self.state_data[1019:1020]),"-"*5
            ###time.sleep(3)
           
        for j in range((self.number_of_barrels-num_barr)*2):
            self.state_data=np.delete(self.state_data,(-1),axis=1)
            #print np.transpose(self.state_data[1019:1020])
        return self.state_data
    
    
    
    
    
    def analysis_state(self,row,num_barr):#------------------------------------------------------------------------ GARY'S MODIFIED-FOR-MY-CLASS STATE MACHINE ---------------------------------------------------------------------------------- this will take in itself and analyze its states.
        IPDtrack=["IPD","IPD","IPD","IPD"]
        if num_barr==1:
            rowtrack=[row[1]]
        if num_barr==2:
            rowtrack=[row[1],row[3]]
        if num_barr==3:
            rowtrack=[row[1],row[3],row[5]]
        if num_barr==4:
            rowtrack=[row[1],row[3],row[5],row[7]]
        IPDtrack=IPDtrack[0:num_barr]
        

        if np.all(np.equal(rowtrack,8)):
            return IPDtrack
           
        barrel_cols = [ (1,2),(3,4),(5,6),(7,8)]
        barrel_cols=barrel_cols[0:num_barr]
        output = []
        for frz_col, def_col in barrel_cols:
            if row[frz_col] == 8:
                output.append("Freezing")
            elif row[def_col] == 11:
                output.append("Defrosting")
            else:
                output.append("Other")
        
        return output
    
    
    
    
    
    def get_dataset(self,num_barr):
    
        self.data_analysis_states = [ "Other", "Other","Other","Other" ]
        self.data_analysis_states=self.data_analysis_states[0:num_barr]
        return self.data_analysis_states
    
    
    
    
    
    def analysis_of_states(self,num_barr):
        import time
        import numpy as np        
        print ["TIME", "BBL1 - FRZ", "BBL1DEF", "BBL2FRZ", "BBL2DEF","BBL1 row specific state",
        "BBL2 row specific state", "BBL1 Data Analysis State", "BBL2 Data Analysis State"]
        # timecap={}
        # for i in range(num_barr):#--------------------------------------------------------------------------- there are n amount of barrels to keep track of, per the input parameter.
            # timecap[i]={}
            # for j in range(3):#------------------------------------------------------------------------------ there are 3 states to keep track of
                # timecap[i][j]=["Start","Finish"]

        #print timecap
        #return

        ###time.sleep(10)
        #print Data[0][0],##time.sleep(5)

        ipditeration={}
        ipdrun={}
        ipdtimerec={}
        ipditerrec=[]
        
        refreeze={}
        refreezeiteration={}
        refreezerunrec={}
        refreezeiterrec=[]
        
        defrost={}
        defrostiteration={}
        defrostrunrec={}
        defrostiterrec=[]
        
        for i in range(num_barr):
            ipdrun[i]={}
            ipdtimerec[i]=0
            ipditeration[i]=0
            ipdrun[i][ipditeration[i]]=State(ipditeration[i],None,None,None)
            ipditerrec.append([])
            ipditerrec[i].append(0)
            
        
            refreeze[i]={}
            refreezerunrec[i]=0
            refreezeiteration[i]=0
            refreeze[i][refreezeiteration[i]]=State(refreezeiteration[i],None,None,None)
            refreezeiterrec.append([])
            refreezeiterrec[i].append(0)
            
            defrost[i]={}
            defrostrunrec[i]=0
            defrostiteration[i]=0
            defrost[i][defrostiteration[i]]=State(defrostiteration[i],None,None,None)   
            defrostiterrec.append([])
            defrostiterrec[i].append(0)
                
                
                
        data_analysis_states=self.get_dataset(num_barr)
               
        for row in self.state_data:
            row_state = self.analysis_state(row,num_barr)
                
            for barrel, barrel_state in enumerate(row_state):
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                        
                if "IPD" in row_state and  ipdtimerec[barrel]==0:#------------------------------------------------------------------------------------------------------------------------------------- When it enters IPD state.

                        
                        #print"\n\n capturing ipd START in IPD interval: ", ipdrun[ipditeration].barrel
                        ###time.sleep(5)
                        ipdrun[barrel][ipditeration[barrel]].start_time=row[0]-self.state_data[0][0]
                        ipdrun[barrel][ipditeration[barrel]].state_name=row_state[barrel]
                        ipdrun[barrel][ipditeration[barrel]].barrel=barrel
                        
                        
                if "Freezing" in row_state[barrel] and refreezerunrec[barrel]==0 and not "IPD" in data_analysis_states:
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        refreeze[barrel][refreezeiteration[barrel]].start_time=row[0]-self.state_data[0][0]
                        refreeze[barrel][refreezeiteration[barrel]].barrel=barrel
                        refreeze[barrel][refreezeiteration[barrel]].state_name=row_state[barrel]
                        #print "\n\n capturing FRZ Start in Barrel: " ,barrel, "Duration interval: ",refreezeiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        ###time.sleep(3)
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        
                if not "Freezing" in row_state[barrel] and refreezerunrec[barrel]==1 and not "IPD" in data_analysis_states:
                        refreeze[barrel][refreezeiteration[barrel]].end_time=row[0]-self.state_data[0][0]
                        refreezerunrec[barrel]=10                    
                        #print "\n\n capturing FRZ end in Barrel: " ,barrel, "Duration interval: ",refreezeiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        ###time.sleep(3)
                        #print "\n\n Duration end for FRZ in barrel: ",barrel,"Creating new time interval in barrel to allow recording. OLD interval: ", refreezeiteration[barrel]
                        refreezeiteration[barrel]+=1
                        refreezeiterrec.append(0)
                        print "To: ",refreezeiteration[barrel]
                        refreeze[barrel][refreezeiteration[barrel]]=State(refreezeiteration[i],None,None,None)
                        ###time.sleep(10)
                        refreezerunrec[barrel]=0
                        
                        
                        
                if "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==0:
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        defrost[barrel][defrostiteration[barrel]].start_time=row[0]-self.state_data[0][0]
                        defrost[barrel][defrostiteration[barrel]].barrel=barrel
                        defrost[barrel][defrostiteration[barrel]].state_name=row_state[barrel]
                        #print "\n\n capturing DEF Start in Barrel: " ,barrel, "Duration interval: ",defrostiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        ###time.sleep(3)
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        
                if not "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==1:
                        defrost[barrel][defrostiteration[barrel]].end_time=row[0]-self.state_data[0][0]
                        defrostrunrec[barrel]=10                    
                        #print "\n\n capturing DEF end in Barrel: " ,barrel, "Duration interval: ",defrostiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        ###time.sleep(3)
                        #print "\n\n Duration end for DEF in barrel: ",barrel,"Creating new time interval in barrel to allow recording. OLD interval: ", defrostiteration[barrel]
                        defrostiteration[barrel]+=1
                        defrostiterrec.append(0)
                        print "To: ",defrostiteration[barrel]
                        defrost[barrel][defrostiteration[barrel]]=State(defrostiteration[i],None,None,None)
                        ###time.sleep(10)
                        defrostrunrec[barrel]=0                        

                if not "IPD" in data_analysis_states and ipdtimerec[barrel]==1:

                   
                    #print"\n\n capturing ipd END in IPD interval: ", ipdrun[ipditeration].barrel
                    ipdrun[barrel][ipditeration[barrel]].end_time=row[0]-self.state_data[0][0]
                    ipditeration[barrel]+=1
                    ipditerrec.append(0)
                    ipdrun[barrel][ipditeration[barrel]]={}
                    ipdrun[barrel][ipditeration[barrel]]=State(ipditeration[barrel],None,None,None)
                    ipdtimerec[barrel]=0 
                    #print "\n\n new IPDrecorder created: ",ipdrun[ipditeration].barrel," Previous: ",ipdrun[ipditeration-1].barrel
                    ###time.sleep(5)
                    #return

                
                    
                    
                    
                if data_analysis_states[barrel] != barrel_state:
                  
                    print "State transition"
                
                    
                # Let's say that we're transitioning from an IPD state to another state
                # Per our definition the IPD continues until all barrels have existed
                # the freeze state - so we need to only change the barrel state when
                # all of the barrels are no longer in IPD
                

                if data_analysis_states[barrel] == "IPD":
                    
                    # any other barrels still freezing?
                    if "Freezing" in row_state:
                        
                        pass # Don't modify the currently stored analysis state
                    else:
                        # At this point all barrels will have existed the IPD state
                        data_analysis_states[barrel] = barrel_state
                    
                else:
                    data_analysis_states[barrel] = barrel_state
                    
                    
                    
                if "IPD" in row_state and ipdtimerec[barrel]==0:#----------------------------------------------------- CRITICAL IPD HARDCODE. DO NOT TOUCH. DO NOT MOVE. ---------------------------------------------------------- this must be here in order for the IPD recording to start.


                    #ipditeration+=1 #-----------------------------------------here is to say that the IPD recording phase has ended and a new one can start, IF the system enters ipd phase again.
                    ipdtimerec[barrel]=1
                if not "IPD" in data_analysis_states and ipditeration!=0 and ipdtimerec[barrel]!=0:
                        #print "\n\n IPD start time recorded already after new recorder made. State Transition found. recording END TIME."
                        ###time.sleep(3)
                        ipdtimerec[barrel]=0
                        #print"\n\n capturing ipd END in IPD interval: ", ipdrun[ipditeration].barrel
                        ipdrun[barrel][ipditeration[barrel]].end_time=row[0]-self.state_data[0][0]
                        ipditeration[barrel]+=1
                        ipditerrec.append(0)
                        ipdrun[barrel][ipditeration[barrel]]={}
                        ipdrun[barrel][ipditeration[barrel]]=State(ipditeration[barrel],None,None,None)
                        ipdtimerec[barrel]=0 
                        #print "\n\n new IPDrecorder created: ",ipdrun[ipditeration].barrel," Previous: ",ipdrun[ipditeration-1].barrel
                        ###time.sleep(5)    
                    
                # if "IPD" in row_state and ipdtimerec==1 and ipditeration !=0:
                    # ipdtimerec=0
                   
            #refreezerunrec[barrel]=0



                if "Freezing" in row_state[barrel] and refreezerunrec[barrel]==0 and not "IPD" in data_analysis_states:
                    #print "\n\n FRZ start time already recorded in barrel: ",barrel,"shifting staterunrecorder in barrel from: ", refreezerunrec[barrel]," to 1 to allow a recording of end time."
                    refreezerunrec[barrel]=1
                    ###time.sleep(10)
                    
                if "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==0:
                    #print "\n\n FRZ start time already recorded in barrel: ",barrel,"shifting staterunrecorder in barrel from: ", defrostrunrec[barrel]," to 1 to allow a recording of end time."
                    defrostrunrec[barrel]=1
                    ###time.sleep(10)



            
            #print row , row_state ,data_analysis_states
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.ipd=ipdrun
        self.refreeze=refreeze
        self.defrost=defrost
        self.ipditerrec=ipditerrec
        self.defrostiterrec=defrostiterrec
        self.refreezeiterrec=refreezeiterrec

                
        ''''''
        for i in range(num_barr):
            print "------------------------------------------< Barrel Number: ",i,">------------------------------------------"
            if np.size(ipdrun.items())>0:
                for l in range(ipditeration[i]):#-----------debug
                    print "     IPD Duration Iteration:      ",l
                    print "                                    IPD Start:      ",ipdrun[i][l].start_time,"\n                                    IPD End:        ",ipdrun[i][l].end_time,"\n                                    IPD Length:     ",ipdrun[i][l].length()   
            if np.size(refreezeiteration.items())>2:
                for j in range(refreezeiteration[i]):
                    print "     Refreeze Duration Iteration: ",j
                    print "                                    Refreeze Start: ",refreeze[i][j].start_time,"\n                                    Refreeze End:   ",refreeze[i][j].end_time,"\n                                    Refreeze Length:",refreeze[i][j].length()   
            if np.size(defrostiteration.items())>2:
                for k in range((defrostiteration[i])):
                    print "     Defrost Duration Iteration:  ",k
                    print "                                    Defrost Start:  ",defrost[i][k].start_time,"\n                                    Defrost End:    ",defrost[i][k].end_time,"\n                                    Defrost Length: ",defrost[i][k].length()   
                print"\n"
        ''''''
        self.ipditeration=ipditeration
        self.refreezeiteration=refreezeiteration
        self.defrostiteration=defrostiteration
        return  
    
    
    
    
    
    def statecleaner(self,num_barr):
        self.newstate=State(None,None,None,None)
        import time
        for i in range(num_barr):
            print "------------------------------------------< Barrel Number: ",i,">------------------------------------------"
            if np.size(self.ipd.items())>0:
                for l in range(self.ipditeration[i]):#-----------debug
                    print "     IPD Duration Iteration:      ",l
                    print "                                    IPD Start:      ",self.ipd[i][l].start_time,"\n                                    IPD End:        ",self.ipd[i][l].end_time,"\n                                    IPD Length:     ",self.ipd[i][l].length()   
            if np.size(self.refreezeiteration.items())>2:
                for j in range(self.refreezeiteration[i]):
                    print "     Refreeze Duration Iteration: ",j
                    print "                                    Refreeze Start: ",self.refreeze[i][j].start_time,"\n                                    Refreeze End:   ",self.refreeze[i][j].end_time,"\n                                    Refreeze Length:",self.refreeze[i][j].length()   
            if np.size(self.defrostiteration.items())>2:
                for k in range((self.defrostiteration[i])):
                    print "     Defrost Duration Iteration:  ",k
                    print "                                    Defrost Start:  ",self.defrost[i][k].start_time,"\n                                    Defrost End:    ",self.defrost[i][k].end_time,"\n                                    Defrost Length: ",self.defrost[i][k].length()   
                print"\n"
        
        
        

        #---------------------------- REFREEZE CLENAUP --------------------------------------
        self.clean_ref={}
        clean_ref_iteration={}
        self.clean_def={}
        clean_def_iteration={}
        self.clean_ipd={}
        clean_ipd_iteration={}
        for barrel in range(num_barr):
        
            self.clean_ref[barrel]={}
            clean_ref_iteration[barrel]=0
            self.clean_ref[barrel][clean_ref_iteration[barrel]]={}
            
            self.clean_def[barrel]={}
            clean_def_iteration[barrel]=0
            self.clean_def[barrel][clean_def_iteration[barrel]]={}
            
            self.clean_ipd[barrel]={}
            clean_ipd_iteration[barrel]=0
            self.clean_ipd[barrel][clean_ipd_iteration[barrel]]={}
            
            ###time.sleep(3)
        if np.size(self.refreezeiteration.items())>2:#------------------------ Test to see if there is even a refreeze
            for barrel in range(num_barr):
                print "Barrel: %s"%barrel
                ####time.sleep(1)
                
                
                
                
                
                for IPDiteration in range(self.ipditeration[barrel]):#-------- for every ipditeration per barrel to check for an overlap
                    print "     IPD Iteration: %s"%IPDiteration
                   
                    ##------------------------------------------------------------- IPD CLEANING --------------------------------------------------------------------------------------
                    if self.ipd[barrel][IPDiteration].length()<30:
                        print "                     ITERATION FAILED. SHORT DURATION PRESENT: Barrel: %s  IPD Iteration: %s Duration Duration: %s"%(barrel,IPDiteration,self.ipd[barrel][IPDiteration].length())
                        ###time.sleep(1)
                        #break
                    else:
                        self.clean_ipd[barrel][clean_ipd_iteration[barrel]]=self.ipd[barrel][IPDiteration]
                        clean_ipd_iteration[barrel]+=1
                        print "                     Iteration passed. Barrel: %s IPD iteration: %s Shift Clean Iteration %s--->%s"%(barrel,IPDiteration,clean_ipd_iteration[barrel]-1,clean_ipd_iteration[barrel])






               ###time.sleep(1)
                ##------------------------------------------------------------- REFREEZE CLEANING --------------------------------------------------------------------------------------
                for iteration in range(self.refreezeiteration[barrel]) or range(np.size(self.refreezeiteration[barrel])):#---------- for every refreeze iteration per barrel
                    print "         Refreeze Iteration: %s"%iteration
                    ###time.sleep(1)
                    test_for_overlap=0
                    
                    if self.refreezeiteration[barrel]>0:
                    
                        for IPDiteration in range(self.ipditeration[barrel]):
                            #test_for_overlap=1
                            if self.refreeze[barrel][iteration].end_time <= self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].start_time >= self.ipd[barrel][IPDiteration].start_time or self.refreeze[barrel][iteration].start_time <=self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].end_time>=self.ipd[barrel][IPDiteration].start_time: 
                                
                                test_for_overlap=1
                                print "                     ITERATION FAILED. OVERLAP PRESENT:        Barrel: %s Refreze Iteration: %s  Duration overlap: %s [%s-%s] %s"%(barrel,iteration,self.ipd[barrel][IPDiteration].start_time,self.refreeze[barrel][iteration].start_time,self.refreeze[barrel][iteration].end_time,self.ipd[barrel][IPDiteration].end_time)
                                ###time.sleep(1)
                             #   break
                        for IPDiteration in range(self.ipditeration[barrel]):
                            if self.refreeze[barrel][iteration].length()<30:
                                print "                     ITERATION FAILED. SHORT DURATION PRESENT: Barrel: %s  Refreeze Iteration: %s Duration Duration: %s"%(barrel,iteration,self.refreeze[barrel][iteration].length())
                                test_for_overlap=1
                                ###time.sleep(1)
                                #break
                            
                        for IPDiteration in range(self.ipditeration[barrel]):#if test_for_overlap==0 and self.refreeze[barrel][iteration].end_time > self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].start_time > self.ipd[barrel][IPDiteration].start_time or self.refreeze[barrel][iteration].start_time <self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].end_time<self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].length()<30 and test_for_overlap==0: 
                            if test_for_overlap==0 and self.refreeze[barrel][iteration].end_time > self.ipd[barrel][IPDiteration].end_time and self.refreeze[barrel][iteration].start_time > self.ipd[barrel][IPDiteration].end_time or test_for_overlap==0 and self.refreeze[barrel][iteration].start_time < self.ipd[barrel][IPDiteration].start_time and self.refreeze[barrel][iteration].end_time < self.ipd[barrel][IPDiteration].start_time and self.refreeze[barrel][iteration].length()>30:    
                                self.clean_ref[barrel][clean_ref_iteration[barrel]]=self.refreeze[barrel][iteration]
                                clean_ref_iteration[barrel]+=1
                                print "                     Iteration passed. Barrel: %s Refreeze iteration: %s Shift Clean Iteration %s--->%s"%(barrel,iteration,clean_ref_iteration[barrel]-1,clean_ref_iteration[barrel])
                                ###time.sleep(1)
                        
                        
                        
                        if np.size(range(self.ipditeration[barrel]))==0:
                            if test_for_overlap==0 and self.refreeze[barrel][iteration].length()>30:    
                                self.clean_ref[barrel][clean_ref_iteration[barrel]]=self.refreeze[barrel][iteration]
                                clean_ref_iteration[barrel]+=1
                                print "                     Iteration passed. Barrel: %s Refreeze iteration: %s Shift Clean Iteration %s--->%s"%(barrel,iteration,clean_ref_iteration[barrel]-1,clean_ref_iteration[barrel])
                                ###time.sleep(1)
    
                ##------------------------------------------------------------- DEFROST CLEANING --------------------------------------------------------------------------------------
                for iteration in range(self.defrostiteration[barrel]) or range(np.size(self.defrostiteration[barrel])):#---------- for every defrost iteration per barrel
                    for IPDiteration in range(self.ipditeration[barrel]):
                        print "         Refreeze Iteration: %s"%iteration
                        ###time.sleep(1)
                        if self.defrost[barrel][iteration].end_time <= self.ipd[barrel][IPDiteration].end_time or self.defrost[barrel][iteration].start_time >= self.ipd[barrel][IPDiteration].start_time and self.defrost[barrel][iteration].start_time <=self.ipd[barrel][IPDiteration].end_time: 
                            
                            test_for_overlap=1
                            print "                     ITERATION FAILED. OVERLAP PRESENT:        Barrel: %s Refreze Iteration: %s  Duration overlap: %s [%s-%s] %s"%(barrel,iteration,self.ipd[barrel][IPDiteration].start_time,self.defrost[barrel][iteration].start_time,self.defrost[barrel][iteration].end_time,self.ipd[barrel][IPDiteration].end_time)
                            ###time.sleep(1)
                         #   break
                        print self.defrostiteration[barrel]
                        if self.defrostiteration[barrel]>0:
                            if self.defrost[barrel][iteration].length()<30:
                                print "                     ITERATION FAILED. SHORT DURATION PRESENT: Barrel: %s  Refreeze Iteration: %s Duration Duration: %s"%(barrel,iteration,self.defrost[barrel][iteration].length())
                                ###time.sleep(1)
                                #break
                            elif self.defrost[barrel][iteration].end_time > self.ipd[barrel][IPDiteration].end_time and self.defrost[barrel][iteration].start_time > self.ipd[barrel][IPDiteration].start_time or self.defrost[barrel][iteration].start_time <self.ipd[barrel][IPDiteration].end_time and self.defrost[barrel][iteration].end_time<self.ipd[barrel][IPDiteration].end_time and self.defrost[barrel][iteration].length()<30: 
                                self.clean_def[barrel][clean_def_iteration[barrel]]=self.defrost[barrel][iteration]
                                clean_def_iteration[barrel]+=1
                                print "                     Iteration passed. Barrel: %s Refreeze iteration: %s Shift Clean Iteration %s--->%s"%(barrel,iteration,clean_def_iteration[barrel]-1,clean_def_iteration[barrel])
                                # ###time.sleep(1)        
                    if np.size(range(self.ipditeration[barrel]))==0:
                        if self.defrost[barrel][iteration].length()>30: 
                            self.clean_def[barrel][clean_def_iteration[barrel]]=self.defrost[barrel][iteration]
                            clean_def_iteration[barrel]+=1
                            print "                     Iteration passed. Barrel: %s Refreeze iteration: %s Shift Clean Iteration %s--->%s"%(barrel,iteration,clean_def_iteration[barrel]-1,clean_def_iteration[barrel])
                            # ###time.sleep(1)   
        
        
        
        self.ipd=self.clean_ipd
        self.defrost=self.clean_def
        self.ipditeration=clean_ipd_iteration
        self.defrostiteration=clean_def_iteration

                        
                        
        print "\n\n\n\n\n\n"    
        for i in range(num_barr):
            print "------------------------------------------< Barrel Number: ",i,">------------------------------------------"
            if np.size(self.ipd.items())>0:
                for l in range(self.ipditeration[i]):#-----------debug
                    print "     IPD Duration Iteration:      ",l
                    print "                                    IPD Start:      ",self.ipd[i][l].start_time,"\n                                    IPD End:        ",self.ipd[i][l].end_time,"\n                                    IPD Length:     ",self.ipd[i][l].length()   
            if np.size(clean_ref_iteration.items())>2:
                for j in range(clean_ref_iteration[i]):
                    print "     Refreeze Duration Iteration: ",j
                    print "                                    Refreeze Start: ",self.clean_ref[i][j].start_time,"\n                                    Refreeze End:   ",self.clean_ref[i][j].end_time,"\n                                    Refreeze Length:",self.clean_ref[i][j].length()   
            if np.size(self.defrostiteration.items())>2:
                for k in range((self.defrostiteration[i])):
                    print "     Defrost Duration Iteration:  ",k
                    print "                                    Defrost Start:  ",self.defrost[i][k].start_time,"\n                                    Defrost End:    ",self.defrost[i][k].end_time,"\n                                    Defrost Length: ",self.defrost[i][k].length()   
                print"\n"                

        self.refreeze=self.clean_ref
        self.refreezeiteration=clean_ref_iteration
    
    
    
    
    
    def getdata(self,num_barr):
        ipdprops={}
        defprops={}
        refprops={}
        
        
        
        ref_RFG_hi={}
        ref_RFG_lo={}
        ref_V={}
        ref_DC={}
        ref_SUP={}
        ref_RT={}
        ref_BTR={}
        ref_time_value={}
        ref_baseline_value={}
        ref_maxhsp_value={}
        ref_minlsp_value={}
        ref_minrt_value={}
        ref_avgdc_value={}
        ref_avgsupr_value={}
        ref_minvoltage_value={}
        ref_maxvoltage_value={}
        
        def_RFG_hi={}
        def_RFG_lo={}
        def_V={}
        def_DC={}
        def_SUP={}
        def_RT={}
        def_BTR={}
        def_time_value={}
        def_baseline_value={}
        def_maxhsp_value={}
        def_minlsp_value={}
        def_minrt_value={}
        def_avgdc_value={}
        def_avgsupr_value={}
        def_minvoltage_value={}
        def_maxvoltage_value={}
        
        ipd_RFG_hi={}
        ipd_RFG_lo={}
        ipd_V={}
        ipd_DC={}
        ipd_SUP={}
        ipd_RT={}
        ipd_BTR={}
        ipd_time_value={}
        ipd_baseline_value={}
        ipd_maxhsp_value={}
        ipd_minlsp_value={}
        ipd_minrt_value={}
        ipd_avgdc_value={}
        ipd_avgsupr_value={}
        ipd_minvoltage_value={}
        ipd_maxvoltage_value={}
        
        
        import time
        
        #------------------------------------------------------------------------------------------ REFREEZE ---------------------------------------------------------------------------------------------------------
        for ref_barrel in range(num_barr):
            ref_BTR[ref_barrel]={}
            ref_RFG_lo[ref_barrel]={}
            ref_RFG_hi[ref_barrel]={}
            ref_V[ref_barrel]={}
            ref_SUP[ref_barrel]={}
            ref_RT[ref_barrel]={}
            ref_DC[ref_barrel]={}
            
            
            ref_time_value[ref_barrel]={}
            ref_baseline_value[ref_barrel]={}
            ref_maxhsp_value[ref_barrel]={}
            ref_minlsp_value[ref_barrel]={}
            ref_minrt_value[ref_barrel]={}
            ref_avgdc_value[ref_barrel]={}
            ref_avgsupr_value[ref_barrel]={}
            ref_minvoltage_value[ref_barrel]={}
            ref_maxvoltage_value[ref_barrel]={}
            
            #print self.refreezeiteration[ref_barrel]
            for ref_instance in range((self.refreezeiteration[ref_barrel])):
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                ref_RFG_lo[ref_barrel][ref_instance]={}
                ref_RFG_lo[ref_barrel][ref_instance]={}
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((ref_RFG_lo[ref_barrel][ref_instance]),np.s_[0:4],axis=1)
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((ref_RFG_lo[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                ref_RFG_hi[ref_barrel][ref_instance]={}
                ref_RFG_hi[ref_barrel][ref_instance]={}
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((ref_RFG_hi[ref_barrel][ref_instance]),np.s_[0:5],axis=1)
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((ref_RFG_hi[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                ref_V[ref_barrel][ref_instance]={}
                ref_V[ref_barrel][ref_instance]={}
                ref_V[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_V[ref_barrel][ref_instance]=np.delete((ref_V[ref_barrel][ref_instance]),np.s_[0:6],axis=1)
                ref_V[ref_barrel][ref_instance]=np.delete((ref_V[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                ref_RT[ref_barrel][ref_instance]={}
                ref_RT[ref_barrel][ref_instance]={}
                ref_RT[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RT[ref_barrel][ref_instance]=np.delete((ref_RT[ref_barrel][ref_instance]),np.s_[0:7],axis=1)
                ref_RT[ref_barrel][ref_instance]=np.delete((ref_RT[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                ref_SUP[ref_barrel][ref_instance]={}
                ref_SUP[ref_barrel][ref_instance]={}
                ref_SUP[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_SUP[ref_barrel][ref_instance]=np.delete((ref_SUP[ref_barrel][ref_instance]),np.s_[0:8],axis=1)
                ref_SUP[ref_barrel][ref_instance]=np.delete((ref_SUP[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                ref_DC[ref_barrel][ref_instance]={}
                ref_DC[ref_barrel][ref_instance]={}
                ref_DC[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_DC[ref_barrel][ref_instance]=np.delete((ref_DC[ref_barrel][ref_instance]),np.s_[0:9],axis=1)
                ref_DC[ref_barrel][ref_instance]=np.delete((ref_DC[ref_barrel][ref_instance]),np.s_[1:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                ref_BTR[ref_barrel][ref_instance]={}
                ref_BTR[ref_barrel][ref_instance]={}
                ref_BTR[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_BTR[ref_barrel][ref_instance]=np.delete((ref_BTR[ref_barrel][ref_instance]),np.s_[0:12+7*ref_barrel],axis=1)
                ref_BTR[ref_barrel][ref_instance]=np.delete((ref_BTR[ref_barrel][ref_instance]),np.s_[1:],axis=1)    
                
                
                
                
                ref_time_value[ref_barrel][ref_instance]={}
                ref_time_value[ref_barrel][ref_instance]=self.refreeze[ref_barrel][ref_instance].length()
                ref_baseline_value[ref_barrel][ref_instance]={}
                ref_baseline_value[ref_barrel][ref_instance]=self.data[self.refreeze[ref_barrel][ref_instance].start_time][14+7*ref_barrel]
                
                ref_maxhsp_value[ref_barrel][ref_instance]={}
                ref_maxhsp_value[ref_barrel][ref_instance]=np.max(ref_RFG_hi[ref_barrel][ref_instance])
                ref_minlsp_value[ref_barrel][ref_instance]={}
                ref_minlsp_value[ref_barrel][ref_instance]=np.min(ref_RFG_lo[ref_barrel][ref_instance])
                ref_minrt_value[ref_barrel][ref_instance]={}
                ref_minrt_value[ref_barrel][ref_instance]=np.min(ref_RT[ref_barrel][ref_instance])
                
                ref_avgdc_value[ref_barrel][ref_instance]={}
                ref_avgdc_value[ref_barrel][ref_instance]=np.mean(ref_DC[ref_barrel][ref_instance])
                ref_avgsupr_value[ref_barrel][ref_instance]={}
                ref_avgsupr_value[ref_barrel][ref_instance]=np.mean(ref_SUP[ref_barrel][ref_instance])
                
                ref_minvoltage_value[ref_barrel][ref_instance]=np.min(ref_V[ref_barrel][ref_instance])
                ref_maxvoltage_value[ref_barrel][ref_instance]=np.max(ref_V[ref_barrel][ref_instance])
        
        
        
        self.ref_BTR=ref_BTR
        self.ref_RFG_lo=ref_RFG_lo
        self.ref_RFG_hi=ref_RFG_hi
        self.ref_V=ref_V
        self.ref_RT=ref_RT
        self.ref_SUP=ref_SUP
        self.ref_DC=ref_DC        

        #----------------------------------------------------------------------------------------- DEFROST ----------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- DEFROST ----------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- DEFROST ----------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- DEFROST ----------------------------------------------------------------------------------------------------------


        for def_barrel in range(num_barr):
            def_BTR[def_barrel]={}
            def_RFG_lo[def_barrel]={}
            def_RFG_hi[def_barrel]={}
            def_V[def_barrel]={}
            def_SUP[def_barrel]={}
            def_RT[def_barrel]={}
            def_DC[def_barrel]={}
            def_time_value[def_barrel]={}
            def_baseline_value[def_barrel]={}
            def_maxhsp_value[def_barrel]={}
            def_minlsp_value[def_barrel]={}
            def_minrt_value[def_barrel]={}
            def_avgdc_value[def_barrel]={}
            def_avgsupr_value[def_barrel]={}
            def_minvoltage_value[def_barrel]={}
            def_maxvoltage_value[def_barrel]={}
            
            
            #print self.defrostiteration[def_barrel]
            for def_instance in range((self.defrostiteration[def_barrel])):
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                def_RFG_lo[def_barrel][def_instance]={}
                def_RFG_lo[def_barrel][def_instance]={}
                def_RFG_lo[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RFG_lo[def_barrel][def_instance]=np.delete((def_RFG_lo[def_barrel][def_instance]),np.s_[0:4],axis=1)
                def_RFG_lo[def_barrel][def_instance]=np.delete((def_RFG_lo[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                def_RFG_hi[def_barrel][def_instance]={}
                def_RFG_hi[def_barrel][def_instance]={}
                def_RFG_hi[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RFG_hi[def_barrel][def_instance]=np.delete((def_RFG_hi[def_barrel][def_instance]),np.s_[0:5],axis=1)
                def_RFG_hi[def_barrel][def_instance]=np.delete((def_RFG_hi[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                def_V[def_barrel][def_instance]={}
                def_V[def_barrel][def_instance]={}
                def_V[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_V[def_barrel][def_instance]=np.delete((def_V[def_barrel][def_instance]),np.s_[0:6],axis=1)
                def_V[def_barrel][def_instance]=np.delete((def_V[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                def_RT[def_barrel][def_instance]={}
                def_RT[def_barrel][def_instance]={}
                def_RT[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RT[def_barrel][def_instance]=np.delete((def_RT[def_barrel][def_instance]),np.s_[0:7],axis=1)
                def_RT[def_barrel][def_instance]=np.delete((def_RT[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                def_SUP[def_barrel][def_instance]={}
                def_SUP[def_barrel][def_instance]={}
                def_SUP[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_SUP[def_barrel][def_instance]=np.delete((def_SUP[def_barrel][def_instance]),np.s_[0:8],axis=1)
                def_SUP[def_barrel][def_instance]=np.delete((def_SUP[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                def_DC[def_barrel][def_instance]={}
                def_DC[def_barrel][def_instance]={}
                def_DC[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_DC[def_barrel][def_instance]=np.delete((def_DC[def_barrel][def_instance]),np.s_[0:9],axis=1)
                def_DC[def_barrel][def_instance]=np.delete((def_DC[def_barrel][def_instance]),np.s_[1:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                def_BTR[def_barrel][def_instance]={}
                def_BTR[def_barrel][def_instance]={}
                def_BTR[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_BTR[def_barrel][def_instance]=np.delete((def_BTR[def_barrel][def_instance]),np.s_[0:12+7*def_barrel],axis=1)
                def_BTR[def_barrel][def_instance]=np.delete((def_BTR[def_barrel][def_instance]),np.s_[1:],axis=1)   

        
                def_time_value[def_barrel][def_instance]={}
                def_time_value[def_barrel][def_instance]=self.defrost[def_barrel][def_instance].length()
                def_baseline_value[def_barrel][def_instance]={}
                def_baseline_value[def_barrel][def_instance]=self.data[self.defrost[def_barrel][def_instance].start_time][14+7*def_barrel]
                
                def_maxhsp_value[def_barrel][def_instance]={}
                def_maxhsp_value[def_barrel][def_instance]=np.max(def_RFG_hi[def_barrel][def_instance])
                def_minlsp_value[def_barrel][def_instance]={}
                def_minlsp_value[def_barrel][def_instance]=np.min(def_RFG_lo[def_barrel][def_instance])
                def_minrt_value[def_barrel][def_instance]={}
                def_minrt_value[def_barrel][def_instance]=np.min(def_RT[def_barrel][def_instance])
                
                def_avgdc_value[def_barrel][def_instance]={}
                def_avgdc_value[def_barrel][def_instance]=np.mean(def_DC[def_barrel][def_instance])
                def_avgsupr_value[def_barrel][def_instance]={}
                def_avgsupr_value[def_barrel][def_instance]=np.mean(def_SUP[def_barrel][def_instance])
        
                def_minvoltage_value[def_barrel][def_instance]=np.min(def_V[def_barrel][def_instance])
                def_maxvoltage_value[def_barrel][def_instance]=np.max(def_V[def_barrel][def_instance])
        
        
        
        
        
        
        self.def_BTR=def_BTR
        self.def_RFG_lo=def_RFG_lo
        self.def_RFG_hi=def_RFG_hi
        self.def_V=def_V
        self.def_RT=def_RT
        self.def_SUP=def_SUP
        self.def_DC=def_DC   

        #----------------------------------------------------------------------------------------- IPD --------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- IPD --------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- IPD --------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- IPD --------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------- IPD --------------------------------------------------------------------------------------------------------------
        for ipd_barrel in range(num_barr):
            ipd_BTR[ipd_barrel]={}
            ipd_RFG_lo[ipd_barrel]={}
            ipd_RFG_hi[ipd_barrel]={}
            ipd_V[ipd_barrel]={}
            ipd_SUP[ipd_barrel]={}
            ipd_DC[ipd_barrel]={}
            ipd_RT[ipd_barrel]={}
            
            
            ipd_time_value[ipd_barrel]={}
            ipd_baseline_value[ipd_barrel]={}
            ipd_maxhsp_value[ipd_barrel]={}
            ipd_minlsp_value[ipd_barrel]={}
            ipd_minrt_value[ipd_barrel]={}
            ipd_avgdc_value[ipd_barrel]={}
            ipd_avgsupr_value[ipd_barrel]={}

            ipd_minvoltage_value[ipd_barrel]={}
            ipd_maxvoltage_value[ipd_barrel]={}

            for ipd_instance in range(self.ipditeration[ipd_barrel]):
            ## gary: dont use magic numbers or "hardcode numbers" so its easier to come back to when 
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                ipd_RFG_lo[ipd_barrel][ipd_instance]={}
                ipd_RFG_lo[ipd_barrel][ipd_instance]={}
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_lo[ipd_barrel][ipd_instance]),np.s_[0:4],axis=1)
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_lo[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                ipd_RFG_hi[ipd_barrel][ipd_instance]={}
                ipd_RFG_hi[ipd_barrel][ipd_instance]={}
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_hi[ipd_barrel][ipd_instance]),np.s_[0:5],axis=1)
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_hi[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                ipd_V[ipd_barrel][ipd_instance]={}
                ipd_V[ipd_barrel][ipd_instance]={}
                ipd_V[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_V[ipd_barrel][ipd_instance]=np.delete((ipd_V[ipd_barrel][ipd_instance]),np.s_[0:6],axis=1)
                ipd_V[ipd_barrel][ipd_instance]=np.delete((ipd_V[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                ipd_RT[ipd_barrel][ipd_instance]={}
                ipd_RT[ipd_barrel][ipd_instance]={}
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((ipd_RT[ipd_barrel][ipd_instance]),np.s_[0:7],axis=1)
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((ipd_RT[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                ipd_SUP[ipd_barrel][ipd_instance]={}
                ipd_SUP[ipd_barrel][ipd_instance]={}
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((ipd_SUP[ipd_barrel][ipd_instance]),np.s_[0:8],axis=1)
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((ipd_SUP[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                ipd_DC[ipd_barrel][ipd_instance]={}
                ipd_DC[ipd_barrel][ipd_instance]={}
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((ipd_DC[ipd_barrel][ipd_instance]),np.s_[0:9],axis=1)
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((ipd_DC[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                ipd_BTR[ipd_barrel][ipd_instance]={}
                ipd_BTR[ipd_barrel][ipd_instance]={}
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_barrel][ipd_instance].start_time:self.ipd[ipd_barrel][ipd_instance].end_time]),0,axis=1)
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((ipd_BTR[ipd_barrel][ipd_instance]),np.s_[0:12+7*ipd_barrel],axis=1)
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((ipd_BTR[ipd_barrel][ipd_instance]),np.s_[1:],axis=1)

                ipd_time_value[ipd_barrel][ipd_instance]={}
                ipd_time_value[ipd_barrel][ipd_instance]=self.ipd[ipd_barrel][ipd_instance].length()
                ipd_baseline_value[ipd_barrel][ipd_instance]={}
                ipd_baseline_value[ipd_barrel][ipd_instance]=self.data[self.ipd[ipd_barrel][ipd_instance].start_time][14+7*ipd_barrel]
                
                ipd_maxhsp_value[ipd_barrel][ipd_instance]={}
                ipd_maxhsp_value[ipd_barrel][ipd_instance]=np.max(ipd_RFG_hi[ipd_barrel][ipd_instance])
                ipd_minlsp_value[ipd_barrel][ipd_instance]={}
                ipd_minlsp_value[ipd_barrel][ipd_instance]=np.min(ipd_RFG_lo[ipd_barrel][ipd_instance])
                ipd_minrt_value[ipd_barrel][ipd_instance]={}
                ipd_minrt_value[ipd_barrel][ipd_instance]=np.min(ipd_RT[ipd_barrel][ipd_instance])
                
                ipd_avgdc_value[ipd_barrel][ipd_instance]={}
                ipd_avgdc_value[ipd_barrel][ipd_instance]=np.mean(ipd_DC[ipd_barrel][ipd_instance])
                ipd_avgsupr_value[ipd_barrel][ipd_instance]={}
                ipd_avgsupr_value[ipd_barrel][ipd_instance]=np.mean(ipd_SUP[ipd_barrel][ipd_instance])
                
                ipd_minvoltage_value[ipd_barrel][ipd_instance]=np.min(ipd_V[ipd_barrel][ipd_instance])
                ipd_maxvoltage_value[ipd_barrel][ipd_instance]=np.max(ipd_V[ipd_barrel][ipd_instance])
                
                
        self.ipd_BTR=ipd_BTR
        self.ipd_RFG_lo=ipd_RFG_lo
        self.ipd_RFG_hi=ipd_RFG_hi
        self.ipd_V=ipd_V
        self.ipd_RT=ipd_RT
        self.ipd_SUP=ipd_SUP
        self.ipd_DC=ipd_DC


        overall_ipdprops_value={}
        overall_defprops_value={}
        overall_refprops_value={}
        
        for barrel in range(num_barr):
            ipdprops[barrel]={}
            defprops[barrel]={}
            refprops[barrel]={}
            overall_ipdprops_value[barrel]={}
            overall_refprops_value[barrel]={}
            overall_defprops_value[barrel]={}
            
            for instance in range(self.ipditeration[barrel]):
                ipdprops[barrel][instance]={}
                ipdprops[barrel][instance]={0:self.ipd_RFG_lo[barrel][instance]}
                ipdprops[barrel][instance].update({1:self.ipd_RFG_hi[barrel][instance]})
                ipdprops[barrel][instance].update({2:self.ipd_V[barrel][instance]})
                ipdprops[barrel][instance].update({3:self.ipd_RT[barrel][instance]})
                ipdprops[barrel][instance].update({4:self.ipd_SUP[barrel][instance]})
                ipdprops[barrel][instance].update({5:self.ipd_DC[barrel][instance]})
                ipdprops[barrel][instance].update({6:self.ipd_BTR[barrel][instance]})
                
                
                overall_ipdprops_value[barrel][instance]={}
                overall_ipdprops_value[barrel][instance]={0:ipd_time_value[barrel][instance]}
                overall_ipdprops_value[barrel][instance].update({1:ipd_baseline_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({2:ipd_maxhsp_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({3:ipd_minlsp_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({4:ipd_minrt_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({5:ipd_avgdc_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({6:ipd_avgsupr_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({7:ipd_maxvoltage_value[barrel][instance]})
                overall_ipdprops_value[barrel][instance].update({8:ipd_minvoltage_value[barrel][instance]})
                
            for instance in range(self.refreezeiteration[barrel]):
                refprops[barrel][instance]={0:self.ref_RFG_lo[barrel][instance]}
                refprops[barrel][instance].update({1:self.ref_RFG_hi[barrel][instance]})
                refprops[barrel][instance].update({2:self.ref_V[barrel][instance]})
                refprops[barrel][instance].update({3:self.ref_RT[barrel][instance]})
                refprops[barrel][instance].update({4:self.ref_SUP[barrel][instance]})
                refprops[barrel][instance].update({5:self.ref_DC[barrel][instance]})
                refprops[barrel][instance].update({6:self.ref_BTR[barrel][instance]})
                
                overall_refprops_value[barrel][instance]={}
                overall_refprops_value[barrel][instance]={0:ref_time_value[barrel][instance]}
                overall_refprops_value[barrel][instance].update({1:ref_baseline_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({2:ref_maxhsp_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({3:ref_minlsp_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({4:ref_minrt_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({5:ref_avgdc_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({6:ref_avgsupr_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({7:ref_maxvoltage_value[barrel][instance]})
                overall_refprops_value[barrel][instance].update({8:ref_minvoltage_value[barrel][instance]})
                
                
        
            for instance in range(self.defrostiteration[barrel]):
                defprops[barrel][instance]={}
                defprops[barrel][instance]={0:self.def_RFG_lo[barrel][instance]}
                defprops[barrel][instance].update({1:self.def_RFG_hi[barrel][instance]})
                defprops[barrel][instance].update({2:self.def_V[barrel][instance]})
                defprops[barrel][instance].update({3:self.def_RT[barrel][instance]})
                defprops[barrel][instance].update({4:self.def_SUP[barrel][instance]})
                defprops[barrel][instance].update({5:self.def_DC[barrel][instance]})
                defprops[barrel][instance].update({6:self.def_BTR[barrel][instance]})
                
                overall_defprops_value[barrel][instance]={}
                overall_defprops_value[barrel][instance]={0:def_time_value[barrel][instance]}
                overall_defprops_value[barrel][instance].update({1:def_baseline_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({2:def_maxhsp_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({3:def_minlsp_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({4:def_minrt_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({5:def_avgdc_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({6:def_avgsupr_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({7:def_maxvoltage_value[barrel][instance]})
                overall_defprops_value[barrel][instance].update({8:def_minvoltage_value[barrel][instance]})
                
        self.ipdprops=ipdprops
        self.defprops=defprops
        self.refprops=refprops
   
        self.overall_defprops_value=overall_defprops_value
        self.overall_ipdprops_value=overall_ipdprops_value
        self.overall_refprops_value=overall_refprops_value
    
    
    
    
    
    def initialize_Tolerances(self):
        x=0#--------------------------------------------------------------------------- this is just to establish a variable.
        ipd4_rfg_lo=[-0.000000000000002536019852714590 , 0.000000000011345518669780900000 ,- 0.0000000197522549099102 , 0.00001664706297478020 ,- 0.006724643990663730 , 0.99175324899836600 , 69.263097541421400]
        ipd4_rfg_hi=[-0.000000000000001671233289853280 , 0.000000000007514297902526400000 ,- 0.0000000134845063433622 , 0.0000122548193127985 ,- 0.005808119933530340 , 1.228499637374680 , 240.0996924873510]
        ipd4_v=[-0.000000010219440369231500000000 , 0.0000247005464145170 ,- 0.0148580821834490 , 238.0503046341210]
        ipd4_rt=[0.000000000000000097260347078284 ,- 0.000000000000241731002795525000 , 0.00000000001198123703942840 , 0.00000032031829803074 ,- 0.0001377269120588430 ,- 0.1080063010927350 , 77.8986790450428]
        ipd4_sup=[0.000000000000001516325614899410 ,- 0.000000000006656995733620930000 , 0.0000000113658051679730 ,- 0.00000947870686179508 , 0.00395539242335789 ,- 0.7440931725646520 , 53.833304436568700]
        ipd4_duty=[-0.000000000000001001447917092700 , 0.000000000005037361204350060000 ,- 0.00000000935658280286464 , 0.00000796017591734055 ,- 0.002978503986445920 , 0.292399262081752 , 57.0746540017013000]
        ipd4_btr=[-0.000000000000006293026564938570 , 0.0000000000222989697384448 ,- 0.0000000298977027546899 , 0.0000187322649963680 ,- 0.005572228919906410 , 0.7222945639582930 , 970.4022320831530]
        
        def4_rfg_lo=[0.000000000000169630234525366000 ,- 0.0000000002645599403197590 , 0.00000015274102242817700 ,- 0.00004026681066231800 , 0.0051276058117068500 ,- 0.320480089558662000 , 58.0495600670625]
        def4_rfg_hi=[-0.000000000000111489654494239000 , 0.0000000001548563880677550 ,- 0.000000075844192432823600 , 0.00001444959089391550000 ,- 0.000061098402065685600 ,- 0.2937899531360970000 , 166.039483813293000]
        def4_v=[-0.000000000000071417005231571600 , 0.00000000011060616581063700 ,- 0.00000006404594996576890 , 0.0000171174262425305000 ,- 0.0021075429074684300 , 0.102855081920549000 , 238.335532635241000]
        def4_rt=[0.000000000000104498603978258000 ,- 0.00000000018046080006728800 , 0.00000011916350803883600 ,- 0.00003806899801019390000 , 0.00643031473911236000 ,- 0.59244949567088300 , 44.99117677865510]
        def4_sup=[-0.000000000000042478977627734100 , 0.000000000049318072346225300 ,- 0.00000001452872672036640 ,- 0.000002224315321154350 , 0.001768248426005550 ,- 0.3018090831488130 , 22.58937931997050]
        def4_duty=[45]
        def4_btr=[-0.000000000000343859157906408000 , 0.000000000617121691113187 ,- 0.000000440823775947578000 , 0.0001602486681267550 ,- 0.0314566570202913000 , 3.231869855277910 , 894.552790322034]
        
        ref4_rfg_lo=[0.0000000000130709123066733 ,- 0.0000000136503202446935 , 0.0000055161253342159 ,- 0.00107780690053222 , 0.103075387979013, - 4.27346568770697 , 94.1598345915965]
        ref4_rfg_hi=[-0.00000000000327943984608733 , 0.00000000372878850210249 ,-0.00000169349605606151 , 0.000390568372430505 ,-0.0485073282211776 , 3.2210081081822 , 153.275673579752]
        ref4_v=[0.000000000000378418984365667 ,- 0.00000000036550993926092 , 0.000000131952569782895 ,- 0.0000220977498852878 ,0.00178214395474613 ,- 0.0746710031826405 , 240.824317689944]
        ref4_rt=[-0.00000000000347710327361523 , 0.00000000360294629693408 ,-0.00000143195246115459 , 0.000269109743980975 ,- 0.0230079648270963 , 0.494106929873897 , 40.687412924506]
        ref4_sup=[-0.0000000000142852999059852 , 0.0000000149385926045583 ,- 0.00000603552895218374 , 0.0011729378647694 ,- 0.10953542607884 , 4.03794713723142, - 8.27110629642979]
        ref4_duty=[-0.00000000000506330004345779 ,0.00000000538133961191277 , -0.00000225822216997687 , 0.00047623881875663 ,- 0.0522568366818242 , 2.53282849414769 , 37.79592770393]
        ref4_btr=[ -0.0000000000119421885386435 , 0.0000000105009276828418 , -0.00000353345921920926 ,0.000536365360298898 , -0.0366003616928813 ,0.951326072591128, 999.592009961661]


        # ipd4_lo=[ipd4_rfg_lo,ipd4_rfd_hi,ipd4_v,ipd4_rt,ipd4_sup,ipd4_duty,ipd4_btr]*.985
        # ipd4_hi=[ipd4_rfg_lo,ipd4_rfd_hi,ipd4_v,ipd4_rt,ipd4_sup,ipd4_duty,ipd4_btr]*1.15
        ipd4=[ipd4_rfg_lo,ipd4_rfg_hi,ipd4_v,ipd4_rt,ipd4_sup,ipd4_duty,ipd4_btr]
        self.IPD4_tolerances=ipd4
        
        # def4_lo=[def4_rfg_lo,def4_rfd_hi,def4_v,def4_rt,def4_sup,def4_duty,def4_btr]*.985
        # def4_hi=[def4_rfg_lo,def4_rfd_hi,def4_v,def4_rt,def4_sup,def4_duty,def4_btr]*1.15
        def4=[def4_rfg_lo,def4_rfg_hi,def4_v,def4_rt,def4_sup,def4_duty,def4_btr]
        self.DEF4_tolerances=def4

        # ref4_lo=[ref4_rfg_lo,ref4_rfd_hi,ref4_v,ref4_rt,ref4_sup,ref4_duty,ref4_btr]*.985
        # ref4_hi=[ref4_rfg_lo,ref4_rfd_hi,ref4_v,ref4_rt,ref4_sup,ref4_duty,ref4_btr]*1.15
        ref4=[ref4_rfg_lo,ref4_rfg_hi,ref4_v,ref4_rt,ref4_sup,ref4_duty,ref4_btr]
        self.REF4_tolerances=ref4    




        ipd3_rfg_lo=[-0.000000000000014350287034385800 , 0.0000000000418624705020636 ,- 0.00000004785638657790590 , 0.000026590545362421900 ,- 0.007099730424577330000 , 0.700448582478128000 , 51.66330704820280]
        ipd3_rfg_hi=[-0.000000000000048655126930162100 , 0.00000000012232276551327400 ,- 0.00000011861655534460600 , 0.00005532568308944710 ,- 0.01260123087912370 , 1.28316608139096000 , 212.95088669029900]
        ipd3_v=[.000000000000005,-.000000000002,.000000002,-.000001,.0004,-.0416,235.37]
        ipd3_rt=[0.000000000000018712856169593300 ,- 0.0000000000432820532630369 , 0.00000003843418793395970 ,- 0.000016743077354304900 , 0.003951192348258280 ,- 0.5729455941878270000 , 69.6209257511355]
        ipd3_sup=[0.000000000000028640004906863400 ,- 0.0000000000724480156256685 , 0.00000007222288053774400 ,- 0.00003585641403580310000 , 0.00916555578096867000 - 1.10183156458269000 , 54.13292728184290]
        ipd3_duty=[-0.000000000000041179140569363500 , 0.000000000115308005613939 ,- 0.00000012355776372272800 , 0.0000630518147228682000 ,- 0.0152057892940340 , 1.350724058355290 , 33.45259834092480]
        ipd3_btr=[0.000000000000006427150810193500 ,- 0.0000000000281739899510190 , 0.000000032944590788400700 ,- 0.00001765991379851650000 , 0.004316789520414570000 ,- 0.3918914963287630 , 999.397039177799]

        def3_rfg_lo=[0.000000000000007380008598744330 ,- 0.0000000000505897792477820 , 0.0000000407060824019280 ,- 0.00001294213895736600 , 0.0019992693385747800 ,- 0.154807120752589000 , 69.93375899302940]
        def3_rfg_hi=[0.000000000000443388694941489000 ,- 0.00000000046824170813942500 , 0.00000019377135827482100 ,- 0.00004091803664446980 , 0.0049822968628578700 ,- 0.39392522125894600 , 166.776158421315000]
        def3_v=[.000006,0,0,-.0023,0,0,235.1]
        def3_rt=[ -0.000000000000222881865534059000 , 0.0000000001686693253541400 ,- 0.0000000319760759315324000 ,- 0.00000274428320225935000 , 0.00151792003209220 ,- 0.174072689384317000 , 38.291224602307100]
        def3_sup=[-0.000000000000422078989877689000 , 0.00000000040542493541799500 ,- 0.00000014206142872964000 , 0.000022567704383153400 ,- 0.001483777164582270 ,- 0.0009194975131892860 , 7.525628381118130]
        def3_duty=[62]
        def3_btr= [-0.000000000003948002126398000000 , 0.00000000467893899151451 ,- 0.000002218582729402960 , 0.0005415593423634740 ,- 0.073560220070698300 , 5.625047120573210 , 785.6865340841850 ]

        ref3_rfg_lo=[0.000000000000069795296141203300 ,- 0.0000000001617877469009410 , 0.00000014260840504006600 ,- 0.000059602171771311300 , 0.01214062981901520000 - 1.1974190211231000 , 110.00]
        ref3_rfg_hi=[-0.000000000000068859277419135900 , 0.00000000017215806021735900 ,- 0.000000166519715315243000 , 0.0000778869797364097000 ,- 0.0179462548095561000 , 1.861684495706970 , 192.04280918950400]
        ref3_v=[2*(1/(10**15)),-5*(1/(10**12)),5*(1/(10**9)),-3*(1/(10**6)),.0007,-.0718,236.41]
        ref3_rt=[0.000000000000022814439049244800 ,- 0.0000000000529003380547552 , 0.000000047162967962064600 ,- 0.00002059786871977900 , 0.0048087343139350600000 ,- 0.6645670123990600 , 73.894778643991400]
        ref3_sup=[ 0.000000000000014239014552723800 ,- 0.0000000000389410504068270 , 0.0000000423143348853191 ,- 0.0000231033472511573000 , 0.00655407782331355000000 ,- 0.881969831334810000000 , 49.93161423110800]
        ref3_duty=[-0.000000000000065920212740646100 , 0.00000000016924471474124500 ,- 0.0000001688090043616940000 , 0.00008147615733434430000 ,- 0.0189769610258361000 , 1.7078452925536500000 , 22.6475677042086000]
        ref3_btr=[-0.000000000000017145635305073900 , 0.0000000000170986424145307000 ,- 0.00000000121795492191857 ,- 0.00000440528697447917000 , 0.001548200798966900 ,- 0.148158340185274000 , 1000.20768955970        ]
        
        # ipd3_lo=[ipd3_rfg_lo,ipd3_rfd_hi,ipd3_v,ipd3_rt,ipd3_sup,ipd3_duty,ipd3_btr]*.985
        # ipd3_hi=[ipd3_rfg_lo,ipd3_rfd_hi,ipd3_v,ipd3_rt,ipd3_sup,ipd3_duty,ipd3_btr]*1.15
        ipd3=[ipd3_rfg_lo,ipd3_rfg_hi,ipd3_v,ipd3_rt,ipd3_sup,ipd3_duty,ipd3_btr]
        self.IPD3_tolerances=ipd3
        
        # def3_lo=[def3_rfg_lo,def3_rfd_hi,def3_v,def3_rt,def3_sup,def3_duty,def3_btr]*.985
        # def3_hi=[def3_rfg_lo,def3_rfd_hi,def3_v,def3_rt,def3_sup,def3_duty,def3_btr]*1.15
        def3=[def3_rfg_lo,def3_rfg_hi,def3_v,def3_rt,def3_sup,def3_duty,def3_btr]
        self.DEF3_tolerances=def3

        # ref3_lo=[ref3_rfg_lo,ref3_rfd_hi,ref3_v,ref3_rt,ref3_sup,ref3_duty,ref3_btr]*.985
        # ref3_hi=[ref3_rfg_lo,ref3_rfd_hi,ref3_v,ref3_rt,ref3_sup,ref3_duty,ref3_btr]*1.15
        ref3=[ref3_rfg_lo,ref3_rfg_hi,ref3_v,ref3_rt,ref3_sup,ref3_duty,ref3_btr]
        self.REF3_tolerances=ref3  
        self.tols4=[self.IPD4_tolerances,self.DEF4_tolerances,self.REF4_tolerances]
        self.tols3=[self.IPD3_tolerances,self.DEF3_tolerances,self.REF3_tolerances]
        
        barr=self.number_of_barrels
        ipd_time=[]
        if barr==3:
            ipd_time=[19*60,14*60]
        if barr==4:
            ipd_time=[22*60,15*60]
        
        
        ipd_base=[4200,3500]
        ipd_max_HSP=[280,240]
        ipd_min_LSP=[50,40]
        ipd_min_RT=[25,10]
        ipd_avg_DC=[60,30]
        ipd_avg_SH=[15,5]
        ipd_max_voltage=[242,239]
        ipd_min_voltage=[232,230]
        self.ipd_overall_tolerances=[ipd_time,ipd_base,ipd_max_HSP,ipd_min_LSP,ipd_min_RT,ipd_avg_DC,ipd_avg_SH,ipd_max_voltage,ipd_min_voltage]
        
        
        if barr==3:
            def_time=[6*60,3*60]
        if barr==4:
            def_time=[6*60,3*60]
        
        
        def_base=[4200,3500]
        def_max_HSP=[280,240]
        def_min_LSP=[50,40]
        def_min_RT=[25,10]
        def_avg_DC=[60,30]
        def_avg_SH=[15,5]
        def_max_voltage=[242,239]
        def_min_voltage=[232,230]
        self.def_overall_tolerances=[def_time,def_base,def_max_HSP,def_min_LSP,def_min_RT,def_avg_DC,def_avg_SH,def_max_voltage,def_min_voltage]
        

        if barr==3:
            ref_time=[6*60,4.5*60]
        if barr==4:
            ref_time=[6*60,4.5*60]
        
        
        ref_base=[4200,3500]
        ref_max_HSP=[280,240]
        ref_min_LSP=[50,40]
        ref_min_RT=[25,10]
        ref_avg_DC=[60,30]
        ref_avg_SH=[15,5]
        ref_max_voltage=[242,239]
        ref_min_voltage=[232,230]
        self.ref_overall_tolerances=[ref_time,ref_base,ref_max_HSP,ref_min_LSP,ref_min_RT,ref_avg_DC,ref_avg_SH,ref_max_voltage,ref_min_voltage]
        '''
        stateprops=[self.ipdprops,self.defprops,self.refprops]#---------------------------------------- to go through the states in iteration
        statelengths=[self.ipd,self.defrost,self.refreeze]
        stateiters=[self.ipditeration,self.defrostiteration,self.refreezeiteration]
        stats=["RFGLow","RFGHigh", "V", "RTemp", "SUPRHT", "DTYCycles", "BTR%"]
        avg_stateprops={}
        shortest_times={}
        lower_tolerance={}
        higher_tolerance={}
        for state in range(np.size(["IPD","Defrost","Refreeze"])):
            avg_stateprops[state]={}
            shortest_times[state]={}
            lower_tolerance[state]={}
            higher_tolerance[state]={}
            
            for barrel in range(self.number_of_barrels):
                
                shortest=float("inf")
                
                for iteration in range(stateiters[state][barrel]):
                    higher_tolerance[state][iteration]={}
                    lower_tolerance[state][iteration]={}
                    avg_stateprops[state][iteration]={}
                    shortest_times[state][iteration]={}
                    for barrel2 in range(num_barr):
                        if statelengths[state][barrel2][iteration].length()<shortest:
                            shortest=statelengths[state][barrel2][iteration].length()
                            shortest_times[state][iteration]=shortest
                        #print shortest
                    for statistic in range(np.size(stats,0)):
                        avg_stateprops[state][iteration][statistic]=[]
                        higher_tolerance[state][iteration][statistic]=[]
                        lower_tolerance[state][iteration][statistic]=[]
                        for timer in range(shortest):
                            avg_getter=[]
                            for barrel2 in range(self.number_of_barrels):
                                #print stateprops[state][barrel][iteration][statistic][timer], state, barrel, iteration, statistic, timer
                                
                                avg_getter.append(stateprops[state][barrel2][iteration][statistic][timer])
                                
                                
                            #print avg_getter,"\n",np.mean(avg_getter)
                            avg_stateprops[state][iteration][statistic].append(np.mean(avg_getter))
                            
                            higher_tolerance[state][iteration][statistic].append(np.max(avg_getter)*1.025)
                            lower_tolerance[state][iteration][statistic].append(np.min(avg_getter)*.95)
                            #higher_tolerance[state][iteration][statistic].append(avg_stateprops[state][iteration][statistic][timer]*1.025)
                            #lower_tolerance[state][iteration][statistic].append(avg_stateprops[state][iteration][statistic][timer]*.95)
                            #self.low_tolerance_model=avg_stateprops
                        #print avg_stateprops[state][barrel][iteration][statistic]
                            
                # to stop the process from running all barrels
                    
        self.high_tolerance_model=higher_tolerance
        self.low_tolerance_model=lower_tolerance
        self.shortest_times=shortest_times
        #print self.low_tolerance_model.viewkeys(),self.number_of_barrels
        '''
    
    
    
    
    
    
    
    def analyze_tolerances(self,num_barr):
        self.have_I_Failed=0
        self.testErrors=[]
        e_code_0="Missing State: %s State Is Missing in Barrel %s."
        e_code_1="Tolerance Out-of-bounds: %s State, Barrel %s, Interval %s, %s"
        
        
        hightol=1.25
        lowtol=.75
        import time
        Tol_data={}
        self.states=[self.ipdprops,self.defprops,self.refprops]
        Barrel_list=["BBL_1","BBL_2","BBL_3","BBL_4"]
        Barrel_list=Barrel_list[0:num_barr]
        Statistics=["RFG_lo","RFG_hi","V","RTemp","SUPHT","DUTYCycles","BTR%"]
        for barrel in range(num_barr):
            Tol_data[barrel]={}
            for state in ["IPD","Defrost","Refreeze"]:
                Tol_data[barrel][state]={}
                if state=="IPD":
                    for instance in range(np.size(self.states[0][barrel].items(),0)):
                        Tol_data[barrel][state][instance]={}
                        for statistic in ["RFG_lo","RFG_hi","V","RTemp","SUPHT","DUTYCycles","BTR%"]:
                            Tol_data[barrel][state][instance][statistic]=True
                if state=="Defrost":
                    for instance in range(np.size(self.states[1][barrel].items(),0)):
                        Tol_data[barrel][state][instance]={}
                        for statistic in ["RFG_lo","RFG_hi","V","RTemp","SUPHT","DUTYCycles","BTR%"]:
                            Tol_data[barrel][state][instance][statistic]=True
                if state=="Refreeze":
                    for instance in range(np.size(self.states[2][barrel].items(),0)):
                        Tol_data[barrel][state][instance]={}
                        for statistic in ["RFG_lo","RFG_hi","V","RTemp","SUPHT","DUTYCycles","BTR%"]:
                            Tol_data[barrel][state][instance][statistic]=True
        #return
        #print Tol_data["BBL_1"]
        #--------------------------------------------------------IPD TOLERANCE TESTING - 4 BARREL
        if num_barr==4:
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.ipdprops[barrel].items(),0)):
                    print "          Instance of IPD: ",instance
                    for statistic in range(self.ipdprops[barrel][instance].__len__()):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        for timer in range(np.size(self.ipdprops[barrel][instance][statistic],0)):
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.IPD4_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.IPD4_tolerances[statistic],timer))*lowtol
                                if self.ipdprops[barrel][instance][statistic][timer][0] > uppertol or  self.ipdprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.ipdprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.ipdprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["IPD"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.ipdprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.ipdprops[barrel][instance][statistic],0))]
                                    pass
                                    
        #--------------------------------------------------------IPD TOLERANCE TESTING - 3BARREL
        if num_barr==3:
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.ipdprops[barrel].items(),0)):
                    print "          Instance of IPD: ",instance
                    for statistic in range(self.ipdprops[barrel][instance].__len__()):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        
                        for timer in range(np.size(self.ipdprops[barrel][instance][statistic],0)):
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.IPD3_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.IPD3_tolerances[statistic],timer))*lowtol
                                if self.ipdprops[barrel][instance][statistic][timer][0] > uppertol or  self.ipdprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.ipdprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.ipdprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["IPD"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.ipdprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.ipdprops[barrel][instance][statistic],0))]
                                    pass
                        
                        
        
        #-------------------------------------------------------- REF/DEF TOLERANCE TESTING - 4 BARREL
        if num_barr==4:
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.refprops[barrel].items(),0)):
                    print "          Instance of Refreeze:  ",instance
                    #print "Number of instances: ", np.size(self.refprops[barrel].items(),0)
                    #return
                    for statistic in range(np.size(Statistics)):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        for timer in range(np.size(self.refprops[barrel][instance][statistic],0)):
                            
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.REF4_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.REF4_tolerances[statistic],timer))*lowtol
                                if self.refprops[barrel][instance][statistic][timer][0] > uppertol or  self.refprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.refprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.refprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["Refreeze"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.refprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.refprops[barrel][instance][statistic],0))]
                                    pass        
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.defprops[barrel].items(),0)):
                    print "          Instance of Refreeze:  ",instance
                    for statistic in range(self.defprops[barrel][instance].__len__()):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        for timer in range(np.size(self.defprops[barrel][instance][statistic],0)):
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.DEF4_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.DEF4_tolerances[statistic],timer))*lowtol
                                if self.defprops[barrel][instance][statistic][timer][0] > uppertol or  self.defprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.defprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.defprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["Defrost"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.defprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.defprops[barrel][instance][statistic],0))]
                                    pass               
        
        
        #-------------------------------------------------------- REF/DEF TOLERANCE TESTING - 3 BARREL
        if num_barr==3:
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.refprops[barrel].items(),0)):
                    print "          Instance of Refreeze:  ",instance
                    #print "Number of instances: ", np.size(self.refprops[barrel].items(),0)
                    #return
                    for statistic in range(np.size(Statistics)):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        for timer in range(np.size(self.refprops[barrel][instance][statistic],0)):
                            
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.REF3_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.REF3_tolerances[statistic],timer))*lowtol
                                if self.refprops[barrel][instance][statistic][timer][0] > uppertol or  self.refprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.refprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.refprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["Refreeze"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.refprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.refprops[barrel][instance][statistic],0))]
                                    pass        
            for barrel in range(num_barr):
                print "barrel: ",barrel
                for instance in range(np.size(self.defprops[barrel].items(),0)):
                    print "          Instance of Refreeze:  ",instance
                    for statistic in range(self.defprops[barrel][instance].__len__()):
                        print "                               Statistic: ", Statistics[statistic]
                        ###time.sleep(2)
                        #------------------------------- COMMENCING TOLERANCE CHECK. ------------------------------
                        for timer in range(np.size(self.defprops[barrel][instance][statistic],0)):
                            if timer >50:# to give a buffer for the test iteration to get its life together
                                uppertol=(np.polyval(self.DEF3_tolerances[statistic],timer))*hightol
                                lowertol=(np.polyval(self.DEF3_tolerances[statistic],timer))*lowtol
                                if self.defprops[barrel][instance][statistic][timer][0] > uppertol or  self.defprops[barrel][instance][statistic][timer][0] < lowertol:
                                    #print ["UpTol -->",uppertol,self.defprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.defprops[barrel][instance][statistic],0))],"<---------- FAIL ----------- ","Failure at:" , Statistics[statistic]," At Duration: ",timer
                                    ###time.sleep(.01)
                                    Tol_data[barrel]["Defrost"][instance][Statistics[statistic]]=False
                                else:
                                    #print ["UpTol -->",uppertol,self.defprops[barrel][instance][statistic][timer][0],lowertol,"<-- LoTol","Prop: %s"%(Statistics[statistic]),"Duration: %s/%s"%(timer,np.size(self.defprops[barrel][instance][statistic],0))]
                                    pass          
        
        
        
        
        
        
        
        ##------------------------------------------- OVERALL TOLERANCE TESTING -------------------------------------------------------
        self.ipd_verdicts=[]
        self.def_verdicts=[]
        self.ref_verdicts=[]
        for barrel in range(num_barr):
            self.ipd_verdicts.append([])
            self.ref_verdicts.append([])
            self.def_verdicts.append([])
            for instance in range(self.ipditeration[barrel]):
                self.ipd_verdicts[barrel].append([])
                for statistic in range(np.size(self.ipd_overall_tolerances,0)):
                    self.ipd_verdicts[barrel][instance].append("Pass")
                
            for instance in range(self.defrostiteration[barrel]):
                self.def_verdicts[barrel].append([])
                for statistic in range(np.size(self.def_overall_tolerances,0)):
                    self.def_verdicts[barrel][instance].append("Pass")
            for instance in range(self.refreezeiteration[barrel]):
                self.ref_verdicts[barrel].append([])
                for statistic in range(np.size(self.ref_overall_tolerances,0)):
                    self.ref_verdicts[barrel][instance].append("Pass")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        overall_Toldata={}
        self.overall_ipdprops={}
        self.overall_refprops={}
        self.overall_defprops={}
        
        for barrel in range(num_barr):
            self.overall_ipdprops[barrel]={}
            self.overall_refprops[barrel]={}
            self.overall_defprops[barrel]={}
            for state in ["IPD","Defrost","Refreeze"]:
                self.overall_ipdprops[barrel][state]={}
                self.overall_refprops[barrel][state]={}
                self.overall_defprops[barrel][state]={}
                if state=="IPD":
                    for instance in range(self.ipditeration[barrel]):
                        self.overall_ipdprops[barrel][state][instance]={}
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            self.overall_ipdprops[barrel][state][instance][statistic]=True
                if state=="Defrost":
                    for instance in range(self.defrostiteration[barrel]):
                        self.overall_defprops[barrel][state][instance]={}
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            self.overall_defprops[barrel][state][instance][statistic]=True
                if state=="Refreeze":
                    for instance in range(self.refreezeiteration[barrel]):
                        self.overall_refprops[barrel][state][instance]={}
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            self.overall_refprops[barrel][state][instance][statistic]=True
                            
                            
        self.overall_props={}
        self.overall_props[0]=self.overall_ipdprops
        self.overall_props[1]=self.overall_defprops
        self.overall_props[2]=self.overall_refprops
                            
                            
        overall_stateprops=[self.overall_ipdprops_value,self.overall_defprops_value,self.overall_refprops_value]
        #overall_stateprops[state][barrel].__len__()>0:
        errorstats=["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."]
        passme=0
        bigtols=[]                    
        if passme==1:
            bigtols=[100,-100]
        else:
            bigtols=[1,1]
        for barrel in range(num_barr):
            print "     Barrel: %s"%(barrel)
            for state in ["IPD","Defrost","Refreeze"]:
                print "         State: %s"%state
                if state=="IPD":
                    if overall_stateprops[0][barrel].__len__()<1:
                        self.have_I_Failed=1
                        self.testErrors.append(e_code_0%(state,barrel+1))
                        
                        
                    for instance in range(self.ipditeration[barrel]):
                        print "             Instance: %s"%instance
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            print "                 %s Statistic %s"%(state,statistic)
                            if self.overall_ipdprops_value[barrel][instance][statistic]>self.ipd_overall_tolerances[statistic][0]*bigtols[0] or self.overall_ipdprops_value[barrel][instance][statistic]<self.ipd_overall_tolerances[statistic][1]*bigtols[1]:
                                print "                 OVERALL %s STATISTIC FAILED."%(str(state).upper())
                                ###time.sleep(.001)
                                self.overall_ipdprops[barrel][state][instance][statistic]=False
                                self.ipd_verdicts[barrel][instance][statistic]="FAIL"
                                self.have_I_Failed=1
                                self.testErrors.append(e_code_1%(state,barrel+1,instance+1,errorstats[statistic]))
                            else:
                                self.have_I_Failed=0
                if state=="Defrost":
                    if overall_stateprops[1][barrel].__len__()<1:
                        self.have_I_Failed=1
                        self.testErrors.append(e_code_0%(state,barrel+1))
                        
                    for instance in range(self.defrostiteration[barrel]):
                        print "             Instance: %s"%instance
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            print "                 %s Statistic %s"%(state,statistic)
                            if self.overall_defprops_value[barrel][instance][statistic]>self.def_overall_tolerances[statistic][0]*bigtols[0] or self.overall_defprops_value[barrel][instance][statistic]<self.def_overall_tolerances[statistic][1]*bigtols[1]:
                                print "                 OVERALL %s STATISTIC FAILED."%(str(state).upper())
                                ###time.sleep(.001)
                                self.overall_defprops[barrel][state][instance][statistic]=False
                                self.def_verdicts[barrel][instance][statistic]="FAIL"
                                self.have_I_Failed=1
                                self.testErrors.append(e_code_1%(state,barrel+1,instance+1,errorstats[statistic]))
                            else:
                                self.have_I_Failed=0
                if state=="Refreeze":
                    if overall_stateprops[2][barrel].__len__()<1:
                        self.have_I_Failed=1
                        self.testErrors.append(e_code_0%(state,barrel+1))
                        
                    for instance in range(self.refreezeiteration[barrel]):
                        print "             Instance: %s"%instance
                        for statistic in range(np.size(["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."])):
                            print "                 %s Statistic %s"%(state,statistic)
                            if self.overall_refprops_value[barrel][instance][statistic]>self.ref_overall_tolerances[statistic][0]*bigtols[0] or self.overall_refprops_value[barrel][instance][statistic]<self.ref_overall_tolerances[statistic][1]*bigtols[1]:
                                print "                 OVERALL %s STATISTIC FAILED."%(str(state).upper())
                                ###time.sleep(.001)
                                self.overall_refprops[barrel][state][instance][statistic]=False
                                self.ref_verdicts[barrel][instance][statistic]="FAIL"
                                self.have_I_Failed=1
                                self.testErrors.append(e_code_1%(state,barrel+1,instance+1,errorstats[statistic]))
                            else:
                                self.have_I_Failed=0
                                

                                
                                
                                
                                
            
        
        
        
        statelist=["IPD","Defrost","Refreeze"]
        





 
        
        
        
        #print Tol_data[0]["IPD"]                
        print "Tolerance Check Complete."
       

        self.hightol=hightol
        self.lowtol=lowtol
        ###time.sleep(1)
        self.errors={}
        for barrel in range(num_barr):
            print "Barrel Number: %s"%(Barrel_list[barrel])
            self.errors[barrel]={}
            for state in range(np.size(statelist)):
                print "    State: %s"%(statelist[state])
                self.errors[barrel][statelist[state]]={}
                for instance in range(np.size(self.states[state][barrel].items(),0)):
                    print "            Instance : %s" %(instance)
                    self.errors[barrel][statelist[state]][instance]={}
                    for statistic in range(self.states[state][barrel][instance].__len__()):
                        if False in self.states[state][barrel][instance][statistic]:
                            #print "                        Property: %s   |   Result: %s"%(Statistics[statistic],Tol_data[barrel][statelist[state]][instance][Statistics[statistic]])
                            self.errors[barrel][statelist[state]][instance][Statistics[statistic]]=Tol_data[barrel][statelist[state]][instance][Statistics[statistic]]
                            #print "                        Property: %s   |   Result: %s"%(Statistics[statistic],self.errors[barrel][statelist[state]][instance][Statistics[statistic]])
                        print "                        Property: %s   |   Result: %s"%(Statistics[statistic],Tol_data[barrel][statelist[state]][instance][Statistics[statistic]])
                        
                        
                        
        for barrel in range(num_barr):
            print "Barrel: %s"%barrel
            for state in ["IPD","Defrost","Refreeze"]:
                print "     State: %s"%state
                if state=="IPD":
                    for instance in range(np.size(self.ipd_verdicts[barrel],0)):
                        print "         Duration interval: %s"%instance
                        for statistic in range(np.size(self.ipd_verdicts[barrel][instance],0)):
                            print "                 Statistic: %s, VERDICT: %s"%(statistic,self.ipd_verdicts[barrel][instance][statistic])
                if state=="Defrost":
                    for instance in range(np.size(self.def_verdicts[barrel],0)):
                        print "         Duration interval: %s"%instance
                        for statistic in range(np.size(self.def_verdicts[barrel][instance],0)):
                            print "                 Statistic: %s, VERDICT: %s"%(statistic,self.def_verdicts[barrel][instance][statistic])
                if state=="Refreeze":
                    for instance in range(np.size(self.ref_verdicts[barrel],0)):
                        print "         Duration interval: %s"%instance
                        for statistic in range(np.size(self.ref_verdicts[barrel][instance],0)):
                            print "                 Statistic: %s, VERDICT: %s"%(statistic,self.ref_verdicts[barrel][instance][statistic])
                            
        '''  This gives the correct tolerance evaluation.          
        for x in range (np.size(self.IPD4_tolerances)):
            print x,"-------"*10
            for i in range(10):
            
                print np.polyval(self.IPD4_tolerances[x],i)
        
        '''
        self.Tol_data=Tol_data
    
    
    
    
    
    def display_plots_version2(self,num_barr,plottols,shonosho):#--------------------------- IPD PLOTS WILL LOOK SIMILAR BECAUSE THEY ALL OCCUR AT THE SAME TIME AND THE STATISTICS EXCEPT FOR THE BTR% ARE COMMON.
        '''
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        '''
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import matplotlib.ticker as ticker
        import matplotlib
        from matplotlib.backends.backend_pdf import PdfPages
        from datetime import datetime as dt
        import datetime
        from datetime import timedelta
        import time
        import matplotlib.ticker as mtick
        
        '''
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        '''
        
        
        '''
        # ##-------------------------------------------------------------------------- Prerun Definitions ---------------------------------------------------------------------------
        # ##-------------------------------------------------------------------------- Prerun Definitions ---------------------------------------------------------------------------
        '''
        self.stateprops=[self.ipdprops,self.defprops,self.refprops]#---------------------------------------- to go through the states in iteration
        self.statelengths=[self.ipd,self.defrost,self.refreeze]
        self.stateiters=[self.ipditeration,self.defrostiteration,self.refreezeiteration]
        tolerance_plot_equations_4=[self.ipd_overall_tolerances,self.def_overall_tolerances,self.ref_overall_tolerances]
        tolerance_plot_equations_3=[self.ipd_overall_tolerances,self.def_overall_tolerances,self.ref_overall_tolerances]
        
        
        
        
        self.plotting_linestyles=['-' , '-.' , ':' , '--' , 'steps','-','-.',':','-' , '-.' , ':' , '--' , 'steps','-','-.',':']#----------------------------------- to seperate the instances from one another
        self.plotting_marker=[ '+' , '.' , 'd' , '8' , 's' , 'p' , '*']#-------------------------------- to seperate the instances from one another again if needed
        self.plotting_barrelcolor=['b','m','c','y']#--------------------------------------------------------- to seperate the barrels from one another
        deg=u'\N{DEGREE SIGN}'
        self.plotting_UOM=["Psi","Psi","V","%sF"%deg,"%sF"%deg,"%","%"]
        
        Barrels=["BBL_1","BBL_2","BBL_3","BBL_4"]
        Barrels=Barrels[0:num_barr]
        States=["IPD","Defrost","Refreeze"]
        stats=["RFGLow","RFGHigh", "V", "RTemp", "SUPRHT", "DTYCycles", "BTR%"]
        '''
        # ##-------------------------------------------------------------------------- Prerun Definitions ---------------------------------------------------------------------------
        # ##-------------------------------------------------------------------------- Prerun Definitions ---------------------------------------------------------------------------
        '''
        
        
        print "\n          ","---"*10,"< Initializing Plots >","---"*10
        
        #print "State: ",state.upper()
        #state=state.lower()

        ipdpics=[]
        refpics=[]
        defpics=[]


        num_statistics=np.size(stats)
        # print "\n Number of %s Iterations: %s"%(States[state],self.stateiters[state])
        # print "\n Number of Statistics: %s \nDisplaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
        # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
        fixnum=6
        numcols=fixnum/2
        numrows=fixnum/3
        ipdtol=0        
        tol_equations=0
        

        
        for state in range(np.size(self.stateprops)):
            if num_barr==4:
                tol_equations=tolerance_plot_equations_4
                ipdtol=self.IPD4_tolerances
                othertols=self.tols4
            if num_barr==3:
                tol_equations=tolerance_plot_equations_3
                ipdtol=self.IPD3_tolerances
                othertols=self.tols3
                
                
                
                
                
            if state==0:
                skip=0
                for barr in range(num_barr):
                    if np.size(range(self.ipditeration[barr]))==0:
                        skip=1
                imnum=0
                if skip==0:
                    #print numcols," columns, and ",numrows," rows."
                    for statistic in range(1):#range(np.size(stats)):
                        BTRfig=plt.figure()
                        BTRx=0#---------------------------------------------------------------------------
                        upper=[]
                        lower=[]
                        longest=0
                        
                        ## here we will define the y-axis limits to show the plot (which will make the plot nicer to look at when out-of-tolerance).
                        highest=-5000 # These values are set with magic numbers as a way to set the plotting y-axis
                        lowest=5000
                        for barrel in range(num_barr):
                            for iteration in range(self.stateiters[state][barrel]):
                                compare_max=max(self.stateprops[state][barrel][iteration][6])
                                compare_min=min(self.stateprops[state][barrel][iteration][6])
                                if compare_max>highest:
                                    highest=compare_max
                                    highest=highest*1.125
                                if compare_min<lowest:
                                    lowest=compare_min
                                    lowest=lowest*.9875
                        
                        
                        for barrel in range(np.size(Barrels)):
                            #BTRfig=plt.figure()

                            for iteration in range(self.stateiters[state][barrel]):
                                x=[]
                                y=[]
                                lower=[]
                                upper=[]
                                long=[]
                                longer=0
                                print "Iteration ----------------------------->>>>>%s"%iteration
                                for iteration2 in range(self.stateiters[state][barrel]):
                                    lengthtest=np.size(range(self.statelengths[state][barrel][iteration2].start_time,self.statelengths[state][barrel][iteration2].end_time))
                                    
                                    long.append(lengthtest)
                                    print long
                                print long
                                if np.size(long)>0:
                                    longer=max(long)
                                if longer>longest:
                                    longest=longer
                                    
                                BTRx=range(self.statelengths[state][barrel][iteration].length())#range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].end_time)#
                                print "Iteration %s Size of BTRx: %s"%(iteration,np.size(BTRx))
                                ###time.sleep(5)
                                BTRy_hold=self.stateprops[state][barrel][iteration][6]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)
                                plotarray=[]
                                #plotarray.append(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration])
                                

                                #plt.xticks(BTRx,timeplot)
                                plt.locator_params(axis='x',nbins=7)
                                times=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].start_time+tolerance_plot_equations_4[state][0][0])
                                #print times
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%M:%S",time.localtime(pos)))
                                    )
                                
                                

                                for timer in range(longest):
                                    
                                    uppertol=(np.polyval(ipdtol[6],timer))*self.hightol
                                    lowertol=(np.polyval(ipdtol[6],timer))*self.lowtol
                                    
                                    upper.append(uppertol)
                                    lower.append(lowertol)
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1)) ##------------------ if there is an error here, it means there are not enough styles for which to plot the different iterations
                                plt.hold(True)
                                plt.xlabel('time (s)')
                                plt.ylabel('%s'%self.plotting_UOM[6])
                                plt.ylim((lowest,highest))
                        y_min,y_max=plt.gca().get_ylim()
                        # plt.axvline(self.ipd_overall_tolerances[0][0]+self.statelengths[state][barrel][iteration].start_time,color='r',linestyle='-.',label="Latest Completion")
                        # plt.axvline(self.ipd_overall_tolerances[0][1]+self.statelengths[state][barrel][iteration].start_time,color='k',linestyle='-.',label="Earliest Completion")
                        
                        # fartime=self.data[tol_equations[state][0][0]][1]+self.statelengths[state][barrel][iteration].start_time
                        # neartime=self.data[tol_equations[state][0][1]][1]+self.statelengths[state][barrel][iteration].start_time
                        
                        # far_time_tolerance=time.strftime("%M:%S",time.localtime(fartime))
                        # near_time_tolerance=time.strftime("%M:%S",time.localtime(neartime))
                        # print far_time_tolerance,near_time_tolerance,fartime,neartime
                        
                        # plt.text(self.ipd_overall_tolerances[0][0]+10+self.statelengths[state][barrel][iteration].start_time, y_min+5, r'(%s)'%(far_time_tolerance))
                        # plt.text(self.ipd_overall_tolerances[0][1]+10+self.statelengths[state][barrel][iteration].start_time, y_min+5, r'(%s)'%(near_time_tolerance))
                        
                        print np.shape(BTRx),np.shape(upper)
                        if plottols==1:
                            # print "This is what the sizes are:",self.shortest_times[state][iteration]
                            # print np.shape(self.high_tolerance_model[state][iteration][statistic]),"<--- high tolerance model"
                            # print np.shape(self.low_tolerance_model[state][iteration][statistic])
                            # print self.high_tolerance_model[state][iteration][6]
                            # print self.low_tolerance_model[state][iteration][6]
                            plt.plot(range(longest),upper,color='r',alpha=0.125,linestyle="--",label="Upper Tolerance")
                            plt.hold(True)
                            plt.plot(range(longest),lower,color='g',alpha=0.125,linestyle="--",label="Lower Tolerance")
                            plt.hold(True)
                            plt.fill_between(range(longest),upper,lower,facecolor="black",alpha=0.125,interpolate=True)
                        plt.hold(False)
                        plt.title("%s: %s (%s)"%(States[state],stats[6],self.plotting_UOM[6]))
                        plt.xlabel('time (s)')
                        plt.grid(True)
                        legend=plt.legend(bbox_to_anchor=(1,.5),loc='center left',borderaxespad=0.)
                        
                        imnum+=1
                        plt.savefig("%s_%s_%s.jpeg"%(__file__,"IPD",imnum),bbox_extra_artists=(legend,),bbox_inches='tight')
                        ipdpics.append("%s_%s_%s.jpeg"%(__file__,"IPD",imnum))
                        if shonosho==1:
                            plt.show()
                        

                        
                    

                    fig=plt.figure()
                
                    for statistic2 in range(num_statistics-1):
                        ## here we will define the y-axis limits to show the plot (which will make the plot nicer to look at when out-of-tolerance).
                        highest=-5000 # These values are set with magic numbers as a way to set the plotting y-axis
                        lowest=5000
                        for barrel in range(num_barr):
                            for iteration in range(self.stateiters[state][barrel]):
                                compare_max=max(self.stateprops[state][barrel][iteration][statistic2])
                                compare_min=min(self.stateprops[state][barrel][iteration][statistic2])
                                if compare_max>highest:
                                    highest=compare_max
                                    highest=highest*1.05
                                    if statistic2==2:
                                        highest=compare_max*1.00625

                                    
                                if compare_min<lowest:
                                    lowest=compare_min
                                    lowest=lowest*.95
                                    if statistic2==2:
                                        lowest=compare_min*.9875

                        for barrel in range(np.size(Barrels)):

                            for iteration in range(self.stateiters[state][barrel]):

                                x=[]
                                y=[]
                                lower=[]
                                upper=[]
                                BTRx= range(self.statelengths[state][barrel][iteration].length())#range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].end_time)#  <----------- used to be that. may include with another file for monitoring.
                                BTRy_hold=self.stateprops[state][barrel][iteration][statistic2]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)
                                plotarray=[]
                                

                                
                                for timer in range(self.statelengths[state][barrel][iteration].start_time,(self.statelengths[state][barrel][iteration].start_time+longest)):
                                    
                                    uppertol=(np.polyval(ipdtol[statistic2],timer))*self.hightol
                                    lowertol=(np.polyval(ipdtol[statistic2],timer))*self.lowtol
                                    
                                    upper.append(uppertol)
                                    lower.append(lowertol)                            
                                
                                
                                #plotarray.append(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration])
                                fig.add_subplot(numrows,numcols,statistic2+1)
                                times=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].end_time)
                                #print times
                                
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%M:%S",time.localtime(pos)))
                                    )
                                    
                                plt.subplots_adjust(hspace=.55)
                                plt.subplots_adjust(wspace=.55)
                                plt.locator_params(axis='x',nbins=4)
                                plt.locator_params(axis='y',nbins=6)
                                plt.xticks(rotation=45)
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1))
                                plt.title("%s (%s)"%(stats[statistic2],self.plotting_UOM[statistic2]))
                                plt.hold(True)
                                plt.xlabel('time (s)')
                                plt.ylabel('%s'%self.plotting_UOM[statistic2])
                                plt.grid(True)

                                if statistic2==2:
                                    plt.ylim((lowest,highest))
                                
                                
                        # y_min,y_max=plt.gca().get_ylim()
                        # plt.axvline(self.ipd_overall_tolerances[0][0]+self.statelengths[state][barrel][iteration].start_time,color='r',linestyle='-.',label="Latest Completion")
                        # plt.axvline(self.ipd_overall_tolerances[0][1]+self.statelengths[state][barrel][iteration].start_time,color='k',linestyle='-.',label="Earliest Completion")
                        
                        # fartime=self.data[tol_equations[state][0][0]][1]+self.statelengths[state][barrel][iteration].start_time
                        # neartime=self.data[tol_equations[state][0][1]][1]+self.statelengths[state][barrel][iteration].start_time
                        
                        # far_time_tolerance=time.strftime("%M:%S",time.localtime(fartime))
                        # near_time_tolerance=time.strftime("%M:%S",time.localtime(neartime))
                        # print far_time_tolerance,near_time_tolerance,fartime,neartime
                        
                        # plt.text(self.ipd_overall_tolerances[0][0]+10+self.statelengths[state][barrel][iteration].start_time, y_min+5, r'(%s)'%(far_time_tolerance))
                        # plt.text(self.ipd_overall_tolerances[0][1]+10+self.statelengths[state][barrel][iteration].start_time, y_min+5, r'(%s)'%(near_time_tolerance))
                        
                        
                        if plottols==1:
                            plt.plot(range(longest),upper,color='r',alpha=0.125,linestyle="--",label="Upper Tolerance")
                            plt.hold(True)
                            plt.plot(range(longest),lower,color='g',alpha=0.125,linestyle="--",label="Lower Tolerance")
                            plt.hold(True)
                            plt.fill_between(range(longest),upper,lower,facecolor="black",alpha=0.125,interpolate=True)
                       
                        
                    plt.hold(False)
                    plt.suptitle("%s"%(States[state]))
                    plt.grid(True)
                    legend=plt.legend(bbox_to_anchor=(1.05,.5),loc='center left',borderaxespad=0.)
                    imnum+=1
                    plt.savefig("%s_%s_%s.jpeg"%(__file__,"IPD",imnum),bbox_extra_artists=(legend,),bbox_inches='tight')#filename_state_barrel_statistic_image_number
                    ipdpics.append("%s_%s_%s.jpeg"%(__file__,"IPD",imnum))
                    if shonosho==1:
                        plt.show()
                    #imnum+=1   
                    
                    
                    
                    
                    
                    
                    
                    
            elif state!=0:
                imnum=0
                #long=[]
                #print numcols," columns, and ",numrows," rows."
                for statistic in range(1):#range(np.size(stats)):
                    BTRfig=plt.figure()
                    longest=0
                    ## here we will define the y-axis limits to show the plot (which will make the plot nicer to look at when out-of-tolerance).
                    highest=-5000 # These values are set with magic numbers as a way to set the plotting y-axis
                    lowest=5000
                    for barrel in range(num_barr):
                        for iteration in range(self.stateiters[state][barrel]):
                            compare_max=max(self.stateprops[state][barrel][iteration][6])
                            compare_min=min(self.stateprops[state][barrel][iteration][6])
                            if compare_max>highest:
                                highest=compare_max
                                highest=highest*1.075
                                
                            if compare_min<lowest:
                                lowest=compare_min
                                lowest=lowest*.975
                                    
                                    
                                    
                    for barrel in range(np.size(Barrels)):
                        print "Barrels: %s"%np.size(Barrels)

                        long=[]
                        longer=0
                        for iteration2 in range(self.stateiters[state][barrel]):
                            lengthtest=np.size(range(self.statelengths[state][barrel][iteration2].start_time,self.statelengths[state][barrel][iteration2].end_time))
                            
                            long.append(lengthtest)
                            #print long
                        #print long
                        if np.size(long)>0:
                            longer=max(long)
                        if longer>longest:
                            longest=longer
                        #print longest
                        
                        
                        print "%s Containing: %s"%(state,self.stateiters[state][1]),np.size(self.stateiters[state][barrel])
                        pass
                        for iteration in range(self.stateiters[state][barrel]) or range(np.size(self.stateiters[state][barrel])):
                            if self.stateiters[state][barrel]==0:
                                print "passing over. iteration yields empty."
                                pass
                            else:
                                print "Iteration: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< %s"%iteration
                                x=[]
                                y=[]
                                lower=[]
                                upper=[]
                                BTRx=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].end_time)#.length())

                                
                                
                                
                                BTRy_hold=self.stateprops[state][barrel][iteration][6]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)
                                plotarray=[]
                                #plotarray.append(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration])
                                BTRfig.add_subplot(1,2,1)
                                plt.subplot(1,2,1)
                                print np.shape(np.transpose(BTRx)),np.shape(BTRy)
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1))## once again, if there is an error, then there are not enough styles for which to plot the different iterations
                                plt.hold(True)
                                plt.grid(True)
                                print "Adding title."
                                plt.title("%s (%s), Chronologic"%(stats[6],self.plotting_UOM[6]))
                                plt.xlabel('time (h:m:s)')
                                plt.ylabel('%s'%self.plotting_UOM[6])
                                plt.xticks(rotation=45)
                                plt.ylim((lowest,highest))
                                
                                times=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].start_time+longest)
                                #print times
                                
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%H:%M:%S",time.localtime(pos)))
                                    )
                                
                                
                                
                                
                                
                                BTRx=range(self.statelengths[state][barrel][iteration].length())#.length())
                                BTRy_hold=self.stateprops[state][barrel][iteration][6]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)
                                plotarray=[]
                                #plotarray.append(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration])
                                BTRfig.add_subplot(1,2,2)
                                plt.subplots_adjust(hspace=1)
                                plt.subplot(1,2,2)
                                plt.subplots_adjust(wspace=.25)
                                for timer in range(longest):
                                    
                                    uppertol=(np.polyval(othertols[state][6],timer))*self.hightol
                                    lowertol=(np.polyval(othertols[state][6],timer))*self.lowtol
                                    
                                    upper.append(uppertol)
                                    lower.append(lowertol)                            
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1))
                                
                                
                                times=range(0,longest)
                                #print times
                                
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%M:%S",time.localtime(pos)))
                                    )
                                
                                
                                
                                
                                plt.hold(True)
                                plt.title("%s (%s), Overlay"%(stats[6],self.plotting_UOM[6]))
                                plt.xlabel('time (m:s)')
                                plt.xticks(rotation=45)
                                #plt.ylim((lowest,highest))
                    #plt.subplot(1,2,2)
                    #print range(longest),np.size(upper)
                    
                                                
                    # y_min,y_max=plt.gca().get_ylim()
                    # plt.axvline(tol_equations[state][0][0],color='r',linestyle='-.',label="Latest Completion")
                    # plt.axvline(tol_equations[state][0][1],color='k',linestyle='-.',label="Earliest Completion")
                    
                    # fartime=self.data[tol_equations[state][0][0]][1]+self.statelengths[state][barrel][iteration].start_time
                    # neartime=self.data[tol_equations[state][0][1]][1]+self.statelengths[state][barrel][iteration].start_time
                    
                    # far_time_tolerance=time.strftime("%M:%S",time.localtime(fartime))
                    # near_time_tolerance=time.strftime("%M:%S",time.localtime(neartime))
                    # print far_time_tolerance,near_time_tolerance,fartime,neartime
                    
                    # plt.text(tol_equations[state][0][0]+10, y_min+5, r'(%s)'%(far_time_tolerance))
                    # plt.text(tol_equations[state][0][1]+10, y_min+5, r'(%s)'%(near_time_tolerance))
                    
                    
                    
                    
                    if self.stateiters[state][barrel]==0:
                        pass
                    else:
                        if plottols==1:
                            plt.plot(range(longest),upper,color='r',alpha=0.125,linestyle="--",label="Upper Tolerance")
                            plt.hold(True)
                            plt.plot(range(longest),lower,color='g',alpha=0.125,linestyle="--",label="Lower Tolerance")
                            plt.hold(True)
                            plt.fill_between(range(longest),upper,lower,facecolor="black",alpha=0.125,interpolate=True)
                                                   
                                
                                
                        plt.suptitle("%s"%(States[state]))        
                        plt.hold(False)
                        plt.grid(True)
                        legend=plt.legend(bbox_to_anchor=(1,.5),loc='center left',borderaxespad=0.)
                        imnum+=1
                        plt.savefig("%s_%s_%s.jpeg"%(__file__,States[state],imnum),bbox_extra_artists=(legend,),bbox_inches='tight')
                        if state==1:
                            defpics.append("%s_%s_%s.jpeg"%(__file__,States[state],imnum))
                        if state==2:
                            refpics.append("%s_%s_%s.jpeg"%(__file__,States[state],imnum))
                        if shonosho==1:
                            plt.show()
                    
                    
                for statistic2 in range(num_statistics-1):
                    fig=plt.figure()
                    longest=0
                    for barrel in range(np.size(Barrels)):
                        ## here we will define the y-axis limits to show the plot (which will make the plot nicer to look at when out-of-tolerance).
                        highest=-5000 # These values are set with magic numbers as a way to set the plotting y-axis
                        lowest=5000
                        for brrl in range(num_barr):
                            for iter in range(self.stateiters[state][brrl]):
                                compare_max=max(self.stateprops[state][brrl][iter][statistic2])
                                compare_min=min(self.stateprops[state][brrl][iter][statistic2])
                                if compare_max>highest:
                                    highest=compare_max
                                    highest=highest*1.075
                                    if statistic2==2:
                                        highest=compare_max*1.00625

                                    
                                if compare_min<lowest:
                                    lowest=compare_min
                                    lowest=lowest*.9125
                                    if statistic2==2:
                                        lowest=compare_min*.9875

                        long=[]
                        for iteration2 in range(self.stateiters[state][barrel]):
                            lengthtest=np.size(range(self.statelengths[state][barrel][iteration2].start_time,self.statelengths[state][barrel][iteration2].end_time))
                            
                            long.append(lengthtest)
                        if np.size(long)>0:
                            long=max(long)
                        if long>longest and isinstance(long,int):
                                longest=long
                        #print longest
                        for iteration in range(self.stateiters[state][barrel]):
                            if self.stateiters[state][barrel]==0:
                                pass
                            else: 
                                x=[]
                                y=[]
                                lower=[]
                                upper=[]
                                BTRx=range(self.statelengths[state][barrel][iteration].length())
                                BTRx=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].end_time)#.length())

                                BTRy_hold=self.stateprops[state][barrel][iteration][statistic2]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)
                                plotarray=[]
                                #plotarray.append(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration])
                                fig.add_subplot(1,2,1)
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1))
                                
                                times=range(self.statelengths[state][barrel][iteration].start_time,self.statelengths[state][barrel][iteration].start_time+longest)
                                #print times
                                
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%H:%M:%S",time.localtime(pos)))
                                    )
                                
                                
                                plt.hold(True)
                                plt.grid(True)
                                plt.xlabel('time (h:m:s)')
                                plt.ylabel('%s'%self.plotting_UOM[statistic2])
                                plt.title("%s (%s), Chronologic"%(stats[statistic2],self.plotting_UOM[statistic2]))
                                plt.xticks(rotation=45)
                                plt.ylim((lowest,highest))
                                
                                BTRx=range(self.statelengths[state][barrel][iteration].length())
                                BTRy_hold=self.stateprops[state][barrel][iteration][statistic2]
                                BTRy=BTRy_hold[:]
                                zip(BTRx,BTRy)  
                                fig.add_subplot(1,2,2)
                                plt.subplots_adjust(wspace=.25)
                                print "Longest: %s"%longest
                                for timer in range(longest):
                                    
                                    uppertol=(np.polyval(othertols[state][statistic2],timer))*self.hightol
                                    lowertol=(np.polyval(othertols[state][statistic2],timer))*self.lowtol
                                    
                                    upper.append(uppertol)
                                    lower.append(lowertol)   
                                plt.plot(np.transpose(BTRx),BTRy,color=self.plotting_barrelcolor[barrel],linestyle=self.plotting_linestyles[iteration],label="BBL%s, Iter:%s"%(barrel+1,iteration+1))
                                
                                times=range(0,longest)
                                #print times
                                
                                plt.gca().xaxis.set_major_formatter(
                                    mtick.FuncFormatter(lambda pos,_: time.strftime("%M:%S",time.localtime(pos)))
                                    )
                                    
                                    
                                    
                                plt.hold(True)
                                plt.grid(True)
                                plt.title("%s (%s), Overlay"%(stats[statistic2],self.plotting_UOM[statistic2]))
                                plt.xlabel('time (m:s)')
                                plt.xticks(rotation=45)
                                if statistic2 ==2:
                                    plt.ylim((lowest,highest))
                    
                    # y_min,y_max=plt.gca().get_ylim()
                    # plt.axvline(tol_equations[state][0][0],color='r',linestyle='-.',label="Latest Completion")
                    # plt.axvline(tol_equations[state][0][1],color='k',linestyle='-.',label="Earliest Completion")
                    
                    # fartime=self.data[tol_equations[state][0][0]][1]
                    # neartime=self.data[tol_equations[state][0][1]][1]
                    
                    # far_time_tolerance=time.strftime("%M:%S",time.localtime(fartime))
                    # near_time_tolerance=time.strftime("%M:%S",time.localtime(neartime))
                    # print far_time_tolerance,near_time_tolerance,fartime,neartime
                    
                    # plt.text(tol_equations[state][0][0]+10, y_min+5, r'(%s)'%(far_time_tolerance))
                    # plt.text(tol_equations[state][0][1]+10, y_min+5, r'(%s)'%(near_time_tolerance))
                    
                    if self.stateiters[state][barrel]==0:
                        pass
                    else:
                        if plottols==1:
                            plt.subplot(1,2,2)
                            
                            plt.plot(range(longest),upper,color='r',alpha=0.125,linestyle="--",label="Upper Tolerance")
                            plt.hold(True)
                            plt.plot(range(longest),lower,color='g',alpha=0.125,linestyle="--",label="Lower Tolerance")
                            plt.hold(True)
                            plt.fill_between(range(longest),upper,lower,facecolor="black",alpha=0.125,interpolate=True)
                                                   
                                
                        plt.suptitle("%s"%(States[state]))        
                        plt.hold(False)
                        legend=plt.legend(bbox_to_anchor=(1,.5),loc='center left',borderaxespad=0.)
                        imnum+=1
                        plt.savefig("%s_%s_%s.jpeg"%(__file__,States[state],imnum),bbox_extra_artists=(legend,),bbox_inches='tight')
                        if state==1:
                            defpics.append("%s_%s_%s.jpeg"%(__file__,States[state],imnum))
                        if state==2:
                            refpics.append("%s_%s_%s.jpeg"%(__file__,States[state],imnum))
                        if shonosho==1:
                            plt.show()


        savedpics=[ipdpics,defpics,refpics]        
        return savedpics
        
    def create_pdf(self,pics,num_barr,deletepics):# ------------------------------- will be using "self" for now. next iteration will be: STATES,ERRORS,PLOTS_GEN)
        import time
        from reportlab.lib.enums import TA_JUSTIFY
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors       
        import datetime
        import calendar
        import os
        absFilePath = os.path.abspath(__file__)
        os.chdir( os.path.dirname(absFilePath) )
        import subprocess
        import signal


        from PIL import Image as immer
         
        doc = SimpleDocTemplate("%s.pdf"%(__file__),pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        Story=[]

        
        ########################################################################################################################################################################## This will be the data to be entered in the beginning of the report. NOT THE TABLES, AND NOT THE TEST STATISTICS.
        ####################################################################### REPORT INTRODUCTORY INFORMATION ##################################################################
        title="FBD QUALITY TEST REPORT" 
        formatted_time = time.ctime()
        serialno=self.data[0][0]
        testtime=self.data[-1][1]-self.data[0][1]
        m,s=divmod(testtime,60)
        h,m=divmod(m,60)
        testlength=datetime.time(h,m,s).strftime("%H:%M:%S")
        t=time.ctime()
        f=datetime.datetime.strptime(t, '%a %b %d %H:%M:%S %Y')
        
        current_time=f.strftime("%m/%d/%Y %H:%M:%S")
        series="77x"
        barr_num=num_barr
        myverdict="PASS"#<----------------------------------------------- THIS NEEDS TO BE CHANGED TO AN ACTUAL THING.

        if self.have_I_Failed==1:
            myverdict="FAIL"
        else:
            myverdict="PASS"
        if myverdict.upper()=="PASS":
            verdictcolor=colors.limegreen
        if myverdict.upper()=="FAIL":
            verdictcolor=colors.pink
        
        
        testduration="<font size=12>Test Duration (seconds): %s</font>"%(testlength)
        barrels="<font size=12>Number of Barrels: %s</font>"%(barr_num)
        seriesname="<font size=12>Series/Model: %s</font>"%(series)
        reporttime='<font size=12>Duration of Report: %s</font>'%(formatted_time)
        ttext='<font size=24>%s</font>'%(title)
        serial="<font size=14>Unit Serial No.: %s</font>"%(serialno)
        #verdictstatement="<font size=12>Verdict:</font>"
        verdict="<font size=20>---------- %s ----------</font>"%(myverdict)
        
        ####################################################################### REPORT INTRODUCTORY INFORMATION ##################################################################
        ########################################################################################################################################################################## This will be the data to be entered in the beginning of the report. NOT THE TABLES, AND NOT THE TEST STATISTICS.
         
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center',alignment=TA_CENTER))
        
###########################################################################
        overall_ipdstatnames=["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."]
        overall_refstatnames=["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."]
        overall_defstatnames=["Duration","Baseline","Max HSP","Min LSP","Min RT","Avg DC","Avg SUPR","Max Volt.","Min Volt."]
        overall_statnames=[overall_ipdstatnames,overall_defstatnames,overall_refstatnames]
        deg=u'\N{DEGREE SIGN}'
        tolerance_UOM=["MM:SS","","Psi","Psi","%sF"%deg,"%","%sF"%deg,"V","V"]
###########################################################################    
        State_names_full=["I.P.D.","Defrost","Refreeze"]
        state_names=["IPD","Def.","Ref."]
        printipd=0#---------------------------------------------------------------------------
        printref=1#---------------------------------------------------------------------------
        printdef=1#---------------------------------------------------------------------------
        tablecombine_columns_ipd=[]
        tablecombine_columns_ref=[]
        tablecombine_columns_def=[]
        tablecombine_columns_iteration=[]
        tablecombine_rows_ref=[]
        overall_tolerances=[self.ipd_overall_tolerances,self.def_overall_tolerances,self.ref_overall_tolerances]
        overall_verdicts=[self.ipd_verdicts,self.def_verdicts,self.ref_verdicts]
        overall_stateprops=[self.overall_ipdprops_value,self.overall_defprops_value,self.overall_refprops_value]
        #overall_stateprops[state][barrel].__len__()>0:
        table_grids_start=[]
        table_grids_end=[]
                ## Calculation data to be put up into the the PDF table above
###########################################################################
        state_iterations=[self.ipditeration,self.defrostiteration,self.refreezeiteration]
        state_iterrecs=[self.ipditerrec,self.defrostiterrec,self.refreezeiterrec]
        
        data= [['UNIT TESTING REPORT (%s)'%(serialno), '-', '-', '-', '-','-'],
                ['Type', '%s'%(series), 'Date', '%s'%(current_time), 'Result:','%s'%(myverdict)],
                ['Sides ', '%s'%(barr_num), 'Test Duration', '%s'%(testlength), '-','-'],
                ['-', '-', 'Tester', 'S. Martinez', '-','-'],
                ['Summary of Results', '-', '-', '-', '-','-'],
                ['', '', 'Actual', 'Low', 'High','Result']]
        
        
        
        '''
        things I will use:
        overall_stateprops[state][barrel][iteration][stat]
        overall_tolerances[state][stat][low/high]
        overall_verdicts[state][barrel][instance][stat]
        state_names[state]
        overall_statnames[state][stat]
        
        
        '''
        for state in range(np.size(state_iterations,0)):
            longest_state_iteration=[]
            for barrel in range(barr_num):
                longest_state_iteration.append([])
                longest_state_iteration[barrel]=0
                for iteration in range(np.size(self.states[state][barrel].items(),0)):
                    longest_state_iteration[barrel]+=1
                longest_iteration=max(longest_state_iteration)
        
        
        
        
        stateswap={}
        for state in range(3):
            stateswap[state]={}
            #for iteration in range(longest_iteration):
        
        
        
        
        
        for state in range(np.size(state_iterations,0)):
            print state_names[state]
            testarray=["","",""]
            data.append(['=======================   %s   =======================' %(State_names_full[state].upper()), '-', '-', '-', '-','-'])
            tablecombine_columns_ipd.append(np.size(data,0))
            longest_state_iteration=[]
            for barrel in range(barr_num):
                longest_state_iteration.append([])
                longest_state_iteration[barrel]=0
                for iteration in range(np.size(self.states[state][barrel].items(),0)):
                    longest_state_iteration[barrel]+=1
                longest_iteration=max(longest_state_iteration)
                print "LONGEST ITERATION: %s"%longest_iteration
                ###time.sleep(5)
            for iteration in range(longest_iteration):
                print "Barrel %s, State %s, Iteration: %s"%(barrel,state,iteration)
                data.append(["--------------------------------- Duration Interval: %s of %s ---------------------------------"%(iteration+1,longest_iteration),'-','-','-','-','-'])
                tablecombine_columns_ipd.append(np.size(data,0))
                #data.append(['Barrel: %s'%(barrel+1)])
                for stat in range(np.size(overall_ipdstatnames,0)):
                    if state!=0:
                        table_grids_start.append(np.size(data,0))
                    for barrel in range(num_barr):
                        if state==0:
                            if overall_stateprops[state][barrel].__len__()>0:
                                if stat==0:
                                    data.append(['%s'%(np.size(data,0)),'%s (%s)'%(overall_statnames[state][stat],tolerance_UOM[stat]),
                                    '%s'%(datetime.time(0,(divmod(overall_stateprops[state][barrel][iteration][stat],60)[0]),(divmod(overall_stateprops[state][barrel][iteration][stat],60)[1])).strftime("%M:%S")),
                                    '%s'%(datetime.time(0,int(divmod(overall_tolerances[state][stat][1],60)[0]),int(divmod(overall_tolerances[state][stat][1],60)[1])).strftime("%M:%S")),
                                    '%s'%(datetime.time(0,int(divmod(overall_tolerances[state][stat][0],60)[0]),int(divmod(overall_tolerances[state][stat][0],60)[1])).strftime("%M:%S")),
                                    '%s'%overall_verdicts[state][barrel][iteration][stat]])
                                    break
                                
                                if stat!=1 and stat!=0:
                                    data.append(['%s'%(np.size(data,0)),'%s (%s)'%(overall_statnames[state][stat],tolerance_UOM[stat]),'%.1f'%overall_stateprops[state][barrel][iteration][stat],'%s'%overall_tolerances[state][stat][1],'%s'%overall_tolerances[state][stat][0],'%s'%overall_verdicts[state][barrel][iteration][stat]])
                                    break
                                if stat==1:
                                    data.append(['%s'%(np.size(data,0)),'Barrel - %s %s (%s)'%(barrel+1,overall_statnames[state][stat],tolerance_UOM[stat]),'%s'%overall_stateprops[state][barrel][iteration][stat],'%s'%overall_tolerances[state][stat][1],'%s'%overall_tolerances[state][stat][0],'%s'%overall_verdicts[state][barrel][iteration][stat]])
                            
                            else:
                                data.append(['%s'%(np.size(data,0)),'No Record','No Record','No Record','No Record','No Record'])
                                break
                                    
                        
                        if state !=0 and state_iterations[state][barrel]>iteration:
                            
                            if overall_stateprops[state][barrel].__len__()>0:
                                
                                if stat==0:
                                    print "Barrel %s, State %s, Iteration %s, Stat: %s"%(barrel,state,iteration,stat)
                                    print state_iterations[state][barrel]
                                    print overall_stateprops[state][barrel][0][stat]
                                    data.append(['%s'%(np.size(data,0)),'Barrel - %s %s (%s)'%(barrel+1,overall_statnames[state][stat],tolerance_UOM[stat]),
                                    '%s'%(datetime.time(0,(divmod(overall_stateprops[state][barrel][iteration][stat],60)[0]),(divmod(overall_stateprops[state][barrel][iteration][stat],60)[1])).strftime("%M:%S")),
                                    '%s'%(datetime.time(0,int(divmod(overall_tolerances[state][stat][1],60)[0]),int(divmod(overall_tolerances[state][stat][1],60)[1])).strftime("%M:%S")),
                                    '%s'%(datetime.time(0,int(divmod(overall_tolerances[state][stat][0],60)[0]),int(divmod(overall_tolerances[state][stat][0],60)[1])).strftime("%M:%S")),
                                    '%s'%overall_verdicts[state][barrel][iteration][stat]])

                                else:
                                    data.append(['%s'%(np.size(data,0)),'Barrel - %s %s (%s)'%(barrel+1,overall_statnames[state][stat],tolerance_UOM[stat]),'%.1f'%overall_stateprops[state][barrel][iteration][stat],'%s'%overall_tolerances[state][stat][1],'%s'%overall_tolerances[state][stat][0],'%s'%overall_verdicts[state][barrel][iteration][stat]])
                                #table_grids_start.append(np.size(data,0))
                            else:
                                data.append(['%s'%(np.size(data,0)),'No Record','No Record','No Record','No Record','No Record'])
                                break
                    if state!=0:
                        table_grids_end.append(np.size(data,0))
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        

        t=Table(data)
        t.setStyle(TableStyle([('BACKGROUND',(-1,1),(-1,1),verdictcolor)]))
        t.setStyle(TableStyle([('ALIGN',(0,0),(0,-1),'LEFT'),
                               ('ALIGN',(0,0),(-1,0),'CENTER'),
                               #('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                               ('VALIGN',(0,0),(0,-1),'TOP'),
                               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                               #('ALIGN',(0,-1),(-1,-1),'CENTER'),
                               
                               ('SPAN',(0,0),(-1,0)),
                               ('SPAN',(0,2),(0,3)),
                               ('SPAN',(1,2),(1,3)),
                               #('SPAN',(2,1),(2,2)),
                               #('SPAN',(3,1),(3,2)),
                               ('SPAN',(4,1),(4,2)),
                               ('SPAN',(5,1),(5,2)),
                               ('SPAN',(3,3),(-1,3)),
                               ('SPAN',(0,4),(-1,4)),
                               ('SPAN',(0,5),(1,5)),
                               
                               ('ALIGN',(3,3),(3,3),'CENTER'),
                               ('ALIGN',(0,4),(-1,4),'CENTER'),
                               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                               ('VALIGN',(2,1),(3,1),'MIDDLE'),
                               ('VALIGN',(2,0),(3,0),'MIDDLE'),
                               #('VALIGN',(1,0,),(-1,-1),'MIDDLE'),
                               #('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                               ('GRID', (0,0), (-1,-1), 0.25, colors.black),#(columnstart,rowstart),(columnend,rowend),thickness
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ]))
        
        colcombine=[tablecombine_columns_ipd,tablecombine_columns_def,tablecombine_columns_ref]
        for length in range(np.size(colcombine)):
            for startstop in range(np.size(colcombine[length])):
                colcombine[length][startstop]+=-1
        colcombine=[tablecombine_columns_iteration,tablecombine_columns_ipd,tablecombine_columns_def,tablecombine_columns_ref]
        
        
        for length in range(np.size(colcombine)):
            for startstop in range(np.size(colcombine[length])):
                t.setStyle(TableStyle([('SPAN',(0,colcombine[length][startstop]),(-1,colcombine[length][startstop]))]))
                t.setStyle(TableStyle([('ALIGN',(0,colcombine[length][startstop]),(-1,colcombine[length][startstop]),'CENTER')]))
        #for length in range(np.size(tablecombine_rows_ref,0)):
            # t.setStyle(TableStyle([('SPAN',(1,tablecombine_rows_ref[length]+1),(1,tablecombine_rows_ref[length]+barr_num))]))
             #print "Spanning from: %s to %s"%(tablecombine_rows_ref[length]+1,tablecombine_rows_ref[length]+barr_num)
        for row in range(np.size(data,0)):
            if data[row][-1]=="FAIL"and row>4:
                t.setStyle(TableStyle([(('BACKGROUND',(-1,row),(-1,row),colors.red))]))
                t.setStyle(TableStyle([(('TEXTCOLOR',(2,row),(2,row),colors.red))]))
        t.setStyle(TableStyle([('VALIGN',(1,4,),(1,-1),'MIDDLE')]))
        print table_grids_start
        print "\n\n",table_grids_end
        
        
        if np.size(table_grids_start,0)>0:
            del table_grids_start[0]
        if np.size(table_grids_end,0)>0:
            del table_grids_end[-1]
        
        for length in range(np.size(table_grids_start)):
            linesize=2.5
            t.setStyle(TableStyle([('LINEBELOW', (1,table_grids_end[length]-1),(1,table_grids_end[length]-1), linesize, colors.grey)]))
            #t.setStyle(TableStyle([('LINEBELOW', (0,table_grids_end[length]-1),(-1,table_grids_end[length]-1), linesize, colors.grey)]))
        
        
        
        Story.append(t) 
        Story.append(PageBreak())
        #### THIS IS THE TABLE THAT WE WILL BE ADDING FIRST. 
        
        
        statelist=["IPD","Defrost","Refreeze"]
        Barrel_list=["BBL_1","BBL_2","BBL_3","BBL_4"]
        Statistics=["RFG_lo","RFG_hi","V","RTemp","SUPHT","DUTYCycles","BTR%"]
        Story.append(Paragraph("<font size=16>--------------- VISUALIZED TEST (LOGGED DATA) ---------------</font>",styles["Center"]))
        Story.append(Spacer(1,24))
        for state in range(np.size(pics)):
            
            amiexistent=0##--------------the check if we should add a state's section if it doesnt exist.
            
            for barrel in range(barr_num):
                if self.stateiters[state][barrel]==0:
                    amiexistent+=1
            if amiexistent>=barr_num:
                Story.append(Paragraph("<font size=12>----------- %s NONEXISTENT IN THIS TEST-----------</font>"%(statelist[state].upper()),styles["Center"]))
            else:
                Story.append(Paragraph("<font size=16>Test Visualization: %s</font>"%statelist[state],styles["Center"]))
                Story.append(Spacer(1,48))
            for picnum in range(np.size(pics[state])):
                im = Image(pics[state][picnum], 5*inch, 3*inch)
                im.hAlign='CENTER'
                Story.append(im)
                Story.append(Spacer(1,24))
                
            Story.append(PageBreak())
        
        
        ##---------------------- This will add the pictures.
        
        Story.append(Paragraph("<font size=16> ---------- NON-TABULATED ERRORS ---------- </font>",styles["Center"]))
        Story.append(Spacer(1,24))
        if np.size(self.testErrors,0)>0:
            Story.append(Paragraph("<font size=12>---------- %s ERRORS DETECTED ----------</font>"%(np.size(self.testErrors)),styles["Center"]))
            Story.append(Spacer(1,48))
            for error in range(np.size(self.testErrors,0)):
                if "missing" in self.testErrors[error].lower():
                    Story.append(Spacer(1,12))
                    Story.append(Paragraph("<font size=8>%s) - XXXXXXXX %s XXXXXXXX</font>"%(error+1,self.testErrors[error]),styles["Normal"]))
                    Story.append(Spacer(1,12))
                else:
                    Story.append(Paragraph("<font size=8>%s) -  %s </font>"%(error+1,self.testErrors[error]),styles["Normal"]))
        if np.size(self.testErrors,0)==0:
            Story.append(Paragraph("<font size=12> ---------- NO ERRORS DETECTED ---------- </font>",styles["Center"]))
        Story.append(PageBreak())
        
       
        
        Story.append(Paragraph("<font size=24>--------------- END OF REPORT ---------------</font>",styles["Center"]))
        doc.build(Story)
        
        
        
        openpage=subprocess.Popen(['%s.pdf'%(__file__)],shell=True)
        
        
        
        
        if "d" in deletepics.lower():
            print " -------------------- DELETING CACHED PICTURES --------------------"
            for state in range(np.size(pics)):
                for picnum in range(np.size(pics[state])):
                    os.remove('%s'%(pics[state][picnum]))
                    print "Picture: %s ------->>>>>>>>>>>>>>> REMOVED"%pics[state][picnum]
                    
        print "\n\n------------ PROGRAM COMPLETE. EXITING. -----------"

            ###time.sleep(10)
        

        







        
        
        
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##-------------------------------------------------------------------------------- CODE TEST INITIALIZATION  -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.           
            
s=StateAnalyzer('774_nodef_bb1.log')#('774DOUBLE.LOG')#('773TESTQUAD.log')#('773logtest2_TEST.log')#'774LABTEST.log')        
#774DOUBLE
#774labtest
#774_nodef_all
#774_nodef_noref
#774_nodef_bb1
#774_fabricated_test


num_barr=s.bar_counter() 
# print num_barr   
#num_barr=4
num_barr_to_use=num_barr #------------------------------------------------------------------------ returns an error sometimes if the barrels used in anlysis dont match with barrels actually working.
s.StatePopulator(num_barr_to_use)#_to_use)


s.analysis_of_states(num_barr_to_use)
s.statecleaner(num_barr_to_use)
# state hierarchy: IPD: number of iterations --> [ .start_time, .end_time]  --------------------------------------------------->>>>>> object.ipd[iteration number].start_time or object.ipd[barrel].end_time
                 # Refreeze and Defrost: barrel -->number of iterations --> [ .start_time, .end_time]-------------------------->>>>>> object.refreeze/defrost[barrel][iteration number].start_time or .end_time


s.getdata(num_barr_to_use)
#print s.ipd_BTR[0][0]
#print s.ipd[0].length()
#print s.ref_BTR[0][1]
s.initialize_Tolerances()
s.analyze_tolerances(num_barr_to_use)
pics=s.display_plots_version2(num_barr_to_use,1,0)
s.create_pdf(pics,num_barr_to_use,"del")
# property legend:  obect.ipdprops/refprops/defprops[barrel][instance][KEY TO PROPERTY:  0=RFGLOW  1=RFGHIGH 2=V  3=RTemp  4=SUPRHT  5=DUTYCycles  6=BTR]
#print s.ipdprops[0][0][0]




#s.statecleaner(num_barr_to_use)


# print "\n\n\n"
# print s.ipdprops[0][0][6][0]
# print np.size(s.refprops[0].items(),0)
# print s.refprops[0][0][0]
# print dir(s.refprops[0][0])
# print s.refprops[0][0].__len__()
#print np.size(s.refprops[0][0].items(),0)
##-------------------------------------------------------------------------------- CODE TEST INITIALIZATION  -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.              















































     
        
    # def display_plots(self,num_barr,state):
        # '''
        # # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # '''
        # import matplotlib.pyplot as plt
        # import matplotlib.dates as mdates
        # import matplotlib.ticker as ticker
        # import matplotlib
        # from matplotlib.backends.backend_pdf import PdfPages
        # from datetime import datetime as dt
        # from datetime import timedelta
        # '''
        # # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # '''
        
        
        
        
        
        
        
        
        
        
        # Barrels=["BBL_1","BBL_2","BBL_3","BBL_4"]
        # States=["IPD","Defrost","Refreeze"]
        # stats=["RFGLow","RFGHigh", "V", "RTemp", "SUPRHT", "DTYCycles", "BTR%"]
        
        # print "\n          ","---"*10,"< Initializing Plots >","---"*10
        
        # print "State: ",state.upper()
        # state=state.lower()
        # if state=="ipd":
            # num_statistics=np.size(stats)            
            # #----------------------------------------------------------- Counting the number of times IPD is entered:
            # print "\n Number of IPD states: ",(self.ipditeration)
            # #----------------------------------------------------------- Counting the number of statistics that exist:
            # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            # numcols=(num_statistics-1)/2
            # numrows=(num_statistics-1)/3
            # print numcols," columns, and ",numrows," rows."
            # for L in range(num_barr):
             # for K in range(self.ipditeration):
             
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # BTRx=range(self.ipd[K].length())
                # #BTRy_hold=np.delete(self.ipdprops[L][K][6],0,axis=1)
                # BTRy_hold=self.ipdprops[l][k][6]
                # BTRy=BTRy_hold[:]
                # zip(BTRx,BTRy)
                # BTRfig=plt.figure()
                # #plots=zip(BTRx,BTRy)
                # plt.plot(np.transpose(BTRx),BTRy,'b')
                # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[0],stats[6],K))
                # plt.show()                
                
               
                
                # fig=plt.figure()
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # for J in range(num_statistics-1):
                    # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[J],K)]
                    # print title
                    # #x_hold=np.delete(self.ipdprops[L][K][J],1,axis=1)
                    # x_hold=range(self.ipd[K].length())
                    # #x=np.array([],dtype=object)
                    # #x=np.append(x,x_hold[:])
                    # x.append(x_hold[:])
                    # #print x
                   # # y_hold=np.delete(self.ipdprops[L][K][J],0,axis=1)
                    # y_hold=(self.ipdprops[L][K][J])
                    # #y=np.array([],dtype=object)
                    # y.append(y_hold[:])
                    # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[0],K)])
                # plots=zip(x,y)
                # axs={}
                # for idx,plot in enumerate(plots):
                    # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    # axs[idx].plot(plot[0],plot[1],'b')
                    # plt.title(["%s" % (stats[idx])])
                # print np.shape(x)
                # plt.show()

        # elif state=="refreeze":
            # num_statistics=np.size(stats)            
            # #----------------------------------------------------------- Counting the number of times IPD is entered:
            # print "\n Number of IPD states: ",(self.refreezeiteration)
            # #----------------------------------------------------------- Counting the number of statistics that exist:
            # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            # numcols=(num_statistics-1)/2
            # numrows=(num_statistics-1)/3
            # print numcols," columns, and ",numrows," rows."
            # for L in range(num_barr):
             # for K in range(self.refreezeiteration[L]):
             
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # BTRx=range(self.refreeze[L][K].length())
                # #BTRy_hold=np.delete(self.refprops[L][K][6],0,axis=1)
                # BTRy_hold=self.refprops[L][K][6]
                # BTRy=BTRy_hold[:]
                # zip(BTRx,BTRy)
                # BTRfig=plt.figure()
                # #plots=zip(BTRx,BTRy)
                # plt.plot(np.transpose(BTRx),BTRy,'c')
                # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[2],stats[6],K))
                # plt.show()                
                
               
                
                # fig=plt.figure()
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # for J in range(num_statistics-1):
                    # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[J],K)]
                    # print title
                    # #x_hold=np.delete(self.refprops[L][K][J],1,axis=1)
                    # x_hold=range(self.refreeze[L][K].length())
                    # #x=np.array([],dtype=object)
                    # #x=np.append(x,x_hold[:])
                    # x.append(x_hold[:])
                    # #print x
                    # #y_hold=np.delete(self.refprops[L][K][J],0,axis=1)
                    # #y=np.array([],dtype=object)
                    # y_hold=self.refprops[L][K][J]
                    # y.append(y_hold[:])
                    # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[1],K)])
                # plots=zip(x,y)
                # axs={}
                # for idx,plot in enumerate(plots):
                    # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    # axs[idx].plot(plot[0],plot[1],'c')
                    # plt.title(["%s" % (stats[idx])])
                # print np.shape(x)
                # plt.show()

        # elif state=="defrost":
            # num_statistics=np.size(stats)            
            # #----------------------------------------------------------- Counting the number of times IPD is entered:
            # print "\n Number of IPD states: ",(self.defrostiteration)
            # #----------------------------------------------------------- Counting the number of statistics that exist:
            # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            # numcols=(num_statistics-1)/2
            # numrows=(num_statistics-1)/3
            # print numcols," columns, and ",numrows," rows."
            # for L in range(num_barr):
             # for K in range(self.defrostiteration[L]):
             
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # BTRx=range(self.defrost[L][K].length())
                # #BTRy_hold=np.delete(self.defprops[L][K][6],0,axis=1)
                # BTRy_hold=self.defprops[L][K][6]
                # BTRy=BTRy_hold[:]
                # zip(BTRx,BTRy)
                # BTRfig=plt.figure()
                # #plots=zip(BTRx,BTRy)
                # plt.plot(np.transpose(BTRx),BTRy,'m')
                # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[1],stats[6],K))
                # plt.show()                
                
               
                
                # fig=plt.figure()
                # x=np.array([],dtype=object)
                # y=np.array([],dtype=object)
                # x=[]
                # y=[]
                # for J in range(num_statistics-1):
                    # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[J],K)]
                    # print title
                    # #x_hold=np.delete(self.defprops[L][K][J],1,axis=1)
                    # x_hold=range(self.defrost[L][K].length())
                    # #x=np.array([],dtype=object)
                    # #x=np.append(x,x_hold[:])
                    # x.append(x_hold[:])
                    # #print x
                    # #y_hold=np.delete(self.defprops[L][K][J],0,axis=1)
                    # #y=np.array([],dtype=object)
                    # y_hold=self.defprops[L][K][J]
                    # y.append(y_hold[:])
                    # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[1],K)])
                # plots=zip(x,y)
                # axs={}
                # for idx,plot in enumerate(plots):
                    # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    # axs[idx].plot(plot[0],plot[1],'m')
                    # plt.title(["%s" % (stats[idx])])
                # print np.shape(x)
                # plt.show()
                
        # else:
            
                # num_statistics=np.size(stats)            
                # #----------------------------------------------------------- Counting the number of times IPD is entered:
                # print "\n Number of IPD states: ",(self.ipditeration)
                # #----------------------------------------------------------- Counting the number of statistics that exist:
                # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                # numcols=(num_statistics-1)/2
                # numrows=(num_statistics-1)/3
                # print numcols," columns, and ",numrows," rows."
                # for L in range(num_barr):
                 # for K in range(self.ipditeration):
                 
                    # BTRx=range(self.ipd[K].length())
                    # #BTRy_hold=np.delete(self.ipdprops[L][K][6],0,axis=1)
                    # BTRy_hold=self.ipdprops[L][K][6]
                    # BTRy=BTRy_hold[:]
                    # zip(BTRx,BTRy)
                    # BTRfig=plt.figure()
                    # #plots=zip(BTRx,BTRy)
                    # plt.plot(np.transpose(BTRx),BTRy,'b')
                    # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[0],stats[6],K))
                    # plt.show()                
                    
                   
                    
                    # fig=plt.figure()
                    # x=np.array([],dtype=object)
                    # y=np.array([],dtype=object)
                    # x=[]
                    # y=[]
                    # for J in range(num_statistics-1):
                        # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[J],K)]
                        # print title
                        # #x_hold=np.delete(self.ipdprops[L][K][J],1,axis=1)
                        # x_hold=range(self.ipd[K].length())
                        # #x=np.array([],dtype=object)
                        # #x=np.append(x,x_hold[:])
                        # x.append(x_hold[:])
                        # #print x
                        # #y_hold=np.delete(self.ipdprops[L][K][J],0,axis=1)
                        # #y=np.array([],dtype=object)
                        # y_hold=self.ipdprops[L][K][J]
                        # y.append(y_hold[:])
                        # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[0],K)])
                    # plots=zip(x,y)
                    # axs={}
                    # for idx,plot in enumerate(plots):
                        # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        # axs[idx].plot(plot[0],plot[1],'b')
                        # plt.title(["%s" % (stats[idx])])
                    # print np.shape(x)
                    # plt.show()
                
                
                
                
                
                # num_statistics=np.size(stats)            
                # #----------------------------------------------------------- Counting the number of times IPD is entered:
                # print "\n Number of IPD states: ",(self.refreezeiteration)
                # #----------------------------------------------------------- Counting the number of statistics that exist:
                # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                # numcols=(num_statistics-1)/2
                # numrows=(num_statistics-1)/3
                # print numcols," columns, and ",numrows," rows."
                # for L in range(num_barr):
                 # for K in range(self.refreezeiteration[L]):
                 
                    # x=np.array([],dtype=object)
                    # y=np.array([],dtype=object)
                    # x=[]
                    # y=[]
                    # BTRx=range(self.refreeze[L][K].length())
                    # #BTRy_hold=np.delete(self.refprops[L][K][6],0,axis=1)
                    # BTRy_hold=self.refprops[L][K][6]
                    # BTRy=BTRy_hold[:]
                    # zip(BTRx,BTRy)
                    # BTRfig=plt.figure()
                    # #plots=zip(BTRx,BTRy)
                    # plt.plot(np.transpose(BTRx),BTRy,'c')
                    # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[2],stats[6],K))
                    # plt.show()                
                    
                   
                    
                    # fig=plt.figure()
                    # x=np.array([],dtype=object)
                    # y=np.array([],dtype=object)
                    # x=[]
                    # y=[]
                    # for J in range(num_statistics-1):
                        # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[J],K)]
                        # print title
                        # #x_hold=np.delete(self.refprops[L][K][J],1,axis=1)
                        # x_hold=range(self.refreeze[L][K].length())
                        # #x=np.array([],dtype=object)
                        # #x=np.append(x,x_hold[:])
                        # x.append(x_hold[:])
                        # #print x
                        # #y_hold=np.delete(self.refprops[L][K][J],0,axis=1)
                        # #y=np.array([],dtype=object)
                        # y_hold=self.refprops[L][K][J]
                        # y.append(y_hold[:])
                        # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[2],K)])
                    # plots=zip(x,y)
                    # axs={}
                    # for idx,plot in enumerate(plots):
                        # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        # axs[idx].plot(plot[0],plot[1],'c')
                        # plt.title(["%s" % (stats[idx])])
                    # print np.shape(x)
                    # plt.show()

            
                # num_statistics=np.size(stats)            
                # #----------------------------------------------------------- Counting the number of times IPD is entered:
                # print "\n Number of IPD states: ",(self.defrostiteration)
                # #----------------------------------------------------------- Counting the number of statistics that exist:
                # print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                # print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                # numcols=(num_statistics-1)/2
                # numrows=(num_statistics-1)/3
                # print numcols," columns, and ",numrows," rows."
                # for L in range(num_barr):
                 # for K in range(self.defrostiteration[L]):
                 
                    # x=np.array([],dtype=object)
                    # y=np.array([],dtype=object)
                    # x=[]
                    # y=[]
                    # BTRx=range(self.defrost[L][K].length())
                    # #BTRy_hold=np.delete(self.defprops[L][K][6],0,axis=1)
                    # BTRy_hold=self.defprops[L][K][6]
                    # BTRy=BTRy_hold[:]
                    # zip(BTRx,BTRy)
                    # BTRfig=plt.figure()
                    # #plots=zip(BTRx,BTRy)
                    # plt.plot(np.transpose(BTRx),BTRy,'m')
                    # plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[1],stats[6],K))
                    # plt.show()                
                    
                   
                    
                    # fig=plt.figure()
                    # x=np.array([],dtype=object)
                    # y=np.array([],dtype=object)
                    # x=[]
                    # y=[]
                    # for J in range(num_statistics-1):
                        # title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[J],K)]
                        # print title
                        # #x_hold=np.delete(self.defprops[L][K][J],1,axis=1)
                        # x_hold=range(self.defrost[L][K].length())
                        # #x=np.array([],dtype=object)
                        # #x=np.append(x,x_hold[:])
                        # x.append(x_hold[:])
                        # #print x
                        # #y_hold=np.delete(self.defprops[L][K][J],0,axis=1)
                        # #y=np.array([],dtype=object)
                        # y_hold=self.defprops[L][K][J]
                        # y.append(y_hold[:])
                        # plt.suptitle(["%s: %s Iteration: %d"%(Barrels[L],States[1],K)])
                    # plots=zip(x,y)
                    # axs={}
                    # for idx,plot in enumerate(plots):
                        # axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        # axs[idx].plot(plot[0],plot[1],'m')
                        # plt.title(["%s" % (stats[idx])])
                    # print np.shape(x)
                    # plt.show()

                    
    




















































##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##-------------------------------------------------------------------------------- CODE TEST DEBUG  -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.           
 
#print s.refreeze[0].items(), np.size(s.refreeze[0].items(),0)

#print s.refreeze[0][0].start_time
#print np.size(s.ipd.items())
#print np.size(s.refreeze.items())
#print np.size(s.refreeze[0].items())

# print s.refreeze[0][1].start_time
# print np.size(s.refreeze[0].items())
# print dir(s.refreeze[0])
# print s.refreeze[0].viewitems()
# print np.size(s.refreeze[0].items(),0)
#s.thecleaners(num_barr_to_use)
# print np.shape(s)
# print (s.state_data[1019:1079])

#s.ipd[0].start_time
#print s.ipd[0].start_time

##-------------------------------------------------------------------------------- CODE TEST DEBUG -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.              
           
'''---------------------------------------------------------------------------------------------------------- TIMERECORDING PER BARRELS WORKING. DO NOT TOUCH .-------------------------------------------------------------------------------------- this works, duplicating for a beta. 
    
    def analysis_of_states(self,num_barr):
        import time
        import numpy as np        
        print ["TIME", "BBL1 - FRZ", "BBL1DEF", "BBL2FRZ", "BBL2DEF","BBL1 row specific state",
        "BBL2 row specific state", "BBL1 Data Analysis State", "BBL2 Data Analysis State"]
        # timecap={}
        # for i in range(num_barr):#--------------------------------------------------------------------------- there are n amount of barrels to keep track of, per the input parameter.
            # timecap[i]={}
            # for j in range(3):#------------------------------------------------------------------------------ there are 3 states to keep track of
                # timecap[i][j]=["Start","Finish"]

        #print timecap
        #return

        ###time.sleep(10)
        #print Data[0][0],##time.sleep(5)
        statingrun={}
        endtimerec={}
        for i in range(num_barr):
            statingrun[i]={}
            endtimerec[i]=0
            statingrun[i] =State(i,None,None,None)
        data_analysis_states=self.get_dataset(num_barr)
               
        for row in self.state_data:
            row_state = self.analysis_state(row,num_barr)
                
            for barrel, barrel_state in enumerate(row_state):
                if "IPD" in row_state and endtimerec[barrel]==0:# row_state[barrel]=="IPD" and endtimerec[barrel]<1 :#------------------------------------------------------------------------------------------------------------------------------------- When it enters IPD state.
                        
                        statingrun[barrel].start_time=row[0]
                        statingrun[barrel].barrel=barrel
                        statingrun[barrel].state_name=row_state[barrel]

                if not "IPD" in data_analysis_states and endtimerec[barrel]==1 :
                    statingrun[barrel].end_time=row[0]
                    endtimerec[barrel]=10
                    
                    
                    
                    
                    
                    
                    
                if data_analysis_states[barrel] != barrel_state:
                    #if barrel_state != "Other":
                    #if endtimerec[barrel]==1:
                        #statingrun[barrel].end_time=row[0]                    
                    print "State transition"
                
                    #timecap[barrel][barrel_state]=[Data[0][0]]
                # Let's say that we're transitioning from an IPD state to another state
                # Per our definition the IPD continues until all barrels have existed
                # the freeze state - so we need to only change the barrel state when
                # all of the barrels are no longer in IPD
                if data_analysis_states[barrel] == "IPD":
                    # statingrun[barrel].start_time=row[0]

                    # statingrun[barrel].barrel=barrel
                    # statingrun[barrel].state_name=data_analysis_states[barrel]
                    # endtimerec[barrel]=1
                    
                    # any other barrels still freezing?
                    if "Freezing" in row_state:
                        
                        pass # Don't modify the currently stored analysis state
                    else:
                        # At this point all barrels will have existed the IPD state
                        data_analysis_states[barrel] = barrel_state
                    
                else:
                    data_analysis_states[barrel] = barrel_state
                    
                    
                    
                if "IPD" in row_state and endtimerec[barrel]==0:#----------------------------------------------------- CRITICAL IPD HARDCODE. DO NOT TOUCH. DO NOT MOVE. ---------------------------------------------------------- this must be here in order for the IPD recording to start.
                    endtimerec[barrel]=1
                    
            print row , row_state ,data_analysis_states
        for x in range(num_barr):
            print "Barrel: ",statingrun[x].barrel," Start Duration: ",statingrun[x].start_time," End Duration: ",statingrun[x].end_time," State: ",statingrun[x].state_name
            print endtimerec
''''''------------------------------------------------------------------------------------------------------- TIMERECORDING PER BARRELS WORKING. DO NOT TOUCH .-------------------------------------------------------------------------------------- this works, duplicating for a beta.             
'''            
            
            
            
            
            
            
            
            
            
'''------------------------------------------------------------------------------------------------------- WORKING. DO NOT TOUCH .-------------------------------------------------------------------------------------- this works, duplicating for a beta.   
    def get_dataset(self,num_barr):
    
        self.data_analysis_states = [ "Other", "Other","Other","Other" ]
        self.data_analysis_states=self.data_analysis_states[0:num_barr]
        return self.data_analysis_states
    
    def analysis_of_states(self,Data,num_barr):
        import time    
        print ["TIME", "BBL1 - FRZ", "BBL1DEF", "BBL2FRZ", "BBL2DEF","BBL1 row specific state",
        "BBL2 row specific state", "BBL1 Data Analysis State", "BBL2 Data Analysis State"]
        data_analysis_states=self.get_dataset(num_barr)        
        for row in Data:
            row_state = self.analysis_state(row,num_barr)
         
            for barrel, barrel_state in enumerate(row_state):
                if data_analysis_states[barrel] != barrel_state:
                    print "State transition"  
                    
                # Let's say that we're transitioning from an IPD state to another state
                # Per our definition the IPD continues until all barrels have existed
                # the freeze state - so we need to only change the barrel state when
                # all of the barrels are no longer in IPD
                if data_analysis_states[barrel] == "IPD":
                    # any other barrels still freezing?
                    if "Freezing" in row_state:
                        pass # Don't modify the currently stored analysis state
                    else:
                        # At this point all barrels will have existed the IPD state
                        data_analysis_states[barrel] = barrel_state
                else:
                    data_analysis_states[barrel] = barrel_state
         
            print row , row_state ,data_analysis_states
''''''------------------------------------------------------------------------------------------------------- WORKING. DO NOT TOUCH .-------------------------------------------------------------------------------------- this works, duplicating for a beta.  
'''    

#print Data


        # #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- vvvvvvvvvvvv Sizing the arrays to correctly represent input data
        # FRZ_Columns=np.array([None,None,None,None],dtype=object)
        # THAW_Columns=np.array([None,None,None,None],dtype=object)
        # SMRT_STATE=np.array([None,None,None,None],dtype=object)
        # ENG_STATE=np.array([None,None,None,None],dtype=object)
        # SMRT_STATE_CHECK=np.array([None,None,None,None],dtype=object)#<---------------------------------------------------------------------------------------------------------------------------------------- stanford, you can use this to check the state times. but in order to record situations in which the barrels dont enter a state an equal amount of times, you may need to make a dict, with keys referring to each state instead.
        # FRZ_Columns_last=np.array([None,None,None,None],dtype=object)
        # THAW_Columns_last=np.array([None,None,None,None],dtype=object)
        
        
        
        # BBL1={777:np.array([],dtype=object),8:np.array([],dtype=object),11:np.array([],dtype=object)}
        # BBL2={777:np.array([],dtype=object),8:np.array([],dtype=object),11:np.array([],dtype=object)}
        # BBL3={777:np.array([],dtype=object),8:np.array([],dtype=object),11:np.array([],dtype=object)}
        # BBL4={777:np.array([],dtype=object),8:np.array([],dtype=object),11:np.array([],dtype=object)}
        # STATE_TIMES=np.array([BBL1,BBL2,BBL3,BBL4],dtype=object)#----------------------------------------------------------------------------------------------------------------------------------------------- this will look like STATE_TIMES[barrel1]([IPDTIMES1-->however many times it IPD's][START,END])([REFTIMES1-->however many times it REF's][START,END])([DEFTIMES1-->however many times it DEF's][START,END]), STATE_TIMES[barrel2]([IPDTIMES1-->however many times it IPD's][START,END])([REFTIMES1-->however many times it REF's][START,END])([DEFTIMES1-->however many times it DEF's][START,END])
        
        # FRZ_Columns=FRZ_Columns[0:self.number_of_barrels]
        # THAW_Columns=THAW_Columns[0:self.number_of_barrels]
        # SMRT_STATE=SMRT_STATE[0:self.number_of_barrels]#-------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to combine the freeze and defrost into a single array instead of two seperate ones.
        # ENG_STATE=ENG_STATE[0:self.number_of_barrels]#---------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to combine the freeze and defrost into a single array instead of two seperate ones.
        # SMRT_STATE_CHECK=SMRT_STATE_CHECK[0:self.number_of_barrels]
        # STATE_TIMES=STATE_TIMES[0:self.number_of_barrels]
        # FRZ_Columns_last=FRZ_Columns_last[0:self.number_of_barrels]
        # THAW_Columns_last=THAW_Columns_last[0:self.number_of_barrels]
        # #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ^^^^^^^^^^^^ Sizing the arrays to correctly represent input data
        
        
        # #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- vvvvvvvvvvvv "Simplifying" states
        # SIMPLE_STATES={0:0,4:0,3:0,5:0,9:0,7:0,10:0,8:3,11:2,777:1}#-------------------------------------------------------------------------------------------------------------------------------------------- Meaning: actual state 8: freezedown (3), actual state 11: defrost (2), SPECIAL STATE(777): IPD (1), all other states (0,4,3,5,7,9,10): Ignore (0) 
        # INENGLISH_STATES={0:"IDLE",4:"IDLE",3:"IDLE",5:"IDLE",9:"IDLE",7:"IDLE",10:"IDLE",8:"FRZDWN",11:"DEFRST",777:"IPD"}
        # #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ^^^^^^^^^^^^ "Simplifying" states
        
        
        # for i in range(np.size(self.time,0)):
            # for barrel in range(self.number_of_barrels):
                # #print barrel
                # #print COLUMN(self.data,10+5+7*barrel)
                # last=0
                # if i!=0:
                    # last=i-1
                    # FRZ_Columns_last[barrel]=SIMPLE_STATES[COLUMN(self.data,10+5+7*barrel)[last]]
                    # THAW_Columns_last[barrel]=SIMPLE_STATES[COLUMN(self.data,10+6+7*barrel)[last]]
                # FRZ_Columns[barrel]=SIMPLE_STATES[COLUMN(self.data,10+5+7*barrel)[i]]#COLUMN(self.data,10+5+7*barrel)[i]#np.append(FRZ_Columns[barrel],COLUMN(self.data,10+5+7*barrel))
                # THAW_Columns[barrel]=SIMPLE_STATES[COLUMN(self.data,10+6+7*barrel)[i]]#COLUMN(self.data,10+6+7*barrel)[i]#np.append(THAW_Columns[barrel],COLUMN(self.data,10+6+7*barrel))
                # #-------------------------------------------------------------------------------SUCCESS--------------------------------------------------------------------------------------------------------- this is supposed to be a test implementation of the smartstate array
                # if FRZ_Columns[barrel] !=0:
                    # SMRT_STATE[barrel]=FRZ_Columns[barrel]
                    # if i!=0:
                        # SMRT_STATE_CHECK[barrel]=np.array([FRZ_Columns_last,FRZ_Columns],dtype=object)
                    # ENG_STATE[barrel]=INENGLISH_STATES[COLUMN(self.data,10+5+7*barrel)[i]]
                # if FRZ_Columns[barrel] ==0:
                    # SMRT_STATE[barrel]=THAW_Columns[barrel]
                    # if i!=0:
                        # SMRT_STATE_CHECK[barrel]=np.array([THAW_Columns_last,THAW_Columns],dtype=object)
                    # ENG_STATE[barrel]=INENGLISH_STATES[COLUMN(self.data,10+6+7*barrel)[i]]
                # #-------------------------------------------------------------------------------SUCCESS--------------------------------------------------------------------------------------------------------- this is supposed to be a test implementation of the smartstate array

                
                # #-------------------------------------------------------------------------------SUCCESS--------------------------------------------------------------------------------------------------------- ATTEMPT TO CREATE IPD IDENTIFICATION
                # if SMRT_STATE.all()==3:
                    # SMRT_STATE[:]=SIMPLE_STATES[777]
                    # ENG_STATE[:]=INENGLISH_STATES[777]
                # #-------------------------------------------------------------------------------SUCCESS--------------------------------------------------------------------------------------------------------- ATTEMPT TO CREATE IPD IDENTIFICATION
                # '''#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ATTEMPT TO RECORD TIMES
                # '''

            # #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this will look at the state before it, to ensure that we dont look at an index before 0.
                # # last=i-1
                # # current=i
                # # if FRZ_Columns[barrel]!=0:
                    # # SMRT_STATE_CHECK[barrel]=np.array([SIMPLE_STATES[COLUMN(self.data,10+5+7*barrel)[last]],SIMPLE_STATES[COLUMN(self.data,10+5+7*barrel)[current]]],dtype=object)
                # # if FRZ_Columns[barrel]==0:
                    # # SMRT_STATE_CHECK[barrel]=np.array([SIMPLE_STATES[COLUMN(self.data,10+6+7*barrel)[last]],SIMPLE_STATES[COLUMN(self.data,10+6+7*barrel)[current]]],dtype=object)
                
                # if i!=0 and np.equal(SMRT_STATE_CHECK.any(barrel),None)==False:   
                    # check1=SMRT_STATE_CHECK[barrel][0]
                    # check2=SMRT_STATE_CHECK[barrel][1]
                    # print check1,check2,"-"*10
                    # if check1!=check2:#---------------------------------------------------------------------------------------------------------------------------------------------- meaning "if the last state is not the same as the new one"
                        # print "Barrel: ",barrel," Previous State: ",SMRT_STATE_CHECK[barrel][0]," New State: ",SMRT_STATE_CHECK[barrel][1]
                    
                # '''#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ATTEMPT TO RECORD TIMES
                # '''          
            
            # print "Freeze Array: ",FRZ_Columns," Defrost Array : ",THAW_Columns," \"Smart\" Array: ",SMRT_STATE," Action Array: ",ENG_STATE
       
        # FRZ_Columns=np.transpose(FRZ_Columns)
        # THAW_Columns=np.transpose(THAW_Columns)
        # state_columns=(["Actual States: ",FRZ_Columns, THAW_Columns,"Processed States: ", ])#--------------------------------------------------------------------------------------------------------------------- this gets all the number of barrels and puts them together format:[bbl1,bbl2,bbl3,bbl4],[simplebbl1,simplebbl2,simpebbl3,simplebbl4].
        
        # '''#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 18:34
        # IPD=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be IPD[barrel1][freezedown1,2,3,4], IPD[barrel2][freezedown1,2,3,4],etc.
        # DEF=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be DEF[barrel1][Defrost1,2,3,4], DEF[barrel2][Defrost1,2,3,4],etc.
        # REF=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be REF[barrel1][Refreeze1,2,3,4], REF[barrel2][Refreeze1,2,3,4],etc.
        
        # for barrel_number in range(self.number_of_barrels):#-------------------------------------------------------------- this will go through the data recorded and get the phase stuff.
            # DEF=np.append(DEF,[None])
            # REF=np.append(REF,[None])
            
            # for i in range(np.size(FRZ_Columns[barrel_number],0)):
            
                # if FRZ_Columns[barrel_number][i-1]!=8 or FRZ_Columns[barrel_number][i+1]!=8:#----------------------------- this will basically run through the data and ONLY record the beginnings and ends of each freezedown.
                    # REF[barrel_number]=np.append(REF[barrel_number],[self.time[i],self.time_easy[i]])
                    
                # if THAW_Columns[barrel_number][i-1]!=11 or THAW_Columns[barrel_number][i+1]!=11:
                    # DEF[barrel_number]=np.append(DEF[barrel_number],[self.time[i],self.time_easy[i]])
        
        # #for barrel_number in range(self.number_of_barrels):
        # for i in range(np.size(REF[barrel_number],0)):#--------------------------------------------------------------------- HERE will be the IPD finder.
            # if REF[:][i-1] or REF[:][i+1]!=4:#----------------------------------------------------------------------------- how this is supposed to work: if all barrels have the 4, record as an IPD.
                # IPD=np.append(IPD,i)
        # phase_data=[IPD,DEF,REF]
        

        # return phase_data
        # ''''''#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 18:34
        # '''    

                
        # '''
        # return state_columns#------------------------------------------------------------------------------------------------------------------------------------ this will return as: [State:1->2][Barrel:1->4][time:START->END]    * OLD ITERATION. 19 July 2016 16:49
        # '''
        
        
       
        
# s=StateAnalyzer('773logtest2_TEST_double.log')        
# num_barr=s.bar_counter()#------------------------------------------------------------------------------------------------------------------------------------------ this function works to count the number of barrels.     
# print num_barr   
# #print s.data
# #print np.shape(s.data)      
'''#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 16:49  
Data=s.StateIdentifier()
print Data
print np.shape(Data[0][1])
print Data[0][1][1:2000]
''''''#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 16:49
'''
# Data=s.StatePopulator(num_barr)

# print Data
# #analysis=Data.analysis_state(num_barr)
# #print States       
        
        
        
        
        # self.states = []
		# analyze()
	
	# def analyze(self):
		# [... detect states ...]
		
		# s = State.initialize()
		# s.barrel_number = 3
		# s.state_name    = "IPD"
		# ...

		# for each state detected:
			# self.states.append( s )
		
	# def get_state(barrel, state_name):
		# #perform search here for State objects which match the above requirements
	
	# def get_error_states(self):
		# error_states = []
		# for state in self.states:
			# if !state.pass():
				# error_states.append ( state)
	
		# return error_states
        
        
# so this would be called: testrun=StateAnalyzer("TestRun",logfile.log)




# This is example test data for two barrels.
#Column 0 is the time, Column 1 is the freeze state, column 2 is the defrost state
#Columns 3 is BBL2 frz, Column 4 is BBL2 defrost
'''
data = [
[1,0,0,0,0],
[2,0,0,0,0],
[3,0,0,8,0],
[4,8,0,8,0],
[5,8,0,8,0],
[6,8,0,8,0],
[8,8,0,0,0],
[9,8,0,0,0],
[10,0,8,0,0],
[11,0,8,0,0],
[12,0,8,0,0],
[13,0,11,0,0],
[14,0,11,0,0]]


data = [
[1,0,0,0,0,8,0,0,0],
[2,0,0,0,0,8,0,0,0],
[3,0,0,8,0,8,0,0,0],
[4,8,0,8,0,8,0,0,0],
[5,8,0,8,0,8,0,8,0],
[6,8,0,8,0,8,0,8,0],
[8,8,0,0,0,0,11,8,0],
[9,8,0,0,0,0,12,8,0],
[10,0,8,0,0,0,4,8,0],
[11,0,8,0,0,0,9,8,0],
[12,0,8,0,0,0,0,8,0],
[13,0,11,0,0,0,0,0,11],
[14,0,11,0,0,0,0,0,11]]
 
def analysis_state(row):
    IPDtrack=["IPD","IPD","IPD","IPD"]
    rowtrack=[row[1],row[3],row[5],row[7]]
    rowtrack=rowtrack[0:num_barr]
    IPDtrack=IPDtrack[0:num_barr]
    print rowtrack

    if np.all(np.equal(rowtrack,8)):#, row[3] == 8,row[5]==8,row[7]==8]):
        return IPDtrack
       
    barrel_cols = [ (1,2),(3,4),(5,6),(7,8)]
    barrel_cols=barrel_cols[0:num_barr]
    output = []
    for frz_col, def_col in barrel_cols:
        if row[frz_col] == 8:
            output.append("Freezing")
        elif row[def_col] == 11:
            output.append("Defrosting")
        else:
            output.append("Other")
    
    return output
       
data_analysis_states = [ "Other", "Other","Other","Other" ]
data_analysis_states=data_analysis_states[0:num_barr] 
print ["TIME", "BBL1 - FRZ", "BBL1DEF", "BBL2FRZ", "BBL2DEF","BBL1 row specific state",
"BBL2 row specific state", "BBL1 Data Analysis State", "BBL2 Data Analysis State"]
              
for row in data:
    row_state = analysis_state(row)
 
    for barrel, barrel_state in enumerate(row_state):
        if data_analysis_states[barrel] != barrel_state:
            print "State transition"   
            
        # Let's say that we're transitioning from an IPD state to another state
        # Per our definition the IPD continues until all barrels have existed
        # the freeze state - so we need to only change the barrel state when
        # all of the barrels are no longer in IPD
        if data_analysis_states[barrel] == "IPD":
            # any other barrels still freezing?
            if "Freezing" in row_state:
                pass # Don't modify the currently stored analysis state
            else:
                # At this point all barrels will have existed the IPD state
                data_analysis_states[barrel] = barrel_state
        else:
            data_analysis_states[barrel] = barrel_state
 
    print row + row_state +data_analysis_states
'''
#array=np.array([[1,2,3,4],[1,2,3,4],[4,3,2,1],[4,3,2,1],[5,6,7,8],[5,6,7,8],[8,7,6,5],[8,7,6,5]])
# np.delete(array,2,axis=1)
# the above deletes the third column.
# np.delete(array,np.s_[0:2],axis=1)
#the above deletes up to the third arrray from index 0
# np.delete(array,[(0:1),3],axis=1)
# above deletes the columns belonging to these indeces..