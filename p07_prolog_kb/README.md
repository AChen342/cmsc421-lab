# P7. Knowledge base in Prolog

Lecture notes: 11 - Knowledge Engineering  
Reuses: P5 Zebra

**Build:** Mirrors course Assignment #2 (Cars World KB), but in a domain you know well, such as a game or comic universe. Uses SWI-Prolog.

## Core
- [ ] Write 5–10 competency questions first
- [ ] Small ontology (classes, `is_a`, properties)
- [ ] 30+ instance facts and rules that answer each question
- [ ] Zebra puzzle in Prolog; compare length and speed with your P5 version

## Measure
Zebra puzzle: Prolog vs. P5 CSP solver, lines of code and runtime.

## Check yourself
- Trace one query's unification and backtracking with `trace.`.
- Which of your rules are Horn clauses, and which could not be?

## Stretch
Pull 50 real facts for your domain from Wikidata with SPARQL and load them as Prolog facts.
