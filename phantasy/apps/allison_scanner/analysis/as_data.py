import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import matplotlib.patches as patches
import matplotlib.colors as colors
from scipy.linalg import svd
from scipy.optimize import nnls

class ASData(object):

    def __init__(self,
    scanner,
    I_grid,
    X_grid,
    V_grid,
    x_or_y = 'x',
    name = '', threshold_sigma = 2.,
    noise_gradient = False,
    correction = "None"):

        self.scanner = scanner
        self.x_or_y = x_or_y
        self.I_grid_raw = I_grid
        self.X_grid = X_grid
        self.V_grid = V_grid
        self.voltage_to_angle_conversion()

        self.name = name
        self.correction = correction

        # First iteration
        prelim_dict = self.prelim_noise( self.I_grid_raw )
        self.I_grid_in = self.in_out_ellipse(self.X_grid, self.Y_grid, self.I_grid_raw, prelim_dict = prelim_dict, how_many_sigma = 6)
        self.data_analysis(self.I_grid_in, threshold_sigma, show_results = False, noise_gradient = False)

        # Second iteration
        self.I_grid_in = self.in_out_ellipse(self.X_grid, self.Y_grid, self.I_grid_raw, prelim_dict = self.parameters_dict, how_many_sigma = 6)
        self.data_analysis(self.I_grid_in, threshold_sigma, show_results = False, noise_gradient = False)
        temporary_dict = self.parameters_dict.copy()

        ellipse_valid = 0
        sigma = 8

        while ellipse_valid != 1:

            self.I_grid_in = self.in_out_ellipse(self.X_grid, self.Y_grid, self.I_grid_raw, prelim_dict = temporary_dict, how_many_sigma = sigma)
#            self.noise_cutoff_plot(self.I_grid_in, threshold_sigma)
            self.data_analysis(self.I_grid_in, threshold_sigma, show_results = True, noise_gradient = noise_gradient, correction=self.correction)
            temporary_dict = self.parameters_dict.copy()

            ellipse_valid = int(input('Enter: 1 if ellipse area is okay, 2 if not'))

            if ellipse_valid != 1:
                sigma = float(input('Input new n where area = n*pi*emit_rms (previous n = %.2f)'%sigma))

