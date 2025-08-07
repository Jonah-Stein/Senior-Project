### Analyzing the Impact of Forced Ballot Truncation on Bucklin, Coombs, Plurality with Runoff, and Schulze in Realistic Environments

## Research Abstract
Elections employ various voting systems to determine winners based on voters' preferences. Recently, ranked-choice elections have become more popular, however, many of them have forced voters to truncate their ballots by only ranking a subset of the candidates. This study analyzes how forced ballot truncation affects the Bucklin, Coombs, plurality with runoff, and Schulze voting systems' abilities to output their true winning sets. This study also accounts for forced ballot truncation within the context of more realistic circumstances as compared to previous research on these voting methods including accounting for voters not completely filling out ballots and voters ordering their candidates who are aligned with their preferences instead of a random order. Using computer simulations, 840,000 sets of ballots were generated with a spatial model using different numbers of candidates, voters, and dimensions. The true winning set was determined for each system using complete preferences, then compared to winning sets derived from repeatedly truncated preferences within the same preference profile. The ability of a voting method to select the true winner under truncated conditions was used to measure its resistance to truncation. The results of this research can provide insights into how forced ballot truncation impacts voting systems in realistic environments, hopefully aiding election designers in their work.

## Running your own simulation
Edit the following variables in `simulation.py`:
- `times_per_permutation`(int): number of preference profiles generated per permutation of variables
- `candidates`(int[]): number of candidates in elections
- `voters`(int[]): number of voters in elections
- `dimension_values`(int[]): number of dimensions for the spatial model
