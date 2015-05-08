"""
Core phyutil model
==================

Defines the fundamental accelerator simulation related routines
Imported from NSLS II APHLA

:author: Lingyun Yang

:modified: Guobao Shen

"""

import logging

from impact import build_result as build_impact_result

_logger = logging.getLogger(__name__)


class Model:
    """ Model results
    """
    def __init__(self, simulation="IMPACT", resultdir=None):
        """class constructor.
        
        :param simulation: simulation code name, either "IMPACT", "TLM", or others
        """
        self.code = simulation.upper()
        self.modelresult=None
        self.resultdir = resultdir
        
    def _buildModelResult(self):
        """
        """
        if self.code == "IMPACT":
            self.modelresult = build_impact_result(directory=self.resultdir)
        else:
            raise Exception("Simulation code {0} not supported yet".format(self.code))
    
    def updateModelResult(self):
        """Update model result
        
        :return: Model object
        """
        return self.modelresult.updateResult()
    
    def getEnergy(self, elemIdx=None):
        """get current sub-machine beam energy.
        Energy for a storage ring, or energy at given device for accelerating machine.
        If device is None, then final deliver energy.
        MeV for electron machine, or MeV/u for a heavy ion machine.
    
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getEnergy(elemIdx)
    
    def getSPosition(self, elemIdx=None):
        """Get element s position at the end if elemIdx is given, or list of s position for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: s position or list
        :raise: RuntimeError
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getSPosition(elemIdx)

    def getAbsPhase(self, elemIdx=None):
        """Get accumulated beam phase in radian at the end if elemIdx is given, 
        or a list for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: accumulated beam phase or list
        :raise: RuntimeError
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getAbsPhase(elemIdx)
    
    def getBetaGamma(self, elemIdx=None):
        """Get beam beta*gamma at the end if elemIdx is given, or a list for all totalelements
        
        :param elemIdx: index number of given element
        
        :return: beta*gamma or list
        :raise: RuntimeError
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getBetaGamma(elemIdx)        

    def getOrbit(self, plane="X", elemIdx=None):
        """Get beam position at the end of an element if elemIdx is given, or beam orbit at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam position at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getOrbit(plane, elemIdx)

    def getTwissAlpha(self, plane="X", elemIdx=None):
        """Get beam twiss alpha parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss alpha at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getTwissAlpha(plane, elemIdx)

    def getTwissBeta(self, plane="X", elemIdx=None):
        """Get beam twiss beta parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getTwissBeta(plane, elemIdx)
        
    def getBeamRms(self, plane="X", elemIdx=None):
        """Get beam RMS parameters at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam twiss beta at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getBeamRms(plane, elemIdx)

    def getEmittance(self, plane="X", elemIdx=None):
        """Get beam normalized emittance (m-rad for transverse and degree-MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getEmittance(plane, elemIdx)
    
    def getBeamMomentumCentroid(self, plane="X", elemIdx=None):
        """Get beam centroid momentum (radian for transverse and MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getBeamMomentumCentroid(plane, elemIdx)
        
    def getMomentumRms(self, plane="X", elemIdx=None):
        """Get beam RMS momentum (radian for transverse and MeV for longitudinal)
        at the end of an element if elemIdx is given, or at all totalelements.
        Current implementation returns all position information from simulation, and does not separate BPM 
        from other devices like magnet and other diagnostic devices like profile monitor.

        :param plane:    beam plane, either "X", "Y", "Z", or "XY"
        :param elemIdx:  element index, `None` by default 
        
        :return: beam emittance at given location, or at all totalelements
        """
        if self.modelresult is None:
            self._buildModelResult()
        return self.modelresult.getMomentumRms(plane, elemIdx)    
