#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix split file errors.
"""

import os.path as op
import mne

subjects = ['f2f_009_01_OTP', 'f2f_010_01_OTP', 'f2f_011_01_OTP',
        'f2f_012_01_OTP', 'f2f_013_01_OTP', 'f2f_014_01_OTP',
        'f2f_015_01_OTP', 'f2f_018_01_OTP', 'f2f_021_01_OTP',
        'f2f_022_01_OTP', 'f2f_023_01_OTP', 'f2f_024_01_OTP',
        'f2f_025_01_OTP', 'f2f_026_01_OTP', 'f2f_027_01_OTP',
        'f2f_028_01_OTP', 'f2f_029_01_OTP', 'f2f_034_01_OTP',
        'f2f_036_01_OTP', 'f2f_037_01_OTP', 'f2f_038_01_OTP',
        'f2f_102_OTP', 'f2f_103_OTP', 'f2f_104_OTP',
        'f2f_106_OTP', 'f2f_107_OTP', 'f2f_108_OTP',
        'f2f_111_OTP', 'f2f_112_OTP', 'f2f_114_OTP',
        'f2f_115_OTP', 'f2f_116_OTP', 'f2f_117_01_OTP',
        'f2f_118_01_OTP', 'f2f_119_01_OTP']

for subj in subjects:
    fname_2 = op.join(subj, 'raw_fif', subj + '_raw-1.fif')
    if op.isfile(fname_2):
        fname_1 = fname_2[:-10] + '_raw.fif'
        raw = mne.io.read_raw_fif(
            fname_1, allow_maxshield='yes', verbose=False)
        if len(raw._filenames) == 1:  # didn't pick up the split
            raw.load_data()
            raw_2 = mne.io.read_raw_fif(fname_2, allow_maxshield='yes',
                                        verbose=False)
            assert raw_2.first_samp == raw.last_samp + 1
            raw.append(raw_2.load_data())
            print('Saving %s' % (fname_1,))
            raw.save(fname_1, overwrite=True)
            raw = mne.io.read_raw_fif(fname_1, allow_maxshield='yes')
            assert len(raw._filenames) == 2