#        self.output_data()
        self.save_plot()

    def voltage_to_angle_conversion(self):

        self.pos_count = len(self.X_grid[0])
        self.pos_step = np.abs(self.X_grid[1,1] - self.X_grid[0,0])
        self.vol_count = len(self.V_grid)
        self.vol_step = np.abs(self.V_grid[1,1] - self.V_grid[0,0])

        xp_results = np.array( [self.scanner.xp_from_V(i) for i in self.V_grid[:,0]] )

        self.y_array = xp_results[:,1]
        self.W_array = xp_results[:,3]

        self.Y_grid, _ = np.meshgrid(self.y_array, self.X_grid[0])
        self.Y_grid *= 1000
        self.Y_grid = self.Y_grid.T
        self.W_grid, _ = np.meshgrid(self.W_array, self.X_grid[0])
        self.W_grid = self.W_grid.T
        #self.Y_grid = np.tile( self.y_array, (self.pos_count, 1) )
        #self.Y_grid = self.Y_grid.transpose()*1000
        #self.W_grid = np.tile( self.W_array, (self.pos_count, 1) )
        #self.W_grid = self.W_grid.transpose()

        self.angle_step = np.abs( self.scanner.xp_from_V(self.vol_step)[1] )

        self.grid_to_res_ratio = (self.angle_step*self.pos_step/1000) / (self.scanner.dxp_conv*self.scanner.s)

    def data_analysis(self, I_grid_in, threshold_sigma, show_results = True, noise_gradient = False,
    correction = 'None'):

        if noise_gradient:
            self.noise_removal_with_gradient(I_grid_in, threshold_sigma)
        else:
            self.noise_removal_without_gradient(I_grid_in, threshold_sigma)

        if correction == 'None':
            self.data_analysis_no_correction()
        elif correction == 'Weight':
            self.data_analysis_weight_correction()
        elif correction == 'PhaseSpace':
            self.data_analysis_ps_correction(self.I_grid_no_noise, self.X_grid, self.Y_grid, self.V_grid)
        else:
            raise Exception('correction must be "None" or "Transmission" or "PhaseSpace"')

        if show_results:

            self.plot_output()

            print(self.x_or_y + '_cen = %s mm' %self.parameters_dict[self.x_or_y + 'cen'])
            print(self.x_or_y + 'p_cen = %s mrad' %self.parameters_dict[self.x_or_y + 'pcen'])
            print(self.x_or_y + '_rms = %s mm' %self.parameters_dict[self.x_or_y + 'rms'])
            print(self.x_or_y*2 + 'p = %s mm-mrad' %self.parameters_dict[self.x_or_y*2 + 'p'])
            print(self.x_or_y + 'p_rms = %s mrad' %self.parameters_dict[self.x_or_y + 'prms'])
            print(self.x_or_y + '_emit_normalized = %s mm-mrad' %self.parameters_dict[self.x_or_y + 'emitn'])
            print('alpha = %s ' %self.parameters_dict['alpha'])
            print('beta = %s m' %self.parameters_dict['beta'])
            print('gamma = %s 1/m' %self.parameters_dict['gamma'])
            print('total projected current = %s A' %self.parameters_dict['I_total'])

    def noise_removal_without_gradient(self, I_grid_in, threshold_sigma):

        self.no_noise = np.copy(I_grid_in)

        threshold = self.noise_avg + threshold_sigma*self.noise_sd

        for i in range(len(self.no_noise)):

            if self.no_noise[i]  == 0:
                pass
            elif self.no_noise[i] < threshold:
                self.no_noise[i] = 0
            else:
                self.no_noise[i] -= self.noise_avg

        self.I_grid_no_noise_prelim = self.no_noise.reshape(self.vol_count, self.pos_count)
        self.I_grid_no_noise = np.copy(self.I_grid_no_noise_prelim)

        iteration_end = False
        self.filter_iteration = 0

        while not iteration_end:
            I_grid_dummy = np.copy(self.I_grid_no_noise)
            self.I_grid_no_noise = self.island_filter(self.I_grid_no_noise, kernel_size = 3, threshold = threshold_sigma)
            self.filter_iteration += 1
            iteration_end = np.array_equal(I_grid_dummy, self.I_grid_no_noise)

    def noise_removal_with_gradient(self, I_grid_in, threshold_sigma):

        self.no_noise = np.copy(I_grid_in).reshape(self.vol_count, self.pos_count)

        self.row_noise_data = []

        for i in range(self.vol_count):
            row_noise = []

            for j in range(self.pos_count):
                if self.no_noise[i,j] == 0.:
                    row_noise.append(self.I_grid_raw[i,j])

            row_noise = np.array(row_noise)

            if len(row_noise) == 0:
                self.row_noise_data.append([0, 0, 0, 0, 0])
            else:

                row_noise_min = np.amin(row_noise)
                row_noise_max = np.amax(row_noise)
                row_noise_avg = np.mean(row_noise)
                row_noise_sd = np.std(row_noise)

                self.row_noise_data.append([len(row_noise), row_noise_max, row_noise_avg, row_noise_min, row_noise_sd])

        for i in range(self.vol_count):

            noise_param = []

            if self.row_noise_data[i][0] < 5:
                counter = 0
                while True:
                    if counter < i:
                        if self.row_noise_data[i-counter][0] < 4:
                            noise_param = self.row_noise_data[i-counter]
                            break
                    if counter < self.vol_count - i:
                        if self.row_noise_data[i+counter][0] < 4:
                            noise_param = self.row_noise_data[i+counter]
                            break
                    counter += 1
            else:
                noise_param = self.row_noise_data[i]

            threshold = noise_param[2] + threshold_sigma*noise_param[4]

#            print(self.no_noise[i])
#            print(threshold)

            for j in range(self.pos_count):
                if self.no_noise[i,j]  == 0.:
                    pass
                elif self.no_noise[i,j] < threshold:
                    self.no_noise[i,j] = 0.
                else:
                    self.no_noise[i,j] -= noise_param[2]

