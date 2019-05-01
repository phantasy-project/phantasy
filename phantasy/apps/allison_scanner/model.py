#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# rest energy [eV/u]
ION_ES = 931.49432e+06  # rest energy [eV/u]


class Model(object):
    """ Data model for allison scanner analysis.

    Parameters
    ----------
    device : Device
        Allison-Scanner device.
    ion_charge : float
        Ion charge, Q.
    ion_mass : int
        Ion mass, A.
    ion_energy : float
        Ion kinetic energy, K, [eV/u]
    """
    # Q: FE_ISRC1:BEAM:Q_BOOK
    # A: FE_ISRC1:BEAM:A_BOOK
    # V: FE_SCS1:BEAM:HV_BOOK
    # K: V * Q / A
    def __init__(self, device, ion_charge=9, ion_mass=39.948,
                 ion_energy=12e3):
        self.device = device
        self.ion_charge = ion_charge
        self.ion_mass = ion_mass
        self.ion_energy = ion_energy

    @property
    def charge_mass_ratio(self):
        return self.ion_charge / self.ion_mass

    @property
    def bg(self):
        gamma = 1 + self.ion_energy / ION_ES
        beta = (1 - 1/gamma ** 2) ** 0.5
        return beta * gamma

    @property
    def device(self):
        """Device : Abstracted allison-scanner device."""
        return self._device

    @device.setter
    def device(self, o):
        self._device = o

    @property
    def ion_charge(self):
        """float : Ion charge notated as Q."""
        return self._ion_charge

    @ion_charge.setter
    def ion_charge(self, x):
        self._ion_charge = x

    @property
    def ion_mass(self):
        """float : Ion mass notated as A."""
        return self._ion_mass

    @ion_mass.setter
    def ion_mass(self, x):
        self._ion_mass = x

    @property
    def ion_energy(self):
        """float : Ion kinetic energy notated as K, [eV/u]."""
        return self._ion_energy

    @ion_energy.setter
    def ion_energy(self, x):
        self._ion_energy = x

    def voltage_to_divergence(self, voltage):
        """Convert input voltage into divergence.

        Parameters
        ----------
        voltage : float
            Voltage value in [V].

        Returns
        -------
        r : tuple
            (xp_max, xp_ref, xp_min, w, ps_area, xp_tilde)
        """
        device = self.device
        xp_conv = 0.5 * self.charge_mass_ratio * abs(voltage) \
                / self.ion_energy * device.length / device.gap
        xp_ref = xp_conv * device.geometric_factor

        s, d = device.slit_width, device.slit_thickness
        g = device.gap
        l1, l2 = device.length1, device.length2
        l_total = device.length + l1 + l2

        xp_max = xp_ref + (s - xp_ref * d) / (l_total + d)
        xp_min = xp_ref - (s - self.device.prefactor1 * xp_ref * d) / (l_total + d)

        norm_area = self.device.dxp0 * s

        if l1 == l2 or d == 0:
            xp_tilde = xp_ref
            w = 0.5 * (1.0 - xp_ref * d / s) ** 2
            ps_area = norm_area * w
        else:
            xp_shift = xp_conv * self.device.prefactor2
            xp_tilde = xp_ref - xp_shift

            xp_min_to_xp_tilde = (s - xp_tilde * d) / (l_total + d)
            xp_ref_to_xp_max = (s - xp_ref * d) / (l_total + d)

            area1 = xp_min_to_xp_tilde * (s - xp_tilde * d) / 2.0
            area2 = xp_shift * (s - xp_tilde * d + s - xp_ref * d) / 2.0
            area3 = xp_ref_to_xp_max * (s - xp_ref * d) / 2.0
            ps_area = area1 + area2 + area3
            w = ps_area / norm_area

        if voltage >= 0:
            return xp_max, xp_ref, xp_min, w, ps_area, xp_tilde
        else:
            return -xp_min, -xp_ref, -xp_max, w, ps_area, -xp_tilde
