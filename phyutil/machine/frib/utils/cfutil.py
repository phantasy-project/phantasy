# encoding: UTF-8

"Utilities for working with Channel Finder"

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import sys

from channelfinder import ChannelFinderClient

from channelfinder.CFDataTypes import Property, Channel

from accel import *


def load(accel, uri, username=None, password=None, start=None, end=None, machine=""):

    client = ChannelFinderClient(BaseURL=uri, username=username, password=password)

    system = Property("system", username)
    subsystem = Property("subsystem", username)
    device = Property("device", username)
    dtype = Property("type", username)
    field = Property("field", username)
    machine = Property("machine", username, machine)
    setpoint = Property("handle", username, "setpoint")
    readback = Property("handle", username, "readback")
    name = Property("name", username)
    z = Property("Z", username)
    

    client.set(properties=[ system, subsystem, device, dtype, field, machine, setpoint, name, z ])


    def create_channels(names):
        channels = []
        for name in names:
            channels.append(Channel(name, username))
        client.set(channels=channels)


    for elem in accel.iter(start=start, end=end):
    
        if isinstance(elem, CavityElement):
           
            pha_channels = [ elem.channels.phase_cset, elem.channels.phase_rset, elem.channels.phase_read ]
            
            amp_channels = [ elem.channels.amplitude_cset, elem.channels.amplitude_rset, elem.channels.amplitude_read ]
            
            channels = pha_channels + amp_channels
            
            create_channels(channels)
            
            system.Value = elem.system
            client.update(property=system, channelNames=channels)
            
            subsystem.Value = elem.subsystem
            client.update(property=subsystem, channelNames=channels)
          
            device.Value = elem.device
            client.update(property=device, channelNames=channels)
            
            name.Value = elem.name
            client.update(property=name, channelNames=channels)
            
            z.Value = str(elem.z+elem.length/2.0)
            client.update(property=z, channelNames=channels)
            
            dtype.Value = "Cavity"
            client.update(property=dtype, channelNames=channels)
          
            field.Value = "Amplitude"
            client.update(property=field, channelNames=amp_channels)
            
            field.Value = "Phase"
            client.update(property=field, channelNames=pha_channels)
            
            client.update(property=setpoint, channelNames=[ pha_channels[0], amp_channels[0] ])
            client.update(property=readback, channelNames=pha_channels[1:] + amp_channels[1:])
            client.update(property=machine, channelNames=channels)
        
        elif isinstance(elem, SolCorrElement):
        
            sol_channels = [ elem.channels.field_cset, elem.channels.field_rset, elem.channels.field_read ]
        
            dch_channels = [ elem.channels.hkick_cset, elem.channels.hkick_rset, elem.channels.hkick_read ]
            
            dcv_channels = [ elem.channels.vkick_cset, elem.channels.vkick_rset, elem.channels.vkick_read ]
            
            channels = sol_channels + dch_channels + dcv_channels
            
            create_channels(channels)
            
            system.Value = elem.system
            client.update(property=system, channelNames=channels)
            
            subsystem.Value = elem.subsystem
            client.update(property=subsystem, channelNames=channels)
          
            device.Value = elem.device
            client.update(property=device, channelNames=sol_channels)
            
            device.Value = "DCH"
            client.update(property=device, channelNames=dch_channels)
            
            device.Value = "DCV"
            client.update(property=device, channelNames=dcv_channels)
            
            name.Value = elem.name
            client.update(property=name, channelNames=channels)
            
            z.Value = str(elem.z+elem.length/2.0)
            client.update(property=z, channelNames=channels)
            
            dtype.Value = "Solenoid"
            client.update(property=dtype, channelNames=sol_channels)
          
            dtype.Value = "DCH"
            client.update(property=dtype, channelNames=dch_channels)
          
            dtype.Value = "DCV"
            client.update(property=dtype, channelNames=dcv_channels)
          
            field.Value = "B"
            client.update(property=field, channelNames=sol_channels)
            
            field.Value = "HKICK"
            client.update(property=field, channelNames=dch_channels)
            
            field.Value = "VKICK"
            client.update(property=field, channelNames=dcv_channels)
            
            client.update(property=setpoint, channelNames=[ sol_channels[0], dch_channels[0], dcv_channels[0] ])
            client.update(property=readback, channelNames=sol_channels[1:] + dch_channels[1:] + dcv_channels[1:])
            client.update(property=machine, channelNames=channels)
        
        elif isinstance(elem, CorrElement):
        
            dch_channels = [ elem.channels.hkick_cset, elem.channels.hkick_rset, elem.channels.hkick_read ]
            
            dcv_channels = [ elem.channels.vkick_cset, elem.channels.vkick_rset, elem.channels.vkick_read ]
            
            channels = dch_channels + dcv_channels
            
            create_channels(channels)
            
            system.Value = elem.system
            client.update(property=system, channelNames=channels)
            
            subsystem.Value = elem.subsystem
            client.update(property=subsystem, channelNames=channels)
                      
            device.Value = "DCH"
            client.update(property=device, channelNames=dch_channels)
            
            device.Value = "DCV"
            client.update(property=device, channelNames=dcv_channels)
            
            name.Value = elem.name
            client.update(property=name, channelNames=channels)
            
            z.Value = str(elem.z+elem.length/2.0)
            client.update(property=z, channelNames=channels)
                      
            dtype.Value = "DCH"
            client.update(property=dtype, channelNames=dch_channels)
          
            dtype.Value = "DCV"
            client.update(property=dtype, channelNames=dcv_channels)
                      
            field.Value = "HKICK"
            client.update(property=field, channelNames=dch_channels)
            
            field.Value = "VKICK"
            client.update(property=field, channelNames=dcv_channels)
            
            client.update(property=setpoint, channelNames=[ dch_channels[0], dcv_channels[0] ])
            client.update(property=readback, channelNames=dch_channels[1:] + dcv_channels[1:])
            client.update(property=machine, channelNames=channels)
        
        elif isinstance(elem, QuadElement):
        
            channels = [ elem.channels.gradient_cset, elem.channels.gradient_rset, elem.channels.gradient_read ]
            
            create_channels(channels)
            
            system.Value = elem.system
            client.update(property=system, channelNames=channels)
            
            subsystem.Value = elem.subsystem
            client.update(property=subsystem, channelNames=channels)
                      
            device.Value = elem.device
            client.update(property=device, channelNames=channels)
                        
            name.Value = elem.name
            client.update(property=name, channelNames=channels)
            
            z.Value = str(elem.z+elem.length/2.0)
            client.update(property=z, channelNames=channels)
                      
            dtype.Value = "Quadrupole"
            client.update(property=dtype, channelNames=channels)
                                
            field.Value = "GRAD"
            client.update(property=field, channelNames=channels)
            
            client.update(property=setpoint, channelNames=[channels[0]])
            client.update(property=readback, channelNames=channels[1:])
            client.update(property=machine, channelNames=channels)
        
        elif isinstance(elem, BPMElement):
            
            x_channels = [ elem.channels.hposition_read ]
            
            y_channels = [ elem.channels.vposition_read ]
            
            channels = x_channels + y_channels
                    
            create_channels(channels)
            
            system.Value = elem.system
            client.update(property=system, channelNames=channels)
            
            subsystem.Value = elem.subsystem
            client.update(property=subsystem, channelNames=channels)
          
            device.Value = elem.device
            client.update(property=device, channelNames=channels)
                        
            name.Value = elem.name
            client.update(property=name, channelNames=channels)
            
            z.Value = str(elem.z+elem.length/2.0)
            client.update(property=z, channelNames=channels)
            
            dtype.Value = "BPM"
            client.update(property=dtype, channelNames=channels)
          
            field.Value = "X"
            client.update(property=field, channelNames=x_channels)
            
            field.Value = "Y"
            client.update(property=field, channelNames=y_channels)
                        
            client.update(property=readback, channelNames=channels)
            client.update(property=machine, channelNames=channels)
        
        elif isinstance(elem, (BLMElement, PMElement, BLElement)):
            # ignore these diagnostic elements
            pass
        
        elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
            # ignore these elements
            pass
                         
        else:
            raise RuntimeError("Unsupported element type: {}".format(type(elem).__name__))

