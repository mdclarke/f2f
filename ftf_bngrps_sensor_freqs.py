# -*- coding: utf-8 -*-

import os.path as op
import mne
import numpy as np
from scipy import stats


# High SES group
subjects = {'high':  ['f2f_009_01_OTP', 'f2f_011_01_OTP', 'f2f_012_01_OTP',
                      'f2f_022_01_OTP', 'f2f_024_01_OTP', 'f2f_025_01_OTP',
                      'f2f_028_01_OTP', 'f2f_034_01_OTP', 'f2f_036_01_OTP',
                      'f2f_037_01_OTP', 'f2f_103_01_OTP', 'f2f_104_01_OTP',
                      'f2f_106_01_OTP'],
            'low': ['f2f_010_01_OTP', 'f2f_013_01_OTP', 'f2f_014_01_OTP',
                    'f2f_015_01_OTP', 'f2f_018_01_OTP', 'f2f_021_01_OTP',
                    'f2f_026_01_OTP', 'f2f_027_01_OTP', 'f2f_102_01_OTP', ]}

data_path = '/storage/Maggie/f2f/psds'
conditions = ['talk', 'ignore']
bands = [(4, 8), (13, 28), (29, 50)]
band_names = ['theta', 'beta', 'gamma']
use_this = mne.read_evokeds(op.join(data_path,
                                    'f2f_009_01_OTP_psd-ave.fif'))[0]
picks = mne.pick_types(use_this.info, meg='planar1')
ch_names = [use_this.ch_names[k] for k in picks]
times = use_this.times

# Get data of interest
N = max(len(l) for l in subjects.values())
for jj, band in enumerate(bands):
    for ii, cond in enumerate(conditions):
        for kk, grp in enumerate(subjects.keys()):
            subj = subjects[grp]
            for si, sub in enumerate(subj):
                if (cond == conditions[0] and grp == subjects.keys()[0] and
                        sub == subj[0] and band == bands[0]):
                    frq_data = np.ones((len(bands), len(conditions),
                                        len(subjects), N,
                                        len(picks),
                                        use_this.data.shape[1])) * np.nan
                ev = mne.read_evokeds(op.join(data_path,
                                              '%s_psd-ave.fif' % sub),
                                      condition=cond)
                ev.pick_types(meg='planar1')
                # bands(jj) X conds(ii) X groups(kk) X subj(si) X chs X frqs
                frq_data[jj, ii, kk, si] = ev.data
# T-test
for jj, band in enumerate(bands):
    mask = np.logical_and(band[0] <= times, times <= band[1])
    I, J, K = np.ix_(np.arange(N), np.arange(len(picks)), mask)
    for ii, cond in enumerate(conditions):
        # per group mean of frqs in contrast for each band
        A = np.mean(frq_data[jj, ii, 0, I, J, K], axis=2)  # high ses
        B = np.mean(frq_data[jj, ii, 1, I, J, K], axis=2)
        T0, p_values = stats.ttest_ind(A, B, axis=0, equal_var=True,
                                       nan_policy='omit')
        neg_p_sign_t = -np.log10(p_values) * np.sign(T0)
        evoked = mne.EvokedArray(neg_p_sign_t[:, np.newaxis],
                                 use_this.pick_types(meg='planar1').info)
        show = picks[np.abs(neg_p_sign_t) >= 1]
        title = band_names[jj] + '/' + conditions[ii]
        fig = evoked.plot_topomap(ch_type='planar1', times=[0], scale=1,
                                  time_format=None, cmap='RdBu_r',
                                  unit='AU', cbar_fmt='%0.1f',
                                  mask=show[:, np.newaxis], size=4,
                                  show_names=lambda x: x[0:] + ' ' * 20,
                                  title=title + ' gradiometers')
