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
        
    def StateIdentifier(self,num_barr):
        self.number_of_data=7 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is the number of columns of data per barrel.
        #self.number_of_barrels=(np.size(self.data,1)-11)/self.number_of_data
        self.true_data=self.number_of_data*num_barr
        self.number_of_barrels=self.true_data/self.number_of_data
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- vvvvvvvvvvvv Sizing the array to correctly represent input data
        FRZ_Columns=np.array([None,None,None,None],dtype=object)
        THAW_Columns=np.array([None,None,None,None],dtype=object)
        SMRT_STATE=np.array([None,None,None,None],dtype=object)
        ENG_STATE=np.array([None,None,None,None],dtype=object)
        FRZ_Columns=FRZ_Columns[0:self.number_of_barrels]
        THAW_Columns=THAW_Columns[0:self.number_of_barrels]
        SMRT_STATE=SMRT_STATE[0:self.number_of_barrels]#-------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to combine the freeze and defrost into a single array instead of two seperate ones.
        ENG_STATE=ENG_STATE[0:self.number_of_barrels]#---------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to combine the freeze and defrost into a single array instead of two seperate ones.

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ^^^^^^^^^^^^ Sizing the array to correctly represent input data
        
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- vvvvvvvvvvvv "Simplifying" states
        SIMPLE_STATES={0:0,4:0,3:0,5:0,9:0,7:0,10:0,8:3,11:2,777:1}#-------------------------------------------------------------------------------------------------------------------------------------------- Meaning: actual state 8: freezedown (3), actual state 11: defrost (2), SPECIAL STATE(777): IPD (1), all other states (0,4,3,5,7,9,10): Ignore (0) 
        INENGLISH_STATES={0:"IDLE",4:"IDLE",3:"IDLE",5:"IDLE",9:"IDLE",7:"IDLE",10:"IDLE",8:"FRZDWN",11:"DEFRST",777:"IPD"}
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ^^^^^^^^^^^^ "Simplifying" states
        
        
        for i in range(np.size(self.time,0)):
            for barrel in range(self.number_of_barrels):
                #print barrel
                #print COLUMN(self.data,10+5+7*barrel)

                FRZ_Columns[barrel]=SIMPLE_STATES[COLUMN(self.data,10+5+7*barrel)[i]]#COLUMN(self.data,10+5+7*barrel)[i]#np.append(FRZ_Columns[barrel],COLUMN(self.data,10+5+7*barrel))
                THAW_Columns[barrel]=SIMPLE_STATES[COLUMN(self.data,10+6+7*barrel)[i]]#COLUMN(self.data,10+6+7*barrel)[i]#np.append(THAW_Columns[barrel],COLUMN(self.data,10+6+7*barrel))
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to be a test implementation of the smartstate array
                if FRZ_Columns[barrel] !=0:
                    SMRT_STATE[barrel]=FRZ_Columns[barrel]
                    ENG_STATE[barrel]=INENGLISH_STATES[COLUMN(self.data,10+5+7*barrel)[i]]
                if FRZ_Columns[barrel] ==0:
                    SMRT_STATE[barrel]=THAW_Columns[barrel]
                    ENG_STATE[barrel]=INENGLISH_STATES[COLUMN(self.data,10+6+7*barrel)[i]]
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- this is supposed to be a test implementation of the smartstate array    
            print "Freeze Array: ",FRZ_Columns," Defrost Array : ",THAW_Columns," \"Smart\" Array: ",SMRT_STATE," Action Array: ",ENG_STATE
       
        FRZ_Columns=np.transpose(FRZ_Columns)
        THAW_Columns=np.transpose(THAW_Columns)
        state_columns=(["Actual States: ",FRZ_Columns, THAW_Columns,"Processed States: ", ])#--------------------------------------------------------------------------------------------------------------------- this gets all the number of barrels and puts them together format:[bbl1,bbl2,bbl3,bbl4],[simplebbl1,simplebbl2,simpebbl3,simplebbl4].
        
        '''#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 18:34
        IPD=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be IPD[barrel1][freezedown1,2,3,4], IPD[barrel2][freezedown1,2,3,4],etc.
        DEF=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be DEF[barrel1][Defrost1,2,3,4], DEF[barrel2][Defrost1,2,3,4],etc.
        REF=np.array([],dtype=object)#------------------------------------------------------------------------------------ this will be REF[barrel1][Refreeze1,2,3,4], REF[barrel2][Refreeze1,2,3,4],etc.
        
        for barrel_number in range(self.number_of_barrels):#-------------------------------------------------------------- this will go through the data recorded and get the phase stuff.
            DEF=np.append(DEF,[None])
            REF=np.append(REF,[None])
            
            for i in range(np.size(FRZ_Columns[barrel_number],0)):
            
                if FRZ_Columns[barrel_number][i-1]!=8 or FRZ_Columns[barrel_number][i+1]!=8:#----------------------------- this will basically run through the data and ONLY record the beginnings and ends of each freezedown.
                    REF[barrel_number]=np.append(REF[barrel_number],[self.time[i],self.time_easy[i]])
                    
                if THAW_Columns[barrel_number][i-1]!=11 or THAW_Columns[barrel_number][i+1]!=11:
                    DEF[barrel_number]=np.append(DEF[barrel_number],[self.time[i],self.time_easy[i]])
        
        #for barrel_number in range(self.number_of_barrels):
        for i in range(np.size(REF[barrel_number],0)):#--------------------------------------------------------------------- HERE will be the IPD finder.
            if REF[:][i-1] or REF[:][i+1]!=4:#----------------------------------------------------------------------------- how this is supposed to work: if all barrels have the 4, record as an IPD.
                IPD=np.append(IPD,i)
        phase_data=[IPD,DEF,REF]
        

        return phase_data
        ''''''#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 18:34
        '''    

                
        '''
        return state_columns#------------------------------------------------------------------------------------------------------------------------------------ this will return as: [State:1->2][Barrel:1->4][time:START->END]    * OLD ITERATION. 19 July 2016 16:49
        '''
        
        
       
        
s=StateAnalyzer('773logtest2_TEST_double.log')        
        
#print s.data
#print np.shape(s.data)      
'''#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 16:49  
Data=s.StateIdentifier()
print Data
print np.shape(Data[0][1])
print Data[0][1][1:2000]
''''''#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    * OLD ITERATION. 19 July 2016 16:49
'''
States=s.StateIdentifier(1)
#print States       
        
        
        
        
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