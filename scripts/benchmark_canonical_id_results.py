#!/usr/bin/env python
import cPickle
import numpy as np
from canonicalbicycleid import canonical_bicycle_id as cbi
from dtk import bicycle, control

def plot(canon, H, riders, environments, idMats):
    filename = ''
    for rider in riders:
        filename += '-' + rider
    for env in environments:
        filename += '-' + env.replace(' ', '')

    filename = '../plots/' + filename[1:]

    print filename

    v0 = 0.
    vf = 10.
    num = 100

    # identified
    iM, iC1, iK0, iK2, iH = idMats
    speeds, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
            v0=v0, vf=vf, num=num)
    w, v = control.eigen_vs_parameter(iAs)
    iEigenvalues, iEigenvectors = control.sort_modes(w, v)

    # whipple model (mean)
    wM, wC1, wK0, wK2, wH = cbi.mean_canon(riders, canon, H)
    speeds, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
            v0=v0, vf=vf, num=num)
    w, v = control.eigen_vs_parameter(wAs)
    wEigenvalues, wEigenvectors = control.sort_modes(w, v)

    # arm model (mean)
    aAs, aBs, aSpeed = cbi.mean_arm(riders)
    indices = np.int32(np.round(speeds * 10))
    w, v = control.eigen_vs_parameter(aAs[indices])
    aEigenvalues, aEigenvectors = control.sort_modes(w, v)

    # eigenvalue plot
    rlfig = cbi.plot_rlocus_parts(speeds, iEigenvalues, wEigenvalues,
            aEigenvalues)
    rlfig.savefig(filename + '-eig.png')

    # root locus
    v0 = 0.
    vf = 10.
    num = 20
    speeds, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
            v0=v0, vf=vf, num=num)
    iEig, null = control.eigen_vs_parameter(iAs)

    speeds, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
            v0=v0, vf=vf, num=num)
    wEig, null = control.eigen_vs_parameter(wAs)

    indices = np.int32(np.round(speeds * 10))
    aEig, null = control.eigen_vs_parameter(aAs[indices])
    rlcfig = cbi.plot_rlocus(speeds, iEig, wEig, aEig)
    rlcfig.savefig(filename + '-rlocus.png')

    # bode plots
    speeds = np.array([2.0, 4.0, 6.0, 9.0])
    null, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
            speeds)
    null, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
            speeds)
    figs = cbi.plot_bode(speeds, iAs, iBs, wAs, wBs, aAs, aBs)
    figs[0].savefig(filename + '-Tphi.png')
    figs[1].savefig(filename + '-Tdel.png')

########################################
allRiders = ['Charlie', 'Jason', 'Luke']
# create the comparison models
canon = cbi.load_benchmark_canon(allRiders)
H = cbi.lateral_force_contribution(allRiders)

with open('../data/idMatrices.p') as f:
    idMatrices = cPickle.load(f)

riders = ['Charlie', 'Jason', 'Luke', 'All']
rMap = {x[0]: [x] for x in riders}
environments = ['Horse Treadmill', 'Pavillion Floor', 'All']
eMap = {x[0]: [x] for x in environments}

for k, v in idMatrices.items():
    r, e = k.split('-')
    if r == 'A':
        riders = ['Charlie', 'Jason', 'Luke']
    else:
        riders = rMap[r]

    if e == 'A':
        environments = ['Horse Treadmill', 'Pavillion Floor']
    else:
        environments = eMap[e]

    plot(canon, H, riders, environments, v)
