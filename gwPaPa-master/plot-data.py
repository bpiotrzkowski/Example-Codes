from pycbc import frame
import pickle
data = frame.read_frame('L-L1_STRAIN_BBH_1-1186741846-20.gwf', 'L-L1_STRAIN_BBH_1') #doesnot work. #uselal
injections = pickle.load(open('injections-BNS.p', "rb"))

###dis broke
