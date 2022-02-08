from pymeasure.instruments.agilent import AgilentB1500

# explicitly define r/w terminations; set sufficiently large timeout in milliseconds or None.
b1500 = AgilentB1500("GPIB0::19::INSTR", read_termination='\r\n', write_termination='\r\n', timeout=600000)
# query SMU config from instrument and initialize all SMU instances
b1500.initialize_all_smus()
CMU=b1500.initialize_cmu(9,'CMU')
# set data output format (required!)
b1500.data_format(21, mode=1) #call after SMUs are initialized to get names for the channels

# choose measurement mode
b1500.meas_mode('CV_SWEEP', CMU) #order in smu_references determines order of measurement


#Sweep Settings
#b1500.sweep_timing(0,5,step_delay=0.1) #hold,delay
b1500.sweep_auto_abort(False,post='STOP') #disable auto abort, set post measurement output condition to stop value of sweep
# Sweep Source
nop = 11
b1500.write("SSP 9, 4")
b1500.cmu7.ac_voltage(0.05)
b1500.cmu7.staircase_sweep(1,0,10,11)#type, mode, start, stop, steps


#Start Measurement
b1500.check_errors()
b1500.clear_buffer()
b1500.clear_timer()
b1500.send_trigger()

# read measurement data all at once
b1500.check_idle() #wait until measurement is finished
data = b1500.read_data(nop) #Factor 2 beacuse of double sweep

#alternatively: read measurement data live
meas = []
for i in range(nop*2):
    read_data = b1500.read_channels(4+1) # 4 measurement channels, 1 sweep source (returned due to mode=1 of data_format)
    # process live data for plotting etc.
    # data format for every channel (status code, channel name e.g. 'SMU1', data name e.g 'Current Measurement (A)', value)
    meas.append(read_data)

#sweep constant sources back to 0V
b1500.smu3.ramp_source('VOLTAGE','Auto Ranging',0,stepsize=0.1,pause=20e-3)
b1500.smu4.ramp_source('VOLTAGE','Auto Ranging',0,stepsize=0.1,pause=20e-3)