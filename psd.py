# -*- coding: utf-8 -*-
"""
Transform epochs into Welch PSD topo plots.
"""

import glob
import os
import os.path as op

import numpy as np

import mne

work_dir = '/storage/Maggie/f2f/'
psd_dir = './psds'

if not op.isdir(psd_dir):
    os.mkdir(psd_dir)

kinds = ('talk', 'ignore')
reload_data = False

if reload_data:
    # fmin, fmax, n_fft = 1., 100., 2048
    n_fft = None

    # Get subject list
    subjects = sorted(glob.glob(work_dir + 'f2f_*_OTP'))
    assert all(op.isdir(s) for s in subjects)
    subjects = [op.basename(s) for s in subjects]
    bad_subjects = ['f2f_023_01_OTP', 'f2f_024_02_OTP', 'f2f_030_01_OTP']
    assert all(b in subjects for b in bad_subjects)
    subjects = [s for s in subjects if s not in bad_subjects]
    for subject in subjects:
        print(subject)
        evokeds = list()
        for kind in kinds:
            print('  epochs: %s' % kind)
            epochs = mne.read_epochs(op.join(
                work_dir, subject, 'epochs',
                '%s_%s_ex-epo.fif' % (subject, kind)), preload=False)
            this_n_fft = 2 ** int(np.ceil(np.log2(len(epochs.times))))
            if n_fft is None:
                n_fft = this_n_fft
                print('  n_fft=%d' % n_fft)
            assert this_n_fft == n_fft
            picks = mne.pick_types(epochs.info, meg=True)
            print('  PSDs')
            psds = np.abs(np.fft.rfft(
                epochs.get_data()[:, picks], axis=-1, n=n_fft))
            freqs = np.fft.rfftfreq(n_fft, 1. / epochs.info['sfreq'])
            # psds, freqs = mne.time_frequency.psd_multitaper(
            #     epochs, fmin, fmax, picks=picks, n_jobs=12)
            info = mne.pick_info(epochs.info, picks)
            info['sfreq'] = 1. / np.diff(freqs[:2])[0]
            psds = np.mean(psds, axis=0)  # average of an average is okay here
            evoked = mne.EvokedArray(psds, info, tmin=freqs[0],
                                     nave=len(epochs), comment=kind)
            evokeds.append(evoked)
        mne.write_evokeds(op.join(psd_dir, subject + '_psd-ave.fif'),
                          evokeds)

flim = [1, 50]
fnames = sorted(glob.glob(op.join(psd_dir, 'f2f_*_OTP_psd-ave.fif')))
evokeds = list()
for kind in kinds:
    evoked = [mne.read_evokeds(fname, kind) for fname in fnames]
    use_names = set(evoked[0].ch_names)
    for e in evoked[1:]:
        use_names = use_names & set(e.ch_names)
    use_names = list(use_names)
    for e in evoked:
        e.pick_channels(use_names)
    evoked = mne.combine_evoked(evoked, 'nave')
    evoked.crop(*flim)
    evoked.comment = kind.capitalize()
    evoked.data *= 1. / 2 ** 15
    evokeds.append(evoked)
colors = ['#1f77b4', '#2ca02c']
mne.viz.plot_evoked_topo(evokeds[::-1], ylim=dict(grad=[0, 2], mag=[0, 10]),
                         color=colors[::-1],
                         axis_facecolor='w', fig_facecolor='w', font_color='k',
                         proj=False, merge_grads=False)
