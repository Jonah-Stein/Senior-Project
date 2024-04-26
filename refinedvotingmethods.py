from pref_voting.profiles import Profile
from pref_voting.profiles_with_ties import ProfileWithTies, Ranking
from itertools import permutations, product
import random
def bucklin_with_variable_lengths(profile):
    winners = list()
    majority = profile.strict_maj_size()
    cand_scores = [0] * profile.num_cands
    # for i in range(profile.num_cands):
    #     cand_scores.append(0)
    cands = profile.num_cands
    ballot_pool = [rank for rank in profile.rankings]
    round = 1
    while max(cand_scores) < majority and len(ballot_pool) > 0 and round <= cands:
        updated_ballot_pool = list()
        for ballot in ballot_pool:
            candidate = ballot.cands_at_rank(round)
            if len(candidate) == 1:
                cand_scores[ballot.cands_at_rank(round)[0]] += 1
                updated_ballot_pool.append(ballot)
            # elif round == cands:
            #     cand_scores[list(set(profile.candidates)-set(ballot.cands))[0]] += 1
        ballot_pool = updated_ballot_pool
        round += 1

    winners = [0]
    for i in range(1, len(cand_scores)):
        if cand_scores[i] > cand_scores[winners[0]]:
            winners = [i]
        elif cand_scores[i] == cand_scores[winners[0]]:
            winners.append(i)

    return winners

def bucklin_with_variable_lengths_logged(profile):
    winners = list()
    majority = profile.strict_maj_size()
    cand_scores = [0] * profile.num_cands
    # for i in range(profile.num_cands):
    #     cand_scores.append(0)
    cands = profile.num_cands
    ballot_pool = [rank for rank in profile.rankings]
    round = 1
    while max(cand_scores) < majority and len(ballot_pool) > 0 and round <= cands:
        updated_ballot_pool = list()
        for ballot in ballot_pool:
            candidate = ballot.cands_at_rank(round)
            if len(candidate) == 1:
                cand_scores[ballot.cands_at_rank(round)[0]] += 1
                updated_ballot_pool.append(ballot)
                # if round == 4:
                #     print(ballot.cands_at_rank(round)[0])
            # elif round == cands:
            #     cand_scores[list(set(profile.candidates)-set(ballot.cands))[0]] += 1
        ballot_pool = updated_ballot_pool
        round += 1
        print(f"ROUND: {round}, CAND_SCORES: {cand_scores}")
        print(f"Length of ballot pool: ", len(ballot_pool))
        round += 1

    winners = [0]
    for i in range(1, len(cand_scores)):
        if cand_scores[i] > cand_scores[winners[0]]:
            winners = [i]
        elif cand_scores[i] == cand_scores[winners[0]]:
            winners.append(i)
        print(winners)

    return winners

def plurality_with_runoff_profile_with_ties(profile, curr_cands = None):
    curr_cands = profile.candidates if curr_cands is None else curr_cands
    
    if len(curr_cands) == 1: 
        return list(curr_cands)
    
    plurality_scores = profile.plurality_scores()  

    max_plurality_score = max(plurality_scores.values())
    
    first = [c for c in curr_cands if plurality_scores[c] == max_plurality_score]
    second = list()
    if len(first) == 1:
        second_plurality_score = list(reversed(sorted(plurality_scores.values())))[1]
        second = [c for c in curr_cands if plurality_scores[c] == second_plurality_score]

    if len(second) > 0:
        all_runoff_pairs = product(first, second)
    else: 
        all_runoff_pairs = [(c1,c2) for c1,c2 in product(first, first) if c1 != c2]

    winners = list()
    for c1, c2 in all_runoff_pairs: 
        
        if profile.margin(c1,c2) > 0:
            winners.append(c1)
        elif profile.margin(c1,c2) < 0:
            winners.append(c2)
        elif profile.margin(c1,c2) == 0:
            winners.append(c1)
            winners.append(c2)
    
    return sorted(list(set(winners)))