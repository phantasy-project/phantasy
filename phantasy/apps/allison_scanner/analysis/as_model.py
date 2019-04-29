import numpy as np
import matplotlib.pyplot as plt

class ASModel(object):

    def __init__(self, L, g, l1, l2, s, d,
                 A_ion = 39.948, Q_ion = 9, KE_per_u = 12e3):
        self.L = L/1000.
        self.g = g/1000.
        self.l1 = l1/1000.
        self.l2 = l2/1000.
        self.s = s/1000.
        self.d = d/1000.

        self.L_interslit = self.L + self.l1 + self.l2

        self.A_ion = A_ion
        self.Q_ion = Q_ion
        self.KE_per_u = KE_per_u

        self.geometric_factor = (self.L + 2*self.l2) / (self.L_interslit)
        self.prefactor1 = (self.L + 2*self.l1)/(self.L + 2*self.l2)
        self.prefactor2 = self.d*2*(self.l2-self.l1) /self.L_interslit/(self.L_interslit + 2*self.d)

        self.dxp_conv = 2*self.s/self.L_interslit
        self.gamma_c = 1. + self.KE_per_u/931.4940954/1e6
        self.beta_c = np.sqrt(1 - self.gamma_c**-2)

    def xp_from_V(self,V0):

        xp_conv = 0.5*(self.Q_ion*np.abs(V0))/(self.A_ion*self.KE_per_u)*self.L/self.g

        xp_ref = xp_conv*self.geometric_factor
        xp_max = xp_ref + (self.s - xp_ref*self.d)/(self.L_interslit + self.d)
        xp_min = xp_ref - (self.s - self.prefactor1*xp_ref*self.d)/(self.L_interslit + self.d)

        norm_area = self.dxp_conv*self.s

        if self.l1 == self.l2 or self.d == 0:
            xp_tilde = xp_ref
            W = 0.5*(1. - xp_ref*self.d/self.s)**2
            ps_area = norm_area*W
        else:
            xp_shift = xp_conv*self.prefactor2
            xp_tilde = xp_ref - xp_shift

            xp_min_to_xp_tilde = (self.s - xp_tilde*self.d)/(self.L_interslit + self.d)
            xp_ref_to_xp_max = (self.s - xp_ref*self.d)/(self.L_interslit + self.d)

            area1 = xp_min_to_xp_tilde  * (self.s - xp_tilde*self.d) / 2.
            area2 = xp_shift * (self.s - xp_tilde*self.d + self.s - xp_ref*self.d) / 2.
            area3 = xp_ref_to_xp_max * (self.s - xp_ref*self.d) / 2.

            ps_area = area1 + area2 + area3

            W = ps_area/norm_area

        if V0 >= 0.:
            return (xp_max, xp_ref, xp_min, W, ps_area, xp_tilde)
        else:
            return (-xp_min, -xp_ref, -xp_max, W, ps_area, -xp_tilde)

    def V_from_xp(self,xp):
        return xp/0.5/self.Q_ion*(self.A_ion*self.KE_per_u)/self.L*self.g/self.geometric_factor

    def test_transmit_ideal(self, x, xp, V0):

        x_0 = x
        xp_0 = xp

        if abs(x_0) > self.s/2.:
    #        print(x_0)
    #        print('rejected x = 0')
            return False

        x_d = x_0 + xp_0*self.d
        xp_d = xp_0

        if abs(x_d) > self.s/2.:
    #        print(x_d)
    #        print('rejected x = d')
            return False

        x_l1 = x_d + xp_d*self.l1
        xp_l1 = xp_d

        x_L = x_l1 + xp_l1*self.L - (self.Q_ion*V0)/(self.A_ion*self.KE_per_u)/self.g*0.5*self.L**2
        xp_L = xp_l1 - (self.Q_ion*V0)/(self.A_ion*self.KE_per_u)*self.L/self.g

        x_l2 = x_L + xp_L*self.l2
        xp_l2 = xp_L

        if abs(x_l2) > self.s/2.:
    #        print('rejected x = l2')
            return False

        x_f = x_l2 + xp_l2*self.d
        xp_f = xp_l2

        if abs(x_f) > self.s/2.:
    #        print('rejected x = x_f')
            return False
        else:
            return True

    def T(self, xp, V0):
        xp_max, xp_ref, xp_min, W, ps_area, xp_tilde = self.xp_from_V(V0)

        c1 = (1 - xp_ref*self.d/self.s)
        c2 = (1 - xp_tilde*self.d/self.s)

        if xp <= xp_min or xp >= xp_max:
            return 0
        elif xp_min < xp <= xp_tilde:
            return (xp - xp_min)/(xp_tilde - xp_min) * c2
        elif xp_tilde < xp <= xp_ref:
            return ((xp - xp_tilde)*c1 + (xp_ref - xp)*c2)/(xp_ref - xp_tilde)
        else:
            return (xp_max - xp) / (xp_max - xp_ref) * c1

class FribASModel(ASModel):

    def __init__(self, beamline, A_ion = 39.948, Q_ion = 9, KE_per_u = 12e3):
        if beamline == 'artemis':
            ASModel.__init__(self, L = 71.85, g = 7.91, l1 = 4.938, l2 = 4.986,
                                    s = 0.06, d = 0.254,
                                    A_ion = A_ion, Q_ion = Q_ion, KE_per_u = KE_per_u)
        elif beamline == 'venus':
            raise Exception('Venus scanner not yet installed')
        else:
            raise Exception('FRIB AS scanner must equal "artemis" or "venus"')
