#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Data fitting module.

.. Tong Zhang <zhangt@frib.msu.edu>
.. 2017-04-03 15:25:36 PM EDT
"""

import lmfit
import numpy as np


class FitModel(object):
    """Data fitting model:

    - *gaussuan*: :math:`a exp(-(x-x_0)^2/2/x_{std}^2) + y_0`
    - *polynomial*: :math:`\Sigma_{i=0}^n x^i a_i`
    - *power*: :math:`a x ^ b`
    - *sin*: :math:`a \sin(b x + c) + d`

    Parameters
    ----------
    model : str
        Name of fitting model, 'gaussian' by default.
    params :
        Initial fitting parameters.

    Keyword Arguments
    -----------------
    x : array
        Data to fit, *x* array.
    y : array
        Data to fit, *y* array.
    n : int
        Highest order for polynomial fit model.
    xmin : float
        Lower limit of fitting data range.
    xmax : float
        Upper limit of fitting data range.
    """

    def __init__(self, model='gaussian', params=None, **kws):
        if params is None:
            params = lmfit.Parameters()
        self._model = model
        self._params = params
        try:
            self._x, self._y = kws['x'], kws['y']
        except:
            self._x, self._y = [], []
        try:
            self.n = kws['n']
        except:
            self.n = 1  # when model is polynomial, highest order
        self.n += 1  # range(n + 1): [0, n]

        # data fitting window
        self.x_fit_min, self.x_fit_max = kws.get('xmin'), kws.get('xmax')

        # fitting method
        self._method = 'leastsq'

        self._set_params_func = {
            'gaussian': self._set_params_gaussian,
            'polynomial': self._set_params_polynomial,
        }
        self._fitfunc = {
            'gaussian': self._fit_gaussian,
            'polynomial': self._fit_polynomial,
        }
        self._gen_func_text = {
            'gaussian': self._gen_func_text_gaussian,
            'polynomial': self._gen_func_text_polynomial,
        }

        self._fit_result = None

    @property
    def model(self):
        """str: Fitting model name, *gaussian* by default.

        Available options:
        - *gaussian*
        """
        return self._model

    @model.setter
    def mode(self, model):
        self._model = model

    @property
    def method(self):
        """str: Fitting method name, *leastsq* by default.

        Available options:

        - *leastsq*: Levenberg-Marquardt
        - *least_squares*: Least-Squares minimization, using Trust Region
          Reflective method by default
        - *differential_evolution*: differential evolution
        - *brute*: brute force method
        - *nelder*: Nelder-Mead
        - *lbfgsb*: L-BFGS-B
        - *powell*: Powell
        - *cg*: Conjugate-Gradient
        - *newton*: Newton-Congugate-Gradient
        - *cobyla*: Cobyla
        - *tnc*: Truncate Newton
        - *trust-ncg*: Trust Newton-Congugate-Gradient
        - *dogleg*: Dogleg
        - *slsqp*: Sequential Linear Squares Programming
        """
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    def _fit_gaussian(self, p, x):
        a = p['a'].value
        x0 = p['x0'].value
        y0 = p['y0'].value
        xstd = p['xstd'].value
        return a * np.exp(-(x - x0) ** 2.0 / 2.0 / xstd / xstd) + y0

    def _fit_polynomial(self, p, x):
        f = 0
        for i in range(self.n):
            f += p['a' + str(i)].value * x ** i
        return f

    def _errfunc(self, p, f, x, y):
        return f(p, x) - y

    def set_data(self, data=None, x=None, y=None):
        """Set raw data to fit, prefer *data* parameter.

        Parameters
        ----------
        data : Array
            Holds x and y data, shape should be ``(n,2)``.
        x : Array
            X data array.
        y : Array
            Y data array.
        """
        if data is not None:
            self._x, self._y = data[:, 0], data[:, 1]
        else:
            if x is not None:
                self._x = x
            if y is not None:
                self._y = y

    def get_data(self):
        """Return raw data, tuple of array x and y.
        """
        return self._x, self._y

    # def _set_fitfunc(self, type=None):
    #    """Type: gaussian, linear, quadratic, polynomial, power, sin
    #    """
    #    if type is not None:
    #        self._model = type

    def _gen_func_text_gaussian(self, p0):
        a = p0['a'].value
        x0 = p0['x0'].value
        y0 = p0['y0'].value
        xstd = p0['xstd'].value
        retfun = '$f(x) = a e^{-\\frac{(x-x_0)^2}{2\sigma_x^2}}+y_0$'
        retcoe = '$a = %.3f, x_0 = %.3f, \sigma_x = %.3f, y_0 = %.3f$' % (a, x0, xstd, y0)
        return {'func': retfun, 'fcoef': retcoe}

    def _gen_func_text_polynomial(self, p0):
        retfun = '$f(x) = \sum_{i=0}^{%s}\,a_i x^i$' % (self.n)
        retcoe = ','.join(['$a_{%d} = %.3f$' % (i, p0['a' + str(i)].value) for i in range(self.n)])
        return {'func': retfun, 'fcoef': retcoe}

    def set_params(self, **p0):
        """Set fitting parameters.

        Parameters
        ----------
        p0 : dict
            Initial fitting parameters.
        """
        self._set_params_func[self._model](p0)

    def _set_params_gaussian(self, p0):
        self._params.add('a', value=p0['a'])
        self._params.add('x0', value=p0['x0'])
        self._params.add('y0', value=p0['y0'])
        self._params.add('xstd', value=p0['xstd'])

    def _set_params_polynomial(self, p0):
        for i in range(self.n):
            pi_name = 'a' + str(i)
            self._params.add(pi_name, value=p0[pi_name])

    def get_fitfunc(self, p0=None):
        """Get fitting function.

        Parameters
        ----------
        p0 : dict
            Fitting parameters.

        Returns
        -------
        ret : tuple
            Tuple of fitting function and text label for plotting.
        """
        if p0 is None:
            p0 = self._fit_result.params
        f_func = self._fitfunc[self._model]
        gen_func = self._gen_func_text[self._model]
        f_text = gen_func(p0)
        return f_func, f_text

    def get_fit_result(self):
        """Return fitting results.
        """
        return self._fit_result

    def fit(self):
        """Do data fittig.
        """
        p = self._params
        f = self._fitfunc[self._model]
        x, y = self._x, self._y

        xmin = self.x_fit_min if self.x_fit_min is not None else x.min()
        xmax = self.x_fit_max if self.x_fit_max is not None else x.max()

        x_fit, idx = FitModel.get_range(x, xmin, xmax)
        y_fit = y[idx]

        m = self._method
        res = lmfit.minimize(self._errfunc, p, method=m, args=(f, x_fit, y_fit))
        self._fit_result = res
        return res

    def fit_report(self):
        """Generate fitting report.
        """
        # gaussian model
        if self._model == 'gaussian':
            if self._fit_result is not None:
                p = self._fit_result.params
                retstr1 = "Fitting Function:" + "\n"
                retstr2 = "a*exp(-(x-x0)^2/2/sx^2)+y0" + "\n"
                retstr3 = "Fitting Output:" + "\n"
                retstr4 = "{a0_k:<3s}: {a0_v:>10.4f}\n".format(a0_k='a', a0_v=p['a'].value)
                retstr5 = "{x0_k:<3s}: {x0_v:>10.4f}\n".format(x0_k='x0', x0_v=p['x0'].value)
                retstr6 = "{sx_k:<3s}: {sx_v:>10.4f}\n".format(sx_k='sx', sx_v=p['xstd'].value)
                retstr7 = "{y0_k:<3s}: {y0_v:>10.4f}".format(y0_k='y0', y0_v=p['y0'].value)
                return retstr1 + retstr2 + retstr3 + retstr4 + retstr5 + retstr6 + retstr7
            else:
                return "Nothing to report."
        elif self._model == 'polynomial':
            if self._fit_result is not None:
                p = self._fit_result.params
                retstr = "Fitting Function:" + "\n"
                fstr = '+'.join(['a' + str(i) + '*x^' + str(i) for i in range(self.n)])
                fstr = fstr.replace('*x^0', '')
                fstr = fstr.replace('x^1', 'x')
                retstr += fstr + '\n'
                retstr += "Fitting Output:" + "\n"
                for i in range(self.n):
                    ki = 'a' + str(i)
                    retstr += "{k:<3s}: {v:>10.4f}\n".format(k=ki, v=p[ki].value)
                return retstr
            else:
                return "Nothing to report."

    def calc_p0(self):
        """Return p0 from input x, y.
        """
        if self._model == 'gaussian':
            x, xdata = self._x, self._y
            x0 = np.sum(x * xdata) / np.sum(xdata)
            p0 = {'a': xdata.max(),
                  'x0': x0,
                  'xstd': (np.sum((x - x0) ** 2 * xdata) / np.sum(xdata)) ** 0.5,
                  'y0': 0,
                  }
        elif self._model == 'polynomial':
            p0 = {'a' + str(i): 1 for i in range(self.n)}
        return p0

    @staticmethod
    def get_range(x, xmin, xmax):
        """Find array range.

        Parameters
        ----------
        x : array
            Orignal numpy 1D array.
        xmin : float
            Min of x range.
        xmax : float
            Max of x range.

        Returns
        -------
        ret : tuple
            Sub-array and indice in original array.
        """
        if xmin >= xmax:
            return x, np.arange(x.size)
        idx1, idx2 = np.where(x > xmin), np.where(x < xmax)
        idx = np.intersect1d(idx1, idx2)
        return x[idx], idx


def gaussian_fit(x, xdata):
    """Return fit function and :math:`x_0`, :math:`\sigma_x` for gaussian fit.

    Parameters
    ----------
    x : array
        Data to fit, x col.
    xdata : array
        Data to fit, y col.

    Returns
    -------
    ret : tuple
        Tuple of fitting function, x0 and xstd.
    """
    fm = FitModel()
    x0 = np.sum(x * xdata) / np.sum(xdata)
    p0 = {'a': xdata.max(),
          'x0': x0,
          'xstd': (np.sum((x - x0) ** 2 * xdata) / np.sum(xdata)) ** 0.5,
          'y0': 0
          }
    fm.set_data(x=x, y=xdata)
    fm.set_params(**p0)
    res = fm.fit()
    x0, xstd = [res.params[k].value for k in ('x0', 'xstd')]

    def fit_func(x):
        return fm.get_fitfunc(res.params)[0](res.params, x)

    return fit_func, x0, xstd
