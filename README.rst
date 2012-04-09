CanonicalBicycleID
==================

Description
-----------

A Python package with functions for identifying unknown coefficients of the
two second order equations of the bicycle in mass-spring-damper form:

M * q'' + C * q' + K * q = T + H * F

or the benchmark speed and gravity dependent form [Meijaard2007]_:

M * q'' + v * C1 * q' + [g * K0 + v^2 * K2] * q = T + H * F

where

q = [roll angle,
     steer angle]

T = [roll torque,
     steer torque]

F = [lateral force]

Dependencies
------------

- setuptools
- BicycleParameters
- BicycleDataProcessor
- DynamicistToolKit
- Uncertainties

Data
----

The data set used for the analyses is available as an HDF5 database and can
easily be accessed and manipulated with the BicycleDataProcessor pacakage.