#            print(self.no_noise[i])

        self.I_grid_no_noise_prelim = self.no_noise.reshape(self.vol_count, self.pos_count)
        self.I_grid_no_noise = np.copy(self.I_grid_no_noise_prelim)

        iteration_end = False
        self.filter_iteration = 0

        while not iteration_end:
            I_grid_dummy = np.copy(self.I_grid_no_noise)
            self.I_grid_no_noise = self.island_filter(self.I_grid_no_noise, kernel_size = 3, threshold = threshold_sigma)
            self.filter_iteration += 1
            iteration_end = np.array_equal(I_grid_dummy, self.I_grid_no_noise)

    def data_analysis_no_correction(self):

        self.I_grid_adjusted = np.copy(self.I_grid_no_noise)*self.grid_to_res_ratio*2
        self.parameters_dict = self.calc_beam_parameters(self.X_grid, self.Y_grid, self.I_grid_adjusted)

    def data_analysis_weight_correction(self):

        self.I_grid_adjusted = np.copy(self.I_grid_no_noise)*self.grid_to_res_ratio/self.W_grid
        self.parameters_dict = self.calc_beam_parameters(self.X_grid, self.Y_grid, self.I_grid_adjusted)

    def data_analysis_ps_correction(self, I_grid, X_grid, Y_grid, V_grid, enforce_zero = True):

        j_grid = I_grid*0.
        coeff_matrix = self.coefficient_matrix(np.flipud(Y_grid[:,0]/1000), np.flipud(V_grid[:,0]))

        x_step = X_grid[1,1] - X_grid[0,0]
        y_step = np.abs(Y_grid[1,1] - Y_grid[0,0])

        for i in range(len(I_grid[0])):

            I_col = I_grid[:,i]

            if enforce_zero:
                coeff_matrix_reduced, include_index = self.enforce_zero(coeff_matrix, np.flipud(I_col))

                if np.sum(coeff_matrix_reduced) != 0.:
                    sol_nnls = nnls(coeff_matrix_reduced, np.flipud(I_col))

                    for j in range(len(include_index)):
                        j_grid[include_index[j], i] = sol_nnls[0][j]

                    j_grid[:,i] = np.flipud(j_grid[:,i])

            else:
                sol_nnls = nnls(coeff_matrix, np.flipud(I_col))
                j_grid[:,i] = np.flipud(sol_nnls[0])
#                j_grid[:,i] = np.flipud(np.linalg.solve(coeff_matrix, np.flipud(I_col)))

        self.I_grid_adjusted = j_grid*x_step*y_step*1e-6
        self.parameters_dict = self.calc_beam_parameters(self.X_grid, self.Y_grid, self.I_grid_adjusted)

#        return coeff_matrix, j_grid*x_step*y_step*1e-6

    def coefficient_matrix(self, Y_array, V_array):

        V_step = V_array[1] - V_array[0]
        Y_step = Y_array[1] - Y_array[0]

        m = len(V_array)

        coeff_matrix = np.zeros((m, m))

        for i in range(m):

            vol = V_array[i]
            y_ref = Y_array[i]
            y_lower = y_ref - Y_step/2.
            y_upper = y_ref + Y_step/2.

            xp_max, xp_ref, xp_min, W, ps_area = self.scanner.xp_from_V(vol)[:5]

            if y_lower < xp_min and y_upper > xp_max:
                coeff_matrix[i,i] = ps_area
            else:
                test_points = np.linspace(xp_min, xp_max, 1001)

                n_up = np.int((xp_max - xp_ref)/Y_step - 0.5) + 1
                n_down = np.int((xp_ref - xp_min)/Y_step - 0.5) + 1
                n = max(n_up, n_down)

                neighbor_coeff = np.zeros(1 + 2*n)

                y_min = y_lower - n*Y_step

                for xp in test_points:
                    T = self.scanner.T(xp, vol)
                    index = np.int((xp - y_min)/Y_step)
                    neighbor_coeff[index] += T

                neighbor_coeff = neighbor_coeff/np.sum(neighbor_coeff)*ps_area

                coeff_matrix[i,i] = neighbor_coeff[n]

                counter = 1
                while True:
                    try:
                        coeff_matrix[i,i+counter] = neighbor_coeff[n+counter]
                    except IndexError:
                        break
                    counter += 1

                counter = 1
                while True:
                    if i-counter > -1 and n-counter >-1:
                        coeff_matrix[i,i-counter] = neighbor_coeff[n-counter]
                    else:
                        break
                    counter += 1

        return coeff_matrix

    def enforce_zero(self, matrix_A, vector_b):

        include_index = list(range(len(matrix_A[0])))

        for i in range(len(vector_b)):
            if vector_b[i] == 0:
                for j in range(len(matrix_A[i])):
                    if matrix_A[i,j] != 0.:
                        try:
                            include_index.remove(j)
                        except ValueError:
                            pass

    #    return include_index

        matrix_A_reduced = np.zeros([len(matrix_A), len(include_index)])

        for i in range(len(include_index)):
            matrix_A_reduced[:,i] = matrix_A[:, include_index[i]]

        return matrix_A_reduced, include_index

    def in_out_polygon(self, X_grid, V_grid, raw_data, beam_polygon):

        counter = 0

        beam_polygon.append(beam_polygon[0])

        beam_polygon = mplPath.Path(np.array(beam_polygon))
        patch = patches.PathPatch(beam_polygon, edgecolor = 'red', lw=2, fill = False)

        for j in V_grid[:,0]:
            for i in X_grid[0,:]:

                if beam_polygon.contains_points([[i,j]])[0]:
                    region_in.append([i, j, raw_data[counter]])
                else:
                    region_in.append([i, j, 0])
                    region_out.append(raw_data[counter])

                region_full.append([i, j, raw_data[counter]])
                counter += 1

        if counter != len(raw_data):
            raise Exception('Not all columns are read')

        self.noise_max = np.amax(self.region_out)
        self.noise_avg = np.mean(self.region_out)
        self.noise_min = np.amin(self.region_out)
        self.noise_sd = np.std(self.region_out)

        return np.array(region_in)[:,2]

    def prelim_noise(self, I_grid, how_many_sigma = 5):

        noise = np.array([])
        noise = np.append(noise, I_grid[0:2, 0:2])
        noise = np.append(noise, I_grid[0:2, -2:])
        noise = np.append(noise, I_grid[-2:, 0:2])
        noise = np.append(noise, I_grid[-2:, -2:])

        noise_min = np.amin(noise)
        noise_max = np.amax(noise)
        noise_avg = np.mean(noise)
        noise_sd = np.std(noise)

        true_false_grid = I_grid >= noise_max + how_many_sigma*noise_sd

        I_grid = (I_grid - noise_avg)*true_false_grid

        prelim_dict = self.calc_beam_parameters(self.X_grid, self.Y_grid, I_grid)

        return prelim_dict

    def in_out_ellipse(self, X_grid, Y_grid, I_grid, prelim_dict, how_many_sigma):

