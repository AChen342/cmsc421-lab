# P12. Reinforcement learning

Lecture notes: 27-28 - Reinforcement Learning  
Reuses: P1 grid

**Build:** An MDP version of P1's grid world (noisy moves, rewards, discount) and a bandit testbed.

## Core
- [ ] Value iteration and policy iteration
- [ ] ε-greedy and UCB1 bandits
- [ ] TD(0) and tabular Q-learning
- [ ] Approximate Q-learning with features

## Measure
Regret over time for ε-greedy vs. UCB1; Q-learning reward per episode for three ε values; iterations to converge for VI vs. PI.

## Check yourself
- Derive the Bellman update for one grid cell by hand.
- Why is Q-learning off-policy, and why does that matter?

## Stretch
Q-learning or DQN on Gymnasium's CartPole; or train an agent for P3's Connect Four.
