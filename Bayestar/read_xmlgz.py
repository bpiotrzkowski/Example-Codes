import numpy as np
from gwpy.table import EventTable
import matplotlib.pyplot as plt  


#recovered table names: 'process', 'process_params', 'segment_definer', 'segment_summary', 'segment', 'sim_inspiral', 'sngl_inspiral', 'coinc_definer', 'coinc_event', 'coinc_event_map', 'time_slide', 'coinc_inspiral'

#injection table names: 'process', 'process_params', 'sim_inspiral'

w1=EventTable.read('/home/gstlalcbc/observing/2/catalog/runs/O2_chunk_08_run_1_180818/H1L1-ALL_LLOID_rates_injections_0000-1172334618-853500.xml.gz',tablename='coinc_inspiral')
print(w1)
print(w1.keys())
w2=EventTable.read('/home/gstlalcbc/observing/2/catalog/injections/rates/O2_8/bns_astrophysical-1172334626-1173188118.xml.gz',tablename='sim_inspiral')
print(w2)
print(w2.keys())

EventTable.write(w1,'recovered_file.xml.gz',format='ligolw')
EventTable.write(w2,'injected_file.xml.gz',format='ligolw')
#print(tfull.keys())

recovered_time=EventTable.read('/home/gstlalcbc/observing/2/catalog/runs/O2_chunk_08_run_1_180818/H1L1-ALL_LLOID_rates_injections_0000-1172334618-853500.xml.gz', tablename='coinc_inspiral',columns=['end_time'])

#recovered_time=EventTable.read('/home/gstlalcbc/observing/2/catalog/runs/O2_chunk_08_run_1_180818/H1L1-ALL_LLOID_rates_injections_0000-1172334618-853500.xml.gz', tablename='sngl_inspiral',columns=['end_time'])

recovered=EventTable.read('/home/gstlalcbc/observing/2/catalog/runs/O2_chunk_08_run_1_180818/H1L1-ALL_LLOID_rates_injections_0000-1172334618-853500.xml.gz', tablename='coinc_inspiral',columns=['mchirp'])

#recovered=EventTable.read('/home/gstlalcbc/observing/2/catalog/runs/O2_chunk_08_run_1_180818/H1L1-ALL_LLOID_rates_injections_0000-1172334618-853500.xml.gz', tablename='sngl_inspiral',columns=['event_id','process_id','end_time','end_time_ns','mass1','mass2'])


injected_time=EventTable.read('/home/gstlalcbc/observing/2/catalog/injections/rates/O2_8/bns_astrophysical-1172334626-1173188118.xml.gz', tablename='sim_inspiral',columns=['l_end_time'])

injected=EventTable.read('/home/gstlalcbc/observing/2/catalog/injections/rates/O2_8/bns_astrophysical-1172334626-1173188118.xml.gz', tablename='sim_inspiral',columns=['simulation_id','process_id','l_end_time','mchirp','eta','mass1','mass2'])

print(recovered)

#table.filter('mass1<3.0',mass2<3.0')

print(injected)




mass_1=np.array(recovered['mass1'])
mass_2=np.array(recovered['mass2'])
mass_recovered=(mass_1*mass_2)**(3/5)/(mass_1+mass_2)**(1/5)
mass_injected=np.array(injected['mchirp'])

#print(mass_array[0])
#print(type(mass_array))
#print(type(mass_array[0]))

tarray=np.array(recovered_time)#recovered_time.as_array()
t2array=np.array(injected_time)#injected_time.as_array()

tarray=tarray.astype(float)
t2array=t2array.astype(float)

tarray,mask=np.unique(tarray,return_index=True)
t2array,mask2=np.unique(t2array,return_index=True)

mass_recovered=mass_recovered[mask]
mass_injected=mass_injected[mask2]

print(tarray[0])
print(type(tarray))
print(type(tarray[0]))

#print(tarray[0],t2array[0])
#intersect,ind1,ind2=np.intersect1d(tarray,t2array,assume_unique=True,return_indices=True)
#intersect,ind2,ind=np.intersect1d(t2array,tarray,assume_unique=True,return_indices=True)
#intersect=np.allclose(tarray,t2array,atol=5)
#print(intersect)
#print(ind1)
#print(ind2)

ind_recovered=np.in1d(tarray,t2array,assume_unique=True)
ind_injected=np.in1d(t2array,tarray,assume_unique=True)

mr=mass_recovered[ind_recovered]
mi=mass_injected[ind_injected]

print(tarray[ind_recovered])
print(t2array[ind_injected])

print('---')
print(mi)
print(mr)
#print(np.sort(tarray))
plt.plot(mi,mr,'.')
plt.plot([1,1],[3,3])
plt.xlabel(r'$\mathcal{M}$ (injected)')
plt.ylabel(r'$\mathcal{M}$ (recovered)')
plt.xlim(.95,1.5)
plt.ylim(.95,1.5)
plt.savefig('test_mass',dpi=200)
#plt.show()
#t['end_time'] , t2['l_end_time']

#print(t.as_array()==t2.as_array())
#print(np.asarray(t)==np.asarray(t2))

	
