# P11. Machine learning from scratch

Lecture notes: 25 - Perceptrons, 26 - Neural Networks  
Reuses: —

**Build:** Everything in numpy first, then the same network in PyTorch.

## Core
- [ ] Naive Bayes text classifier with Laplace smoothing (spam/ham)
- [ ] Binary and multiclass perceptron
- [ ] Logistic regression with softmax
- [ ] 2-layer MLP with hand-written backprop on MNIST (mini-batch SGD)

## Measure
Train vs. test accuracy curves per model; show overfitting on a small training set and fix it with L2 or early stopping.

## Check yourself
- Check your backprop with numerical gradients (finite differences).
- Why can't a single perceptron learn XOR?

## Stretch
Small CNN in PyTorch; compare accuracy and parameter count with the MLP.