#        how_many_sigma = how_many_sigma*np.pi
        raw_data = I_grid.flatten()

        counter = 0
        region_in = []
        region_out = []

        prelim_x = prelim_dict[self.x_or_y + 'cen']
        prelim_xp = prelim_dict[self.x_or_y + 'pcen']
        prelim_emit = prelim_dict[self.x_or_y + 'emit']
        prelim_alpha = prelim_dict['alpha']
        prelim_beta = prelim_dict['beta']
        prelim_gamma = prelim_dict['gamma']

        ellipse_matrix = np.array([[prelim_gamma, prelim_alpha],[prelim_alpha, prelim_beta]])
        eigen_values, eigen_vector_matrix = np.linalg.eig(ellipse_matrix)
        rotation_matrix = eigen_vector_matrix

###     empirical adjustment because ellipse from eigenvalues were found to be too elongated

        if eigen_values[0] > eigen_values[1]:
            eigen_values[0] /= 1.25
            eigen_values[1] *= 1.25
        else:
            eigen_values[1] /= 1.25
            eigen_values[0] *= 1.25

###     eigenvectors equal eigen_vector_matrix[:,0] and eigen_vector_matrix[:,1]

        self.circle_list = np.array([ [np.cos(theta), np.sin(theta)] for theta in np.linspace(0., 2*np.pi, 61) ])
        self.ellipse_u = np.array([[u0[0] * np.sqrt(np.pi*how_many_sigma*prelim_emit/eigen_values[0]),
                                    u0[1] * np.sqrt(np.pi*how_many_sigma*prelim_emit/eigen_values[1])] for u0 in self.circle_list])
        self.ellipse_x = np.array( [ np.dot( rotation_matrix , u) + np.array([prelim_x, prelim_xp])  for u in self.ellipse_u ] )

        for j in Y_grid[:,0]:
            for i in X_grid[0,:]:

                i_tilde = (i - prelim_x)
                j_tilde = (j - prelim_xp)

                i_new, j_new = np.dot( np.linalg.inv(rotation_matrix) , np.array([i_tilde,j_tilde]))

                if eigen_values[0]*i_new**2 + eigen_values[1]*j_new**2 <= np.pi*how_many_sigma*prelim_emit:
                    region_in.append([i, j, raw_data[counter]])

                    r = prelim_gamma*i_tilde**2 + prelim_alpha*2*i_tilde*j_tilde + prelim_beta*j_tilde**2
                    r_prime = eigen_values[0]*i_new**2 + eigen_values[1]*j_new**2

                else:
                    region_in.append([i, j, 0])
                    region_out.append(raw_data[counter])
                counter += 1

        if counter != len(raw_data):
            raise Exception('Not all columns are read')

        self.noise_max = np.amax(region_out)
        self.noise_avg = np.mean(region_out)
        self.noise_min = np.amin(region_out)
        self.noise_sd = np.std(region_out)

        return np.array(region_in)[:,2]

    def noise_cutoff_plot(self, I_grid_in, threshold_sigma):
        plt.hist(I_grid_in.flatten(), bins = 40)
        plt.axvline(x= self.noise_avg + threshold_sigma*self.noise_sd)
        plt.show()

    def island_filter(self, input_grid, kernel_size = 7, threshold = 2):

        if kernel_size != 3 and kernel_size != 5 and kernel_size != 7:
            raise Exception("kernel size not defined correctly")

        n = kernel_size//2

        dummy_grid = input_grid != 0
        binary_grid = input_grid*0.

        row, col = np.nonzero(input_grid)

        for i in range(len(col)):

            try:
                neighbor_sum = np.sum( dummy_grid[ row[i]-n : row[i]+n+1 , col[i]-n : col[i]+n+1 ] ) - 1
                if neighbor_sum >= threshold:
                    binary_grid[row[i], col[i]] = 1
            except IndexError:
                pass

        return binary_grid*input_grid

    def calc_beam_parameters_old(self, I_grid):

        I_total = np.sum(I_grid)
        x = np.sum(np.multiply(self.X_grid, I_grid)) / I_total
        xp = np.sum(np.multiply(self.Y_grid, I_grid)) / I_total

        xx = np.sum(np.multiply((self.X_grid -x)**2, I_grid)) / I_total
        xxp = np.sum( np.multiply( (self.Y_grid -xp), np.multiply((self.X_grid -x), I_grid)) ) / I_total
        xpxp = np.sum(np.multiply((self.Y_grid -xp)**2, I_grid)) / I_total

        x_rms = np.sqrt(xx)
        xp_rms = np.sqrt(xpxp)

        x_emit = np.sqrt(xx*xpxp - xxp**2)
        x_emit_n = x_emit*self.scanner.beta_c

        beta = xx/x_emit
        gamma = xpxp / x_emit
        alpha = -xxp / x_emit

