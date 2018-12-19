import numpy as np

def twindow(t,h,t0,tl): 
	ind=(t0<t)==(t<(t0+tl))
	return h[ind]

