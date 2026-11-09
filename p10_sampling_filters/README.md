# P10. Sampling, HMMs and robot localization

Lecture notes: 23 - MCMC and Approximate Inference, 24 - Viterbi, Particle and Kalman Filters  
Reuses: P9, P1 grid

**Build:** Rebuilds the localization half of course Project 3 (SLAM with Bayes filters).

## Core
- [ ] Prior, rejection, likelihood-weighting and Gibbs sampling on P9's nets
- [ ] Viterbi and forward filtering on the occasionally dishonest casino HMM
- [ ] Particle filter localizing a robot on P1's grid from noisy wall sensors

## Measure
Error vs. sample count per sampler (log scale) against VE's exact answer; particle filter error over time for 100, 1,000, 10,000 particles.

## Check yourself
- Why does rejection sampling waste samples when evidence is unlikely?
- When does a Kalman filter beat a particle filter?

## Stretch
1-D Kalman filter (boat on a line); add mapping to the particle filter for a simple SLAM.