#        return dict(x=x, xp=xp, x_rms = x_rms, xxp=xxp, xp_rms = xp_rms, x_emit=x_emit, x_emit_n = x_emit_n,
#                    alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)

        if self.x_or_y == 'x':
            return dict(xcen=x, xpcen=xp, xrms = x_rms, xxp=xxp, xprms = xp_rms, xemit=x_emit, xemitn = x_emit_n,
                        alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)
        else:
            return dict(ycen=x, ypcen=xp, yrms = x_rms, yyp=xxp, yprms = xp_rms, yemit=x_emit, yemitn = x_emit_n,
                        alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)

    def calc_beam_parameters(self, X_grid, Y_grid, I_grid):

        X_grid = np.copy(X_grid)
        Y_grid = np.copy(Y_grid)

        x_step = np.abs(X_grid[1,1] - X_grid[0,0])
        y_step = np.abs(Y_grid[1,1] - Y_grid[0,0])

        j_grid = I_grid / (x_step*y_step)
        I_total = np.sum(I_grid)

        x = np.sum(np.multiply(X_grid, I_grid)) / I_total
        xp = np.sum(np.multiply(Y_grid, I_grid)) / I_total

        X_grid -= x
        Y_grid -= xp

        X_grid_up = X_grid + x_step/2.
        X_grid_low = X_grid - x_step/2.
        Y_grid_up = Y_grid + y_step/2
        Y_grid_low = Y_grid - y_step/2.

        xx = np.abs( np.sum( y_step*(X_grid_up**3 - X_grid_low**3)/3.*j_grid ) )/ I_total
        xxp = np.sum( X_grid*Y_grid*I_grid ) / I_total
        xpxp = np.abs( np.sum( x_step*(Y_grid_up**3 - Y_grid_low**3)/3.*j_grid ) )/ I_total

        x_rms = np.sqrt(xx)
        xp_rms = np.sqrt(xpxp)

        x_emit = np.sqrt(xx*xpxp - xxp**2)
        x_emit_n = x_emit*self.scanner.beta_c

        beta = xx/x_emit
        gamma = xpxp / x_emit
        alpha = -xxp / x_emit

