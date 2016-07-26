# Phase Analyzer re-write:

# 1) Create a class called StateAnalyzer which will do the following:
   # * Read in the logged data
   # * Scan the data to detect when the different phases start and stop
   # * Package up the collected data into State classes
   
# Example:

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
        self.number_of_data=7 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is the number of columns of data per barrel.
        
        self.number_of_barrels=(np.size(self.data,1)-11)/self.number_of_data       
        return self.number_of_barrels
    
    def StatePopulator(self,num_barr):
        self.number_of_data=7 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is the number of columns of data per barrel.
        self.number_of_barrels=4#--------------------------------------------------------------- CRITICAL HARDCODE VALUE. DO NOT CHANGE . -------------------------------------------------------------------------------------------------------- this is a CRITICAL HARDCODED VALUE. 
        
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
            #time.sleep(3)
           
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

        #time.sleep(10)
        #print Data[0][0],time.sleep(5)

        ipditeration=0
        ipdrun={}
        ipdrun[ipditeration]={}
        ipdrun[ipditeration]=State(ipditeration,None,None,None)
        ipdtimerec=0
        
        refreeze={}
        refreezeiteration={}
        refreezerunrec={}

        defrost={}
        defrostiteration={}
        defrostrunrec={}
        
        
        for i in range(num_barr):
            refreeze[i]={}
            refreezerunrec[i]=0
            refreezeiteration[i]=0
            refreeze[i][refreezeiteration[i]]=State(refreezeiteration[i],None,None,None)
            
            defrost[i]={}
            defrostrunrec[i]=0
            defrostiteration[i]=0
            defrost[i][defrostiteration[i]]=State(defrostiteration[i],None,None,None)            
                
                
                
                
        data_analysis_states=self.get_dataset(num_barr)
               
        for row in self.state_data:
            row_state = self.analysis_state(row,num_barr)
                
            for barrel, barrel_state in enumerate(row_state):
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                        
                if "IPD" in row_state and  ipdtimerec==0:#------------------------------------------------------------------------------------------------------------------------------------- When it enters IPD state.

                        
                        #print"\n\n capturing ipd START in IPD interval: ", ipdrun[ipditeration].barrel
                        #time.sleep(5)
                        ipdrun[ipditeration].start_time=row[0]-self.state_data[0][0]
                        ipdrun[ipditeration].state_name=row_state[barrel]
                        
                        
                        
                if "Freezing" in row_state[barrel] and refreezerunrec[barrel]==0 and not "IPD" in data_analysis_states:
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        refreeze[barrel][refreezeiteration[barrel]].start_time=row[0]-self.state_data[0][0]
                        refreeze[barrel][refreezeiteration[barrel]].barrel=barrel
                        refreeze[barrel][refreezeiteration[barrel]].state_name=row_state[barrel]
                        #print "\n\n capturing FRZ Start in Barrel: " ,barrel, "Time interval: ",refreezeiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        #time.sleep(3)
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        
                if not "Freezing" in row_state[barrel] and refreezerunrec[barrel]==1 and not "IPD" in data_analysis_states:
                        refreeze[barrel][refreezeiteration[barrel]].end_time=row[0]-self.state_data[0][0]
                        refreezerunrec[barrel]=10                    
                        #print "\n\n capturing FRZ end in Barrel: " ,barrel, "Time interval: ",refreezeiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        #time.sleep(3)
                        #print "\n\n Time end for FRZ in barrel: ",barrel,"Creating new time interval in barrel to allow recording. OLD interval: ", refreezeiteration[barrel]
                        refreezeiteration[barrel]+=1
                        print "To: ",refreezeiteration[barrel]
                        refreeze[barrel][refreezeiteration[barrel]]=State(refreezeiteration[i],None,None,None)
                        #time.sleep(10)
                        refreezerunrec[barrel]=0
                        
                        
                        
                if "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==0:
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        defrost[barrel][defrostiteration[barrel]].start_time=row[0]-self.state_data[0][0]
                        defrost[barrel][defrostiteration[barrel]].barrel=barrel
                        defrost[barrel][defrostiteration[barrel]].state_name=row_state[barrel]
                        #print "\n\n capturing DEF Start in Barrel: " ,barrel, "Time interval: ",defrostiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        #time.sleep(3)
                        #------------------------------------------------------------------------------------------------------- CRITICAL TEST CODE FOR THE FUTURE. DO NOT TOUCH. ---------------------------------------------------------------- THIS IS A TEST TO RECORD BARREL IPD TIMES THAT WILL BE USED FOR OTHER STATES. DONT TOUCH.
                        
                if not "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==1:
                        defrost[barrel][defrostiteration[barrel]].end_time=row[0]-self.state_data[0][0]
                        defrostrunrec[barrel]=10                    
                        #print "\n\n capturing DEF end in Barrel: " ,barrel, "Time interval: ",defrostiteration[barrel]," with time: ", row[0]-self.state_data[0][0]
                        #time.sleep(3)
                        #print "\n\n Time end for DEF in barrel: ",barrel,"Creating new time interval in barrel to allow recording. OLD interval: ", defrostiteration[barrel]
                        defrostiteration[barrel]+=1
                        print "To: ",defrostiteration[barrel]
                        defrost[barrel][defrostiteration[barrel]]=State(defrostiteration[i],None,None,None)
                        #time.sleep(10)
                        defrostrunrec[barrel]=0                        

                if not "IPD" in data_analysis_states and ipdtimerec==1:

                   
                    #print"\n\n capturing ipd END in IPD interval: ", ipdrun[ipditeration].barrel
                    ipdrun[ipditeration].end_time=row[0]-self.state_data[0][0]
                    ipditeration+=1
                    ipdrun[ipditeration]={}
                    ipdrun[ipditeration]=State(ipditeration,None,None,None)
                    ipdtimerec=0 
                    #print "\n\n new IPDrecorder created: ",ipdrun[ipditeration].barrel," Previous: ",ipdrun[ipditeration-1].barrel
                    #time.sleep(5)
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
                    
                    
                    
                if "IPD" in row_state and ipdtimerec==0:#----------------------------------------------------- CRITICAL IPD HARDCODE. DO NOT TOUCH. DO NOT MOVE. ---------------------------------------------------------- this must be here in order for the IPD recording to start.


                    #ipditeration+=1 #-----------------------------------------here is to say that the IPD recording phase has ended and a new one can start, IF the system enters ipd phase again.
                    ipdtimerec=1
                if not "IPD" in data_analysis_states and ipditeration!=0 and ipdtimerec!=0:
                        #print "\n\n IPD start time recorded already after new recorder made. State Transition found. recording END TIME."
                        #time.sleep(3)
                        ipdtimerec=0
                        #print"\n\n capturing ipd END in IPD interval: ", ipdrun[ipditeration].barrel
                        ipdrun[ipditeration].end_time=row[0]-self.state_data[0][0]
                        ipditeration+=1
                        ipdrun[ipditeration]={}
                        ipdrun[ipditeration]=State(ipditeration,None,None,None)
                        ipdtimerec=0 
                        #print "\n\n new IPDrecorder created: ",ipdrun[ipditeration].barrel," Previous: ",ipdrun[ipditeration-1].barrel
                        #time.sleep(5)    
                    
                # if "IPD" in row_state and ipdtimerec==1 and ipditeration !=0:
                    # ipdtimerec=0
                   
            #refreezerunrec[barrel]=0



                if "Freezing" in row_state[barrel] and refreezerunrec[barrel]==0 and not "IPD" in data_analysis_states:
                    #print "\n\n FRZ start time already recorded in barrel: ",barrel,"shifting staterunrecorder in barrel from: ", refreezerunrec[barrel]," to 1 to allow a recording of end time."
                    refreezerunrec[barrel]=1
                    #time.sleep(10)
                    
                if "Defrosting" in row_state[barrel] and defrostrunrec[barrel]==0:
                    #print "\n\n FRZ start time already recorded in barrel: ",barrel,"shifting staterunrecorder in barrel from: ", defrostrunrec[barrel]," to 1 to allow a recording of end time."
                    defrostrunrec[barrel]=1
                    #time.sleep(10)



            
            #print row , row_state ,data_analysis_states
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.ipd=ipdrun
        self.refreeze=refreeze
        self.defrost=defrost

                
        ''''''
        for i in range(num_barr):
            print "------------------------------------------< Barrel Number: ",i,">------------------------------------------"
            if np.size(ipdrun.items())>0:
                for l in range(ipditeration):#-----------debug
                    print "     IPD Time Iteration:      ",l
                    print "                                    IPD Start:      ",ipdrun[l].start_time,"\n                                    IPD End:        ",ipdrun[l].end_time,"\n                                    IPD Length:     ",ipdrun[l].length()   
            if np.size(refreezeiteration.items())>2:
                for j in range(refreezeiteration[i]):
                    print "     Refreeze Time Iteration: ",j
                    print "                                    Refreeze Start: ",refreeze[i][j].start_time,"\n                                    Refreeze End:   ",refreeze[i][j].end_time,"\n                                    Refreeze Length:",refreeze[i][j].length()   
            if np.size(defrostiteration.items())>2:
                for k in range((defrostiteration[i])):
                    print "     Defrost Time Iteration:  ",k
                    print "                                    Defrost Start:  ",defrost[i][k].start_time,"\n                                    Defrost End:    ",defrost[i][k].end_time,"\n                                    Defrost Length: ",defrost[i][k].length()   
                print"\n"
        ''''''
        self.ipditeration=ipditeration
        self.refreezeiteration=refreezeiteration
        self.defrostiteration=defrostiteration
        return  
    '''    
    def thecleaners(self,num_barr):# ------------------------------------------------------------ NOT WORKING. IMPLEMENT AND FIX LATER. -------------------------------------------------------------------------------
        self.newref={}
        rearranger={}
        import time
        for barrel in range(num_barr):
            self.newref[barrel]={}
            rearranger[barrel]=0
            self.newref[barrel][rearranger[barrel]]=State(None,None,None,None)
            for instance in range(self.refreezeiteration[barrel]):# ------------------------------------------------------- cleaning the refreeze
                if (self.refreeze[barrel][instance].start_time or self.refreeze[barrel][instance].end_time) <=self.ipd[barrel].end_time and (self.refreeze[barrel][instance].start_time or self.refreeze[barrel][instance].end_time) >=self.ipd[barrel].start_time or   not (self.refreeze[barrel][instance].end_time-self.refreeze[barrel][instance].start_time) >=20:

                        print "There Was a REFREEZE iteration that did not meet criteria to be deemed a refreeze. removing from states."
                        time.sleep(.1)
                        self.newref[barrel][rearranger[barrel]]=State(self.refreeze[barrel][instance].barrel,self.refreeze[barrel][instance].start_time,self.refreeze[barrel][instance].end_time,self.refreeze[barrel][instance].state_name)
                        self.newref[barrel][rearranger[barrel]].start_time=self.refreeze[barrel][instance].start_time
                        self.newref[barrel][rearranger[barrel]].end_time=self.refreeze[barrel][instance].end_time
                        self.refreeze[barrel].pop(instance)
                        self.refreezeiteration[barrel]=rearranger[barrel]
                rearranger[barrel]+=1

        #self.refreeze=self.newref
        print self.refreeze[0].viewkeys()
        print self.refreeze[0][1].start_time
    '''        
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
        
        
        
        def_RFG_hi={}
        def_RFG_lo={}
        def_V={}
        def_DC={}
        def_SUP={}
        def_RT={}
        def_BTR={}
        
        
        ipd_RFG_hi={}
        ipd_RFG_lo={}
        ipd_V={}
        ipd_DC={}
        ipd_SUP={}
        ipd_RT={}
        ipd_BTR={}

        
        
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
            #print self.refreezeiteration[ref_barrel]
            for ref_instance in range((self.refreezeiteration[ref_barrel])):
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                ref_RFG_lo[ref_barrel][ref_instance]={}
                ref_RFG_lo[ref_barrel][ref_instance]={}
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((ref_RFG_lo[ref_barrel][ref_instance]),np.s_[1:4],axis=1)
                ref_RFG_lo[ref_barrel][ref_instance]=np.delete((ref_RFG_lo[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                ref_RFG_hi[ref_barrel][ref_instance]={}
                ref_RFG_hi[ref_barrel][ref_instance]={}
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((ref_RFG_hi[ref_barrel][ref_instance]),np.s_[1:5],axis=1)
                ref_RFG_hi[ref_barrel][ref_instance]=np.delete((ref_RFG_hi[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                ref_V[ref_barrel][ref_instance]={}
                ref_V[ref_barrel][ref_instance]={}
                ref_V[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_V[ref_barrel][ref_instance]=np.delete((ref_V[ref_barrel][ref_instance]),np.s_[1:6],axis=1)
                ref_V[ref_barrel][ref_instance]=np.delete((ref_V[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                ref_RT[ref_barrel][ref_instance]={}
                ref_RT[ref_barrel][ref_instance]={}
                ref_RT[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_RT[ref_barrel][ref_instance]=np.delete((ref_RT[ref_barrel][ref_instance]),np.s_[1:7],axis=1)
                ref_RT[ref_barrel][ref_instance]=np.delete((ref_RT[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                ref_SUP[ref_barrel][ref_instance]={}
                ref_SUP[ref_barrel][ref_instance]={}
                ref_SUP[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_SUP[ref_barrel][ref_instance]=np.delete((ref_SUP[ref_barrel][ref_instance]),np.s_[1:8],axis=1)
                ref_SUP[ref_barrel][ref_instance]=np.delete((ref_SUP[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                ref_DC[ref_barrel][ref_instance]={}
                ref_DC[ref_barrel][ref_instance]={}
                ref_DC[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_DC[ref_barrel][ref_instance]=np.delete((ref_DC[ref_barrel][ref_instance]),np.s_[1:9],axis=1)
                ref_DC[ref_barrel][ref_instance]=np.delete((ref_DC[ref_barrel][ref_instance]),np.s_[2:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                ref_BTR[ref_barrel][ref_instance]={}
                ref_BTR[ref_barrel][ref_instance]={}
                ref_BTR[ref_barrel][ref_instance]=np.delete((self.data[self.refreeze[ref_barrel][ref_instance].start_time:self.refreeze[ref_barrel][ref_instance].end_time]),0,axis=1)
                ref_BTR[ref_barrel][ref_instance]=np.delete((ref_BTR[ref_barrel][ref_instance]),np.s_[1:12+7*ref_barrel],axis=1)
                ref_BTR[ref_barrel][ref_instance]=np.delete((ref_BTR[ref_barrel][ref_instance]),np.s_[2:],axis=1)    

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
            #print self.defrostiteration[def_barrel]
            for def_instance in range((self.defrostiteration[def_barrel])):
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                def_RFG_lo[def_barrel][def_instance]={}
                def_RFG_lo[def_barrel][def_instance]={}
                def_RFG_lo[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RFG_lo[def_barrel][def_instance]=np.delete((def_RFG_lo[def_barrel][def_instance]),np.s_[1:4],axis=1)
                def_RFG_lo[def_barrel][def_instance]=np.delete((def_RFG_lo[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                def_RFG_hi[def_barrel][def_instance]={}
                def_RFG_hi[def_barrel][def_instance]={}
                def_RFG_hi[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RFG_hi[def_barrel][def_instance]=np.delete((def_RFG_hi[def_barrel][def_instance]),np.s_[1:5],axis=1)
                def_RFG_hi[def_barrel][def_instance]=np.delete((def_RFG_hi[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                def_V[def_barrel][def_instance]={}
                def_V[def_barrel][def_instance]={}
                def_V[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_V[def_barrel][def_instance]=np.delete((def_V[def_barrel][def_instance]),np.s_[1:6],axis=1)
                def_V[def_barrel][def_instance]=np.delete((def_V[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                def_RT[def_barrel][def_instance]={}
                def_RT[def_barrel][def_instance]={}
                def_RT[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_RT[def_barrel][def_instance]=np.delete((def_RT[def_barrel][def_instance]),np.s_[1:7],axis=1)
                def_RT[def_barrel][def_instance]=np.delete((def_RT[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                def_SUP[def_barrel][def_instance]={}
                def_SUP[def_barrel][def_instance]={}
                def_SUP[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_SUP[def_barrel][def_instance]=np.delete((def_SUP[def_barrel][def_instance]),np.s_[1:8],axis=1)
                def_SUP[def_barrel][def_instance]=np.delete((def_SUP[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                def_DC[def_barrel][def_instance]={}
                def_DC[def_barrel][def_instance]={}
                def_DC[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_DC[def_barrel][def_instance]=np.delete((def_DC[def_barrel][def_instance]),np.s_[1:9],axis=1)
                def_DC[def_barrel][def_instance]=np.delete((def_DC[def_barrel][def_instance]),np.s_[2:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                def_BTR[def_barrel][def_instance]={}
                def_BTR[def_barrel][def_instance]={}
                def_BTR[def_barrel][def_instance]=np.delete((self.data[self.defrost[def_barrel][def_instance].start_time:self.defrost[def_barrel][def_instance].end_time]),0,axis=1)
                def_BTR[def_barrel][def_instance]=np.delete((def_BTR[def_barrel][def_instance]),np.s_[1:12+7*def_barrel],axis=1)
                def_BTR[def_barrel][def_instance]=np.delete((def_BTR[def_barrel][def_instance]),np.s_[2:],axis=1)   

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
            for ipd_instance in range(self.ipditeration):
            
                #--------------------------------------------------------------------------- RFG_Low ---------------------------------------------------------------------------------------------------------------------
                ipd_RFG_lo[ipd_barrel][ipd_instance]={}
                ipd_RFG_lo[ipd_barrel][ipd_instance]={}
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_lo[ipd_barrel][ipd_instance]),np.s_[1:4],axis=1)
                ipd_RFG_lo[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_lo[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RFG_High ---------------------------------------------------------------------------------------------------------------------
                ipd_RFG_hi[ipd_barrel][ipd_instance]={}
                ipd_RFG_hi[ipd_barrel][ipd_instance]={}
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_hi[ipd_barrel][ipd_instance]),np.s_[1:5],axis=1)
                ipd_RFG_hi[ipd_barrel][ipd_instance]=np.delete((ipd_RFG_hi[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- Voltage ---------------------------------------------------------------------------------------------------------------------
                ipd_V[ipd_barrel][ipd_instance]={}
                ipd_V[ipd_barrel][ipd_instance]={}
                ipd_V[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_V[ipd_barrel][ipd_instance]=np.delete((ipd_V[ipd_barrel][ipd_instance]),np.s_[1:6],axis=1)
                ipd_V[ipd_barrel][ipd_instance]=np.delete((ipd_V[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- RTemp ---------------------------------------------------------------------------------------------------------------------
                ipd_RT[ipd_barrel][ipd_instance]={}
                ipd_RT[ipd_barrel][ipd_instance]={}
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((ipd_RT[ipd_barrel][ipd_instance]),np.s_[1:7],axis=1)
                ipd_RT[ipd_barrel][ipd_instance]=np.delete((ipd_RT[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                #--------------------------------------------------------------------------- SUPRHT ---------------------------------------------------------------------------------------------------------------------
                ipd_SUP[ipd_barrel][ipd_instance]={}
                ipd_SUP[ipd_barrel][ipd_instance]={}
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((ipd_SUP[ipd_barrel][ipd_instance]),np.s_[1:8],axis=1)
                ipd_SUP[ipd_barrel][ipd_instance]=np.delete((ipd_SUP[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                
                #--------------------------------------------------------------------------- DUTYCycles ---------------------------------------------------------------------------------------------------------------------
                ipd_DC[ipd_barrel][ipd_instance]={}
                ipd_DC[ipd_barrel][ipd_instance]={}
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((ipd_DC[ipd_barrel][ipd_instance]),np.s_[1:9],axis=1)
                ipd_DC[ipd_barrel][ipd_instance]=np.delete((ipd_DC[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)
                
                
                
                
                #--------------------------------------------------------------------------- BTR ---------------------------------------------------------------------------------------------------------------------
                ipd_BTR[ipd_barrel][ipd_instance]={}
                ipd_BTR[ipd_barrel][ipd_instance]={}
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((self.data[self.ipd[ipd_instance].start_time:self.ipd[ipd_instance].end_time]),0,axis=1)
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((ipd_BTR[ipd_barrel][ipd_instance]),np.s_[1:12+7*ipd_barrel],axis=1)
                ipd_BTR[ipd_barrel][ipd_instance]=np.delete((ipd_BTR[ipd_barrel][ipd_instance]),np.s_[2:],axis=1)


        self.ipd_BTR=ipd_BTR
        self.ipd_RFG_lo=ipd_RFG_lo
        self.ipd_RFG_hi=ipd_RFG_hi
        self.ipd_V=ipd_V
        self.ipd_RT=ipd_RT
        self.ipd_SUP=ipd_SUP
        self.ipd_DC=ipd_DC



        for barrel in range(num_barr):
            ipdprops[barrel]={}
            defprops[barrel]={}
            refprops[barrel]={}
            for instance in range(self.ipditeration):
                ipdprops[barrel][instance]={}
                ipdprops[barrel][instance]={0:self.ipd_RFG_lo[barrel][instance]}
                ipdprops[barrel][instance].update({1:self.ipd_RFG_hi[barrel][instance]})
                ipdprops[barrel][instance].update({2:self.ipd_V[barrel][instance]})
                ipdprops[barrel][instance].update({3:self.ipd_RT[barrel][instance]})
                ipdprops[barrel][instance].update({4:self.ipd_SUP[barrel][instance]})
                ipdprops[barrel][instance].update({5:self.ipd_DC[barrel][instance]})
                ipdprops[barrel][instance].update({6:self.ipd_BTR[barrel][instance]})

            for instance in range(self.refreezeiteration[barrel]):
                refprops[barrel][instance]={0:self.ref_RFG_lo[barrel][instance]}
                refprops[barrel][instance].update({1:self.ref_RFG_hi[barrel][instance]})
                refprops[barrel][instance].update({2:self.ref_V[barrel][instance]})
                refprops[barrel][instance].update({3:self.ref_RT[barrel][instance]})
                refprops[barrel][instance].update({4:self.ref_SUP[barrel][instance]})
                refprops[barrel][instance].update({5:self.ref_DC[barrel][instance]})
                refprops[barrel][instance].update({6:self.ref_BTR[barrel][instance]})
        
            for instance in range(self.defrostiteration[barrel]):
                defprops[barrel][instance]={}
                defprops[barrel][instance]={0:self.def_RFG_lo[barrel][instance]}
                defprops[barrel][instance].update({1:self.def_RFG_hi[barrel][instance]})
                defprops[barrel][instance].update({2:self.def_V[barrel][instance]})
                defprops[barrel][instance].update({3:self.def_RT[barrel][instance]})
                defprops[barrel][instance].update({4:self.def_SUP[barrel][instance]})
                defprops[barrel][instance].update({5:self.def_DC[barrel][instance]})
                defprops[barrel][instance].update({6:self.def_BTR[barrel][instance]})
                
        
        self.ipdprops=ipdprops
        self.defprops=defprops
        self.refprops=refprops
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
   

    def display_plots(self,num_barr,state):
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
        from datetime import timedelta
        '''
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        # ##-------------------------------------------------------------------------- CLASS IMPORT ---------------------------------------------------------------------------
        '''
        
        
        
        
        
        
        
        
        
        
        Barrels=["BBL_1","BBL_2","BBL_3","BBL_4"]
        States=["IPD","Defrost","Refreeze"]
        stats=["RFGLow","RFGHigh", "V", "RTemp", "SUPRHT", "DTYCycles", "BTR%"]
        
        print "\n          ","---"*10,"< Initializing Plots >","---"*10
        
        print "State: ",state.upper()
        state=state.lower()
        if state=="ipd":
            num_statistics=np.size(stats)            
            #----------------------------------------------------------- Counting the number of times IPD is entered:
            print "\n Number of IPD states: ",(self.ipditeration)
            #----------------------------------------------------------- Counting the number of statistics that exist:
            print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            numcols=(num_statistics-1)/2
            numrows=(num_statistics-1)/3
            print numcols," columns, and ",numrows," rows."
            for L in range(num_barr):
             for K in range(self.ipditeration):
             
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                BTRx=range(self.ipd[K].length())
                BTRy_hold=np.delete(self.ipdprops[L][K][6],0,axis=1)
                BTRy=BTRy_hold[:]
                zip(BTRx,BTRy)
                BTRfig=plt.figure()
                #plots=zip(BTRx,BTRy)
                plt.plot(np.transpose(BTRx),BTRy,'b')
                plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[0],stats[6],K))
                plt.show()                
                
               
                
                fig=plt.figure()
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                for J in range(num_statistics-1):
                    title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[J],K)]
                    print title
                    x_hold=np.delete(self.ipdprops[L][K][J],1,axis=1)
                    x_hold=range(self.ipd[K].length())
                    #x=np.array([],dtype=object)
                    #x=np.append(x,x_hold[:])
                    x.append(x_hold[:])
                    #print x
                    y_hold=np.delete(self.ipdprops[L][K][J],0,axis=1)
                    #y=np.array([],dtype=object)
                    y.append(y_hold[:])
                plots=zip(x,y)
                axs={}
                for idx,plot in enumerate(plots):
                    axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    axs[idx].plot(plot[0],plot[1],'b')
                    plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[idx],K)])
                print np.shape(x)
                plt.show()

        elif state=="refreeze":
            num_statistics=np.size(stats)            
            #----------------------------------------------------------- Counting the number of times IPD is entered:
            print "\n Number of IPD states: ",(self.refreezeiteration)
            #----------------------------------------------------------- Counting the number of statistics that exist:
            print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            numcols=(num_statistics-1)/2
            numrows=(num_statistics-1)/3
            print numcols," columns, and ",numrows," rows."
            for L in range(num_barr):
             for K in range(self.refreezeiteration[L]):
             
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                BTRx=range(self.refreeze[L][K].length())
                BTRy_hold=np.delete(self.refprops[L][K][6],0,axis=1)
                BTRy=BTRy_hold[:]
                zip(BTRx,BTRy)
                BTRfig=plt.figure()
                #plots=zip(BTRx,BTRy)
                plt.plot(np.transpose(BTRx),BTRy,'c')
                plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[2],stats[6],K))
                plt.show()                
                
               
                
                fig=plt.figure()
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                for J in range(num_statistics-1):
                    title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[J],K)]
                    print title
                    x_hold=np.delete(self.refprops[L][K][J],1,axis=1)
                    x_hold=range(self.refreeze[L][K].length())
                    #x=np.array([],dtype=object)
                    #x=np.append(x,x_hold[:])
                    x.append(x_hold[:])
                    #print x
                    y_hold=np.delete(self.refprops[L][K][J],0,axis=1)
                    #y=np.array([],dtype=object)
                    y.append(y_hold[:])
                plots=zip(x,y)
                axs={}
                for idx,plot in enumerate(plots):
                    axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    axs[idx].plot(plot[0],plot[1],'c')
                    plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[idx],K)])
                print np.shape(x)
                plt.show()

        elif state=="defrost":
            num_statistics=np.size(stats)            
            #----------------------------------------------------------- Counting the number of times IPD is entered:
            print "\n Number of IPD states: ",(self.defrostiteration)
            #----------------------------------------------------------- Counting the number of statistics that exist:
            print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
            print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
            numcols=(num_statistics-1)/2
            numrows=(num_statistics-1)/3
            print numcols," columns, and ",numrows," rows."
            for L in range(num_barr):
             for K in range(self.defrostiteration[L]):
             
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                BTRx=range(self.defrost[L][K].length())
                BTRy_hold=np.delete(self.defprops[L][K][6],0,axis=1)
                BTRy=BTRy_hold[:]
                zip(BTRx,BTRy)
                BTRfig=plt.figure()
                #plots=zip(BTRx,BTRy)
                plt.plot(np.transpose(BTRx),BTRy,'m')
                plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[1],stats[6],K))
                plt.show()                
                
               
                
                fig=plt.figure()
                x=np.array([],dtype=object)
                y=np.array([],dtype=object)
                x=[]
                y=[]
                for J in range(num_statistics-1):
                    title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[J],K)]
                    print title
                    x_hold=np.delete(self.defprops[L][K][J],1,axis=1)
                    x_hold=range(self.defrost[L][K].length())
                    #x=np.array([],dtype=object)
                    #x=np.append(x,x_hold[:])
                    x.append(x_hold[:])
                    #print x
                    y_hold=np.delete(self.defprops[L][K][J],0,axis=1)
                    #y=np.array([],dtype=object)
                    y.append(y_hold[:])
                    
                plots=zip(x,y)
                axs={}
                for idx,plot in enumerate(plots):
                    axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                    axs[idx].plot(plot[0],plot[1],'m')
                    plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[idx],K)])
                print np.shape(x)
                plt.show()
                
        else:
            
                num_statistics=np.size(stats)            
                #----------------------------------------------------------- Counting the number of times IPD is entered:
                print "\n Number of IPD states: ",(self.ipditeration)
                #----------------------------------------------------------- Counting the number of statistics that exist:
                print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                numcols=(num_statistics-1)/2
                numrows=(num_statistics-1)/3
                print numcols," columns, and ",numrows," rows."
                for L in range(num_barr):
                 for K in range(self.ipditeration):
                 
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    BTRx=range(self.ipd[K].length())
                    BTRy_hold=np.delete(self.ipdprops[L][K][6],0,axis=1)
                    BTRy=BTRy_hold[:]
                    zip(BTRx,BTRy)
                    BTRfig=plt.figure()
                    #plots=zip(BTRx,BTRy)
                    plt.plot(np.transpose(BTRx),BTRy,'b')
                    plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[0],stats[6],K))
                    plt.show()                
                    
                   
                    
                    fig=plt.figure()
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    for J in range(num_statistics-1):
                        title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[J],K)]
                        print title
                        x_hold=np.delete(self.ipdprops[L][K][J],1,axis=1)
                        x_hold=range(self.ipd[K].length())
                        #x=np.array([],dtype=object)
                        #x=np.append(x,x_hold[:])
                        x.append(x_hold[:])
                        #print x
                        y_hold=np.delete(self.ipdprops[L][K][J],0,axis=1)
                        #y=np.array([],dtype=object)
                        y.append(y_hold[:])
                    plots=zip(x,y)
                    axs={}
                    for idx,plot in enumerate(plots):
                        axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        axs[idx].plot(plot[0],plot[1],'b')
                        plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[0],stats[idx],K)])
                    print np.shape(x)
                    plt.show()
                
                
                num_statistics=np.size(stats)            
                #----------------------------------------------------------- Counting the number of times IPD is entered:
                print "\n Number of IPD states: ",(self.refreezeiteration)
                #----------------------------------------------------------- Counting the number of statistics that exist:
                print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                numcols=(num_statistics-1)/2
                numrows=(num_statistics-1)/3
                print numcols," columns, and ",numrows," rows."
                for L in range(num_barr):
                 for K in range(self.refreezeiteration[L]):
                 
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    BTRx=range(self.refreeze[L][K].length())
                    BTRy_hold=np.delete(self.refprops[L][K][6],0,axis=1)
                    BTRy=BTRy_hold[:]
                    zip(BTRx,BTRy)
                    BTRfig=plt.figure()
                    #plots=zip(BTRx,BTRy)
                    plt.plot(np.transpose(BTRx),BTRy,'c')
                    plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[2],stats[6],K))
                    plt.show()                
                    
                   
                    
                    fig=plt.figure()
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    for J in range(num_statistics-1):
                        title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[J],K)]
                        print title
                        x_hold=np.delete(self.refprops[L][K][J],1,axis=1)
                        x_hold=range(self.refreeze[L][K].length())
                        #x=np.array([],dtype=object)
                        #x=np.append(x,x_hold[:])
                        x.append(x_hold[:])
                        #print x
                        y_hold=np.delete(self.refprops[L][K][J],0,axis=1)
                        #y=np.array([],dtype=object)
                        y.append(y_hold[:])
                    plots=zip(x,y)
                    axs={}
                    for idx,plot in enumerate(plots):
                        axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        axs[idx].plot(plot[0],plot[1],'c')
                        plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[idx],K)])
                    print np.shape(x)
                    plt.show()
                
                
                
                num_statistics=np.size(stats)            
                #----------------------------------------------------------- Counting the number of times IPD is entered:
                print "\n Number of IPD states: ",(self.refreezeiteration)
                #----------------------------------------------------------- Counting the number of statistics that exist:
                print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                numcols=(num_statistics-1)/2
                numrows=(num_statistics-1)/3
                print numcols," columns, and ",numrows," rows."
                for L in range(num_barr):
                 for K in range(self.refreezeiteration[L]):
                 
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    BTRx=range(self.refreeze[L][K].length())
                    BTRy_hold=np.delete(self.refprops[L][K][6],0,axis=1)
                    BTRy=BTRy_hold[:]
                    zip(BTRx,BTRy)
                    BTRfig=plt.figure()
                    #plots=zip(BTRx,BTRy)
                    plt.plot(np.transpose(BTRx),BTRy,'c')
                    plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[2],stats[6],K))
                    plt.show()                
                    
                   
                    
                    fig=plt.figure()
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    for J in range(num_statistics-1):
                        title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[J],K)]
                        print title
                        x_hold=np.delete(self.refprops[L][K][J],1,axis=1)
                        x_hold=range(self.refreeze[L][K].length())
                        #x=np.array([],dtype=object)
                        #x=np.append(x,x_hold[:])
                        x.append(x_hold[:])
                        #print x
                        y_hold=np.delete(self.refprops[L][K][J],0,axis=1)
                        #y=np.array([],dtype=object)
                        y.append(y_hold[:])
                    plots=zip(x,y)
                    axs={}
                    for idx,plot in enumerate(plots):
                        axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        axs[idx].plot(plot[0],plot[1],'c')
                        plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[2],stats[idx],K)])
                    print np.shape(x)
                    plt.show()

            
                num_statistics=np.size(stats)            
                #----------------------------------------------------------- Counting the number of times IPD is entered:
                print "\n Number of IPD states: ",(self.defrostiteration)
                #----------------------------------------------------------- Counting the number of statistics that exist:
                print "\n Number of statistics: ",num_statistics,"\n Displaying: \n\n","-----"*15,"\n  ",stats,"\n","-----"*15
                print "\n\nBTR% will be plotted seperately. thus, new statistics plots will have:"
                numcols=(num_statistics-1)/2
                numrows=(num_statistics-1)/3
                print numcols," columns, and ",numrows," rows."
                for L in range(num_barr):
                 for K in range(self.defrostiteration[L]):
                 
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    BTRx=range(self.defrost[L][K].length())
                    BTRy_hold=np.delete(self.defprops[L][K][6],0,axis=1)
                    BTRy=BTRy_hold[:]
                    zip(BTRx,BTRy)
                    BTRfig=plt.figure()
                    #plots=zip(BTRx,BTRy)
                    plt.plot(np.transpose(BTRx),BTRy,'m')
                    plt.title("%s: %s, %s, iteration: %d" %(Barrels[L],States[1],stats[6],K))
                    plt.show()                
                    
                   
                    
                    fig=plt.figure()
                    x=np.array([],dtype=object)
                    y=np.array([],dtype=object)
                    x=[]
                    y=[]
                    for J in range(num_statistics-1):
                        title=["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[J],K)]
                        print title
                        x_hold=np.delete(self.defprops[L][K][J],1,axis=1)
                        x_hold=range(self.defrost[L][K].length())
                        #x=np.array([],dtype=object)
                        #x=np.append(x,x_hold[:])
                        x.append(x_hold[:])
                        #print x
                        y_hold=np.delete(self.defprops[L][K][J],0,axis=1)
                        #y=np.array([],dtype=object)
                        y.append(y_hold[:])
                        
                    plots=zip(x,y)
                    axs={}
                    for idx,plot in enumerate(plots):
                        axs[idx]=fig.add_subplot(numrows,numcols,idx+1)
                        axs[idx].plot(plot[0],plot[1],'m')
                        plt.title(["%s: %s, %s,  iteration: %d" % (Barrels[L],States[1],stats[idx],K)])
                    print np.shape(x)
                    plt.show()





        
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##-------------------------------------------------------------------------------- CODE TEST INITIALIZATION  -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.           
            
s=StateAnalyzer('773logtest2_TEST.log')#('773TESTQUAD.log')#('773logtest2_TEST.log')#'774LABTEST.log')        
num_barr=s.bar_counter() 
# print num_barr   
num_barr=4
num_barr_to_use=3 #------------------------------------------------------------------------ returns an error sometimes if the barrels used in anlysis dont match with barrels actually working.
s.StatePopulator(num_barr_to_use)#_to_use)


s.analysis_of_states(num_barr_to_use)

# state hierarchy: IPD: number of iterations --> [ .start_time, .end_time]  --------------------------------------------------->>>>>> object.ipd[iteration number].start_time or object.ipd[barrel].end_time
                 # Refreeze and Defrost: barrel -->number of iterations --> [ .start_time, .end_time]-------------------------->>>>>> object.refreeze/defrost[barrel][iteration number].start_time or .end_time


s.getdata(num_barr_to_use)
#print s.ipd_BTR[0][0]
#print s.ipd[0].length()
#print s.ref_BTR[0][1]



# property legend:  obect.ipdprops/refprops/defprops[barrel][instance][KEY TO PROPERTY:  0=RFGLOW  1=RFGHIGH 2=V  3=RTemp  4=SUPRHT  5=DUTYCycles  6=BTR]
#print s.ipdprops[0][0][0]


s.display_plots(num_barr_to_use,"all")
##-------------------------------------------------------------------------------- CODE TEST INITIALIZATION  -------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.  
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- These are everything needed to currently run the code.              




































































































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

        #time.sleep(10)
        #print Data[0][0],time.sleep(5)
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
            print "Barrel: ",statingrun[x].barrel," Start Time: ",statingrun[x].start_time," End Time: ",statingrun[x].end_time," State: ",statingrun[x].state_name
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
# above deletes the columns belonging to these indeces.