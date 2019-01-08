import math
import lal
import lalframe
import lalsimulation
import numpy as np
import pickle

def bbh_mass_distribution(u,mmin,mmax,alpha):
    if alpha != -1:
        return (u*(mmax**(alpha+1)-mmin**(alpha+1))+mmin**(alpha+1))**(1.0/(alpha+1))
    else:
        return np.exp(u*(np.log(mmax)-np.log(mmin))+np.log(mmin))
    
def simulate_merger(mass1,mass2,sim_id):
    # details about the detector
    detector_prefix = 'L1'
    sample_rate = 4096.0

    # details about the injection and fixed parameters
    waveform = 'IMRPhenomPv2pseudoFourPN'
    approximant = lalsimulation.GetApproximantFromString(str(waveform))
    geocentric_end_time = 1000
    right_ascension = 0.3
    declination = -0.4
    inclination = 0.0
    coalescence_phase = 0.0
    polarization_angle = 0.0
    low_frequency = 20.0
    lambda1 = lambda2 = 0.0
    distance = 1000.0
    spin1x = spin1y = 0.0
    spin2x = spin2y = 0.0
    spin1z = 0.0
    spin2z = 0.0

    parameters = {}
    parameters['m1'] = mass1*lal.MSUN_SI
    parameters['m2'] = mass2*lal.MSUN_SI
    parameters['S1x'] = spin1x
    parameters['S1y'] = spin1y
    parameters['S1z'] = spin1z
    parameters['S2x'] = spin2x
    parameters['S2y'] = spin2y
    parameters['S2z'] = spin2z
    parameters['distance'] = distance*1e6*lal.PC_SI
    parameters['inclination'] = inclination
    parameters['phiRef'] = coalescence_phase
    parameters['longAscNodes'] = 0.0
    parameters['eccentricity'] = 0.0
    parameters['meanPerAno'] = 0.0
    parameters['deltaT'] = 1.0 / sample_rate
    parameters['f_min'] = low_frequency
    parameters['f_ref'] = 0.0
    parameters['LALparams'] = None
    parameters['approximant'] = approximant
    
    h_plus, h_cross = lalsimulation.SimInspiralTD(**parameters)
#Docstring: SimInspiralTD(8 REAL8 distance, REAL8 inclination, REAL8 phiRef, REAL8 longAscNodes, REAL8 eccentricity, REAL8 meanPerAno, REAL8 deltaT, REAL8 f_min, REAL8 f_ref, Dict LALparams, Approx
    h_plus.epoch += geocentric_end_time
    h_cross.epoch += geocentric_end_time

    # compute strain in detector
    detector = lalsimulation.DetectorPrefixToLALDetector(detector_prefix)
    h = lalsimulation.SimDetectorStrainREAL8TimeSeries(
        hplus = h_plus,
        hcross = h_cross,
        right_ascension = right_ascension,
        declination = declination,
        psi = polarization_angle,
        detector = detector
    )

    # FIXME: correct the units of the strain
    #h.sampleUnits = lal.StrainUnit

    # create detector data time series

    # the start of the time series is one second before the beginning
    # of the injection and the end time is one second after it

    start_time = math.floor(h.epoch) - 4
    duration = math.ceil(h.data.length / sample_rate) + 8
    length = int(round(duration * sample_rate))
    channel_name = detector_prefix + ':STRAIN'
    # create zero-noise detector stream

    time_series = lal.CreateREAL8TimeSeries(
        name = channel_name,
        epoch = start_time,
        f0 = 0.0,
        deltaT = 1.0/sample_rate,
        sampleUnits = lal.StrainUnit,
        length = length
    )

    # zero the data
    time_series.data.data[:] = 0.0

    # add the injection to the detector time series
    lalsimulation.SimAddInjectionREAL8TimeSeries(time_series, h, None)

    # output the detector time series to a frame file
    lalframe.FrWriteREAL8TimeSeries(time_series, 0)
    theta = {
        'sim-id' : sim_id,
        'mass_1' : mass1,
        'mass_2' : mass2,
        'S1x' : spin1x,
        'S1y' : spin1y,
        'S1z' : spin1z,
        'S2x' : spin2x,
        'S2y' : spin2y,
        'S2z' : spin2z,
        'distance' : distance,
        'inclination' : inclination,
        'right_ascension' : right_ascension,
        'declination' : declination,
        'psi' : polarization_angle,
        'phiRef' : coalescence_phase,
        'lambda1' : lambda1,
        'lambda2' : lambda2,
        'f_min' : low_frequency,
        'f_ref' : 20.0,
        'deltaT' : 1.0 / sample_rate,
        'start_time' : start_time,
        'duration' : duration
    }
    return theta
