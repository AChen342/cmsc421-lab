# P9. Bayes net library

Lecture notes: 20 - Uncertainty I - Probability Basics, 21 - Uncertainty II - Bayesian Networks, 22 - Uncertainty III - Bayes Net Inference  
Reuses: —

**Build:** `Factor` and `BayesNet` classes with CPTs, and a joint-distribution check for small nets.

## Core
- [ ] Inference by enumeration
- [ ] Variable elimination (factor product + sum-out)
- [ ] d-separation checker
- [ ] Burglary/alarm network and cancer network

## Measure
Time for enumeration vs. variable elimination on a chain of 5–20 nodes; compare two elimination orders.

## Check yourself
- Show explaining away: P(Burglary | Alarm) vs. P(Burglary | Alarm, Earthquake).
- Simulate Monty Hall 10,000 times and match it to Bayes' rule.

## Stretch
Polytree algorithm, checked against VE.
