#!/usr/bin/env python
import cPickle
from canonicalbicycleid import canonical_bicycle_id as cbi

riders = ['Charlie', 'Jason', 'Luke']
environments = ['Horse Treadmill', 'Pavillion Floor']
maneuvers = ['Balance',
             'Track Straight Line',
             'Balance With Disturbance',
             'Track Straight Line With Disturbance']

canon = cbi.load_benchmark_canon(riders)
# This gives the proportion of the lateral force which should be added to the
# steer torque and roll torque equations in the canonical equations.
H = cbi.lateral_force_contribution(riders)

runs = cbi.select_runs(riders, maneuvers, environments)
# try to load in all of the runs for the given run numbers.
trials, errors = cbi.load_trials(runs, H)
goodRuns = list(set(runs).difference(errors))

# pick the free parameters
rollParams = ['Mpd', 'C1pd', 'K0pd']
steerParams = ['Mdd', 'C1dp', 'C1dd',
               'K0dd', 'K2dd', 'HdF']

idMatrices = {}
covarMatrices = {}

# These are the 12 models that we are interested in.
combinations = [(x, y) for x in (riders + ['All']) for y in (environments +
        ['All'])]

for combo in combinations:
    print('Computing the estimate for riders: {} and environments: {}'.format(combo[0], combo[1]))
    if combo[0] == 'All':
        riders = ['Charlie', 'Jason', 'Luke']
    else:
        riders = [combo[0]]
    if combo[1] == 'All':
        environments = ['Horse Treadmill', 'Pavillion Floor']
    else:
        environments = [combo[1]]

    runs = cbi.select_runs(riders, maneuvers, environments)
    runs = list(set(runs).difference(errors))

    means = cbi.mean_canon(riders, canon, H)
    idMat, rollCovar, steerCovar = cbi.enforce_symmetry(runs, trials,
            rollParams, steerParams, *means)

    idMatrices[combo[0][0] + '-' + combo[1][0]] = idMat
    covarMatrices[combo[0][0] + '-' + combo[1][0]] = (rollCovar, steerCovar)

    print('Done.')

with open('../data/goodRuns.p', 'w') as f:
    cPickle.dump(goodRuns, f)

# save all of the identified matrices to file
with open('../data/idMatrices.p', 'w') as f:
    cPickle.dump(idMatrices, f)

with open('../data/covarMatrices.p', 'w') as f:
    cPickle.dump(covarMatrices, f)
