# -*- coding: utf-8 -*-

"""
Created on Fri May 6 7:11:32 2016
@author: mdclarke
mnefun processing script for face to face
"""
import mnefun
import numpy as np
from score import score

n_cores = 4
params = mnefun.Params(tmin=-0.1, tmax=7.0, n_jobs=n_cores,
                       n_jobs_mkl=1, lp_cut=80., lp_trans=3.,
                       n_jobs_fir=n_cores, n_jobs_resample=n_cores,
                       bmin=-0.1, decim=10, proj_sfreq=200,
                       filter_length='auto')
# Notes
# 108 has 19s for 13s

params.subjects = ['f2f_009_01_OTP', 'f2f_010_01_OTP', 'f2f_011_01_OTP',
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
                   'f2f_118_01_OTP', 'f2f_119_01_OTP',
                   'f2f_013_sim']

params.subjects_dir = 'subjects'
params.structurals = params.subjects
params.dates = [(2013, 0, 00)] * len(params.subjects)
params.subject_indices = [35]
# params.subject_indices = np.setdiff1d(np.arange(len(params.subjects)),
#                                       [])
params.score = score
params.acq_ssh = 'maggie@minea.ilabs.uw.edu'
params.acq_dir = ['/sinuhe/data03/face_to_face']
params.sws_ssh = 'localhost'  # 'maggie@kasga.ilabs.uw.edu'
params.sws_dir = '/mnt/bakraid/data/sss_work'  # '/data07/maggie/f2f/'
params.sws_port = 2222
# SSS options
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4.
params.int_order = 6
params.st_correlation = .995  # otp
params.movecomp = 'inter'
params.trans_to = 'twa'
params.coil_bad_count_duration_limit = np.inf
params.coil_dist_limit = None
params.coil_t_window = 'auto'
params.coil_t_step_min = 1.
# Trial/CH rejection criteria
params.autoreject_thresholds = True  # set automatically for each subject
params.autoreject_types = ('mag', 'grad')
params.auto_bad_reject = None
params.ssp_ecg_reject = None
params.flat = dict(grad=1e-13, mag=1e-15)

params.compute_rank = True  # better inverse
params.cov_rank = None  # compute cov on SSS basis
params.force_erm_cov_rank_full = False
params.proj_ave = True  # compute projs on Evoked artifact waveform
params.run_names = ['%s']
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.runs_empty = ['%s_erm']
params.proj_nums = [[2, 2, 0],  # ECG: grad/mag/eeg
                    [0, 0, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.cov_method = 'shrunk'
params.bem_type = '5120'
# Epoching
params.in_names = ['talk', 'ignore']

params.in_numbers = [13, 15]

params.analyses = ['All',
                   'Each']

params.out_names = [['All'],
                    ['talk', 'ignore']]

params.out_numbers = [[1, 1],  # Combine all trials
                      [1, 2]]  # Each
params.must_match = [
    [],  # no match
    [0, 1]]  # match each

times = [0.5, 1., 2.5]

params.report_params.update(  # add a couple of nice diagnostic plots
    bem=False,  # Using a surrogate
    good_hpi_count=False,
    whitening=[
        dict(analysis='All', name='aud',
             cov='%s-80-sss-cov.fif'),
        dict(analysis='Each', name='talk',
             cov='%s-80-sss-cov.fif'),
        dict(analysis='Each', name='ignore',
             cov='%s-80-sss-cov.fif'),
    ],
    sensor=False,
    source=[
        dict(analysis='All', name='All',
             inv='%s_aud-80-sss-meg-free-inv.fif', times=times,
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Each', name='talk',
             inv='%s_aud-80-sss-meg-free-inv.fif', times=times,
             views=['lat', 'caudal'], size=(800, 800)),
        dict(analysis='Each', name='ignore',
             inv='%s_vis-80-sss-meg-free-inv.fif', times=times,
             views=['lat', 'caudal'], size=(800, 800)),
    ],
    source_alignment=False,
    psd=False,  # often slow
)
mnefun.do_processing(
    params,
    fetch_raw=False,
    do_score=True,
    push_raw=False,
    do_sss=True,
    fetch_sss=True,
    do_ch_fix=False,
    gen_ssp=True,
    apply_ssp=True,
    write_epochs=True,
    gen_covs=True,
    gen_fwd=True,
    gen_inv=True,
    gen_report=True,
    print_status=False)