#        return dict(x=x, xp=xp, x_rms = x_rms, xxp=xxp, xp_rms = xp_rms, x_emit=x_emit, x_emit_n = x_emit_n,
#                    alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)

        if self.x_or_y == 'x':
            return dict(xcen=x, xpcen=xp, xrms = x_rms, xxp=xxp, xprms = xp_rms, xemit=x_emit, xemitn = x_emit_n,
                        alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)
        else:
            return dict(ycen=x, ypcen=xp, yrms = x_rms, yyp=xxp, yprms = xp_rms, yemit=x_emit, yemitn = x_emit_n,
                        alpha=alpha, beta=beta, gamma=gamma, I_total=I_total)

    def beam_param_no_noise(self):
        self.calc_beam_parameters(self.X_grid, self.Y_grid, self.I_grid_no_noise)



    def phase_space_plot(self, Y_grid, data_grid, ellipse = False, ellipse_coord = [], polygon = False, sign_contrast = False):

        fig = plt.figure(figsize = (7.5,4))
        ax = fig.add_subplot(111)
        pv_fig = self.phase_space_subplot(ax, Y_grid, data_grid, ellipse, ellipse_coord, polygon, sign_contrast)

        plt.gcf().subplots_adjust(bottom=0.15)
#        ax.set_facecolor((0.26700400000000002, 0.0048739999999999999, 0.32941500000000001))

        cbar = fig.colorbar(pv_fig)

        plt.show()

        return fig

    def phase_space_subplot(self, ax, Y_grid, data_grid, ellipse = False, ellipse_coord = [], polygon = False, sign_contrast = False):

        if sign_contrast:
            data_grid = (data_grid > 0).astype(int)

        pv_fig = ax.pcolormesh(self.X_grid, Y_grid, data_grid, cmap=plt.get_cmap('jet'))
#        pv_fig = ax.pcolormesh(self.X_grid, Y_grid, data_grid, norm=colors.LogNorm())
        ax.set_xlabel(self.x_or_y + ' [mm]')
        ax.set_ylabel(self.x_or_y + "' [mrad]")

