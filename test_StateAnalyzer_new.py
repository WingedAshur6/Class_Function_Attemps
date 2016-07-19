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
        
        self.data = np.fromfile('773logtest2_TEST.log', int, -1, "\t")
        self.columns=39#------------------------------------------------------------------------------------------------- I actually went and counted the number of columns in the output data
        self.data=np.reshape(self.data,(np.size(self.data)/self.columns,self.columns))#---------------------------------- to reshape the newly aqcuired dataset to represent the output data
        
        
    def StateIdentifier(self):
        self.number_of_data=7 #------------------------------------------------------------------------------------------ this is the number of columns of data per barrel.
        self.number_of_barrels=(np.size(self.data,1)-11)/self.number_of_data
        IPD_Columns=np.array([None,None,None,None],dtype=object)
        DEF_Columns=np.array([None,None,None,None],dtype=object)
        IPD_Columns=IPD_Columns[0:self.number_of_barrels]
        DEF_Columns=DEF_Columns[0:self.number_of_barrels]
        
        for barrel in range(self.number_of_barrels):
            print barrel
            #print COLUMN(self.data,10+5+7*barrel)

            IPD_Columns[barrel]=np.append(IPD_Columns[barrel],COLUMN(self.data,10+5+7*barrel))
            DEF_Columns[barrel]=np.append(DEF_Columns[barrel],COLUMN(self.data,10+6+7*barrel))
       
        IPD_Columns=np.transpose(IPD_Columns)
        DEF_Columns=np.transpose(DEF_Columns)
        state_columns=([IPD_Columns, DEF_Columns])#---------------------------------------------------------------------- this gets all the number of barrels and puts them together.
        return state_columns#-------------------------------------------------------------------------------------------- this will return as: [State:1->2][Barrel:1->4][time:START->END]
    
        
        
       
        
s=StateAnalyzer('773logtest2_TEST.log')        
        
print s.data
print np.shape(s.data)        
Data=s.StateIdentifier()
print Data
print np.shape(Data[0][1])
print Data[0][1][1:2000]
        
        
        
        
        
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