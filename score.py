### scoring function for f2f

import numpy as np
import mne
from mnefun._paths import get_raw_fnames, get_event_fnames


def score(p, subjects, run_indices):
    """Default scoring function that just passes event numbers through"""
    for si, subj in enumerate(subjects):
        print('  Scoring subject %s... ' % subj, end='')

        # Figure out what our filenames should be
        raw_fnames = get_raw_fnames(p, subj, 'raw', False, False,
                                    run_indices[si])
        eve_fnames = get_event_fnames(p, subj, run_indices[si])

        for raw_fname, eve_fname in zip(raw_fnames, eve_fnames):
            raw = mne.io.read_raw_fif(raw_fname, allow_maxshield='yes',
                                      verbose=False)
            events = mne.find_events(raw, stim_channel='STI101',
                                     shortest_event=1, mask=128,
                                     mask_type='not_and',
                                     verbose=False)
            events[:, 2] += 10
            if subj.startswith('f2f_108'):  # weird triggering
                mask = (events[:, 2] == 19)
                events[mask, 2] = 13
            n_bad = (~np.in1d(events[:, 2], [11, 13, 15])).sum()
            if n_bad > 0:
                print('Found %d unknown events!' % n_bad)
            else:
                print()
            mne.write_events(eve_fname, events)