#        ax.set_facecolor((0.26700400000000002, 0.0048739999999999999, 0.32941500000000001))
        if ellipse:
            ax.plot(ellipse_coord[:,0], ellipse_coord[:,1], color='r', linewidth=2.0)
        if polygon:
            ax.add_patch(self.patch)

        return pv_fig

    def results_plot(self, centroid = True, projection = True, rms_ellipse = True, text_in = True, text_out=True, normalize = True):

        X_grid_rectified, Y_grid_rectified, I_grid_rectified = self.pcolormesh_remedy(self.X_grid, self.Y_grid, self.I_grid_adjusted)

        if normalize:
            I_grid_rectified = I_grid_rectified /np.sum(I_grid_rectified) * 100

        fig = plt.figure(figsize = (7.5,5))
        ax = plt.subplot(111)
        pv_fig = ax.pcolormesh(X_grid_rectified, Y_grid_rectified, I_grid_rectified, cmap=plt.get_cmap('jet'))

        ax.set_xlabel(self.x_or_y + ' [mm]')
        ax.set_ylabel(self.x_or_y + "' [mrad]")

        plt.gcf().subplots_adjust(bottom=0.15)
        cbar = fig.colorbar(pv_fig)

        if normalize:
            cbar.ax.set_title('beam %')

        ax.set_xlim(X_grid_rectified[0,0], X_grid_rectified[-1,-1])
        ax.set_ylim(Y_grid_rectified[-1,-1], Y_grid_rectified[0,0])

        if centroid:
            ax.axvline(self.parameters_dict[self.x_or_y + 'cen'], linestyle='--', lw=1., color='w')
            ax.axhline(self.parameters_dict[self.x_or_y + 'pcen'], linestyle='--', lw=1., color='w')

        if rms_ellipse:

            prelim_x = self.parameters_dict[self.x_or_y + 'cen']
            prelim_xp = self.parameters_dict[self.x_or_y + 'pcen']
            prelim_gamma = self.parameters_dict['gamma']
            prelim_alpha = self.parameters_dict['alpha']
            prelim_beta = self.parameters_dict['beta']
            prelim_emit = self.parameters_dict[self.x_or_y + 'emit']

            ellipse_matrix = np.array([[prelim_gamma, prelim_alpha],[prelim_alpha, prelim_beta]])
            eigen_values, eigen_vector_matrix = np.linalg.eig(ellipse_matrix)
            rotation_matrix = eigen_vector_matrix

            circle_list = np.array([ [np.cos(theta), np.sin(theta)] for theta in np.linspace(0., 2*np.pi, 601) ])
            ellipse_u = np.array([[u0[0]*np.sqrt(4 * prelim_emit/eigen_values[0]),
                                   u0[1]*np.sqrt(4 * prelim_emit/eigen_values[1])] for u0 in circle_list])
            ellipse_x = np.array( [ np.dot( rotation_matrix , u) + np.array([prelim_x, prelim_xp])  for u in ellipse_u ] )

            ax.scatter(ellipse_x[:,0], ellipse_x[:,1], s=0.2, color='w')

        if projection:

            x_list = X_grid_rectified[0]
            y_list = Y_grid_rectified[:,0]

            x_max = np.amax(x_list)
            x_min = np.amin(x_list)
            y_max = np.amax(y_list)
            y_min = np.amin(y_list)

            a = np.array([np.sum(I_grid_rectified[:,i]) for i in range(len(x_list))])
            b = np.array([np.sum(I_grid_rectified[i]) for i in range(len(y_list))])

            a = a/np.amax(a) *(y_max-y_min)/5. + y_min
            b = b/np.amax(b) *(x_max-x_min)/5. + x_min

            ax.step(x_list[1:], a[:-1], lw=1., color='y')
            ax.step(b[:-1], y_list[1:], lw=1., color='y')

        if text_out:
            x_pos = x_max + (x_max-x_min)/4.
            y_pos = [y_max - (i+1)*(y_max-y_min)/10. for i in range(10)]
            ax.text(x_pos, y_pos[0], self.x_or_y + 'cen = %.2f mm' %self.parameters_dict[self.x_or_y + 'cen'], fontsize=12)
            ax.text(x_pos, y_pos[1], self.x_or_y + 'pcen = %.2f mrad' %self.parameters_dict[self.x_or_y + 'pcen'], fontsize=12)
            ax.text(x_pos, y_pos[2], self.x_or_y + 'rms = %.2f mm' %self.parameters_dict[self.x_or_y + 'rms'], fontsize=12)
            ax.text(x_pos, y_pos[3], self.x_or_y + 'prms = %.2f mrad' %self.parameters_dict[self.x_or_y + 'prms'], fontsize=12)
            ax.text(x_pos, y_pos[4], self.x_or_y + 'emitn = %.4f mm-mrad' %self.parameters_dict[self.x_or_y + 'emitn'], fontsize=12)
            ax.text(x_pos, y_pos[5], self.x_or_y + '_alpha = %.2f ' %self.parameters_dict['alpha'], fontsize=12)
            ax.text(x_pos, y_pos[6], self.x_or_y + '_beta = %.2f m' %self.parameters_dict['beta'], fontsize=12)
            ax.text(x_pos, y_pos[7], self.x_or_y + '_gamma = %.2f /m' %self.parameters_dict['gamma'], fontsize=12)

            ax.text(x_pos, y_max, self.name, fontsize=12)

        if text_in:
            y_pos = [y_max - (i+1)/2.*(y_max-y_min)/8. for i in range(3)]
            if self.parameters_dict['alpha'] < 0:
                x_pos = x_min + 0.5*(x_max-x_min)/10.
            else:
                x_pos = x_min + 5.5*(x_max-x_min)/10.

            ax.text(x_pos, y_pos[0], r'$\epsilon_{%s}$ =  %.4f mm-mrad' %(self.x_or_y, self.parameters_dict[self.x_or_y + 'emitn']), fontsize=12, color='w')
            ax.text(x_pos, y_pos[1], r'$\alpha_{%s}$ = %.2f ' %(self.x_or_y, self.parameters_dict['alpha']), fontsize=12, color='w')
            ax.text(x_pos, y_pos[2], r'$\beta_{%s}$ = %.2f m' %(self.x_or_y, self.parameters_dict['beta']), fontsize=12, color='w')


        plt.show()

        return fig

    def plot_raw(self, polygon = False, sign_contrast = False):
        return self.phase_space_plot(self.V_grid, np.copy(self.I_grid_raw), ellipse = ellipse, ellipse_coord = self.ellipse_x, polygon = polygon, sign_contrast = sign_contrast)

    def plot_no_noise_prelim(self, ellipse = False, polygon = False, sign_contrast = False):
        return self.phase_space_plot(self.V_grid, np.copy(self.I_grid_no_noise_prelim), ellipse = ellipse, ellipse_coord = self.ellipse_x, polygon = polygon, sign_contrast = sign_contrast)

    def plot_no_noise(self, ellipse = False, polygon = False, sign_contrast = False):
        return self.phase_space_plot(self.V_grid, np.copy(self.I_grid_no_noise), ellipse = ellipse, ellipse_coord = self.ellipse_x, polygon = polygon, sign_contrast = sign_contrast)

    def plot_adjusted(self, ellipse = False, polygon = False, sign_contrast = False):
        return self.phase_space_plot(self.Y_grid, np.copy(self.I_grid_adjusted), ellipse = ellipse, ellipse_coord = self.ellipse_x, polygon = polygon, sign_contrast = sign_contrast)

    def noise_data(self):
        return (self.noise_max, self.noise_avg, self.noise_min, self.noise_sd)

    def noise_histogram(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(self.region_out, 20)
        ax.axvline(x = self.noise_avg, color = 'k')
        ax.axvline(x = self.noise_avg + self.noise_sd, color = 'r')
        ax.axvline(x = self.noise_avg - self.noise_sd, color = 'r')
        ax.axvline(x = self.noise_avg + 2*self.noise_sd, color = 'g')
        ax.axvline(x = self.noise_avg - 2*self.noise_sd, color = 'g')

        return fig

    def plot_output(self, ellipse_or_polygon = 'ellipse'):
        if ellipse_or_polygon == 'ellipse':
            fig = self.plot_adjusted(sign_contrast = True, ellipse = True, polygon = False)#sign_contrast = True)
#            fig.savefig(self.name + '_no_noise.png',format='png', dpi=400)
        elif ellipse_or_polygon == 'polygon':
            fig = self.plot_adjusted(sign_contrast = True, ellipse = False, polygon = True)#sign_contrast = True)
#            fig.savefig(self.name + '_no_noise.png',format='png', dpi=400)
        else:
            raise Exception('ellipse_or_polygon not defined')
        fig = self.plot_adjusted()
#        fig.savefig(self.name + '_adjusted.png',format='png', dpi=400)

    def pcolormesh_remedy(self, X_grid, Y_grid, I_grid):

        x_max = np.amax(X_grid)
        x_step = X_grid[1,1]-X_grid[0,0]

        X_grid_rectified = X_grid - x_step/2.
        X_grid_rectified = np.insert(X_grid_rectified, self.pos_count, x_max + x_step/2., axis=1)
        X_grid_rectified = np.insert(X_grid_rectified, self.vol_count, 0, axis=0)
        X_grid_rectified[-1] = X_grid_rectified[0]

        y_min = np.amin(Y_grid)
        y_step = Y_grid[1,1]-Y_grid[0,0]

        Y_grid_rectified = Y_grid - y_step/2.
        Y_grid_rectified = np.insert(Y_grid_rectified, self.pos_count, 0, axis=1)
        Y_grid_rectified[:,-1] = Y_grid_rectified[:,0]
        Y_grid_rectified = np.insert(Y_grid_rectified, self.vol_count, y_min - y_step/2., axis=0)

        I_grid_rectified = I_grid
        I_grid_rectified = np.insert(I_grid_rectified, self.pos_count, 0, axis=1)
        I_grid_rectified = np.insert(I_grid_rectified, self.vol_count, 0, axis=0)

        return X_grid_rectified, Y_grid_rectified, I_grid_rectified

    def save_plot(self):
        fig = self.results_plot()
        fig.savefig( self.name + '_Plot.png', format='png', dpi=400, bbox_inches='tight')

    def return_parameters(self):
        return [self.x, self.xp, self.xx,
        self.xxp, self.xpxp, self.x_emit*self.scanner.beta_c,
        self.alpha, self.beta, self.gamma, self.total_I]
