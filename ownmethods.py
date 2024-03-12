from pref_voting.profiles import Profile
from pref_voting.profiles_with_ties import ProfileWithTies, Ranking
from itertools import permutations, product

def truncate_profile(profile, length):
    '''
    Takes an input of a previously created profile along with the ballot length at which the truncation should take place

    Returns a profile with ties

    Based off of generate_truncated_profile function
    '''
    
    lprof = profile
    
    rmaps = list()
    for r in lprof.rankings:
        truncate_at = length
        truncated_r = r[0:truncate_at]
        #print(f"the length of the ballot is {len(truncated_r)}")

        rmap = {c: _r + 1 for _r, c in enumerate(truncated_r)}

        rmaps.append(rmap)

    return ProfileWithTies(
        rmaps,
        cmap=lprof.cmap,
        candidates=lprof.candidates
    )

'''
Takes an input of type 'Profile_With_Ties'
'''
def bucklin_with_uniform_truncation(profile, length = None):
    length = length if length is not None else profile.num_cands
    majority = profile.strict_maj_size()
    cand_scores = list()
    for i in range(profile.num_cands):
        cand_scores.append(0)


    rankings = [rank for rank in profile.rankings]
    round = 1
    while max(cand_scores) < majority and round <= length:
        for rank in rankings:
            cand_scores[rank.cands_at_rank(round)[0]] += 1
        
        round += 1
    
    winners = [0]
    for i in range(1, len(cand_scores)):
        if cand_scores[i] > cand_scores[winners[0]]:
            winners = [i]
        elif cand_scores[i] == cand_scores[winners[0]]:
            winners.append(i)
    
    return winners

def strict_last(rank, remaining_candidates):
    cands_ranked = rank.cands
    #print(f"Rank: {rank}")

    last = list()

    for cand in remaining_candidates:
        if cand not in cands_ranked:
            last.append(cand)
    
    if len(last) == 0:
        return rank.last()
    else:
        return last

def coombs_with_uniform_truncation(profile):
    # Number of votes needed for a candidate to be elected
    majority = profile.strict_maj_size()

    # Candidates that haven't been eliminated yet, starts with all the candidates in the election
    remaining_candidates = profile.candidates

    # cand_scores keeps track of how many last place votes a candidate gets in a cycle as well as the amount of first place(later on) 
    cand_scores = list()
    for i in range(profile.num_cands):
        cand_scores.append(0)


    # Runs until a candidate has a majority of the votes, or all candidates are eliminated 
    while True:
        # List of all the rankings associated with the election
        rankings = profile.rankings

        i = 0
        while i < len(rankings):
            if len(rankings[i].ranks) == 0:
                rankings.pop(i)
            else:
                i += 1

        # calculate if there is a majority
        for rank in rankings:
            cand_scores[rank.first()[0]] += 1


        # If there is more than one cand remaining, check whether a majority is present, otherwise return the only remaining candidate
        if len(remaining_candidates) > 1:
            winners = [remaining_candidates[0]]
            if max(cand_scores) >= majority:
                for i in range(1, len(remaining_candidates)):
                    if cand_scores[remaining_candidates[i]] > cand_scores[winners[0]]:
                        winners = [remaining_candidates[i]]
                    elif cand_scores[remaining_candidates[i]] == cand_scores[winners[0]]:
                        winners.append(remaining_candidates[i])
                return winners
        else:
            return remaining_candidates
        
        # clears cand_scores to all 0
        for i in range(len(cand_scores)):
            cand_scores[i] = 0

        # Iterates through the rankings and keeps track of last place votes for candidates
        for rank in rankings:
            last = strict_last(rank, remaining_candidates)
            #print(f"Last: {last}")
            
            for cand in last:
                cand_scores[cand] += 1


        # List of cands to remove after each round
        cands_to_remove = list()

        # Iterates through all last place scores for candidates and updates the candidates that have to be removed
        for cand in remaining_candidates:
            if cands_to_remove == []:
                cands_to_remove.append(cand)
            elif cand_scores[cand] > cand_scores[cands_to_remove[0]]:
                cands_to_remove = [cand]
            elif cand_scores[cand] == cand_scores[cands_to_remove[0]]:
                cands_to_remove.append(cand)
        '''
        print("\n")
        print(f"REMOVED CANDIDATE: {cands_to_remove}")
        print("\n")
        '''
        '''
        # Removes eliminated candidates from ranking 
        for i in range(len(rankings)):
            for cand in cands_to_remove:
                rankings[i].remove_cand(cand)
                print(rankings[i].ranks)
                
                # if the ranking doesn't have any of the remaining candidates, then remove the ranking
                if len(rankings[i].ranks) == 0:
                    rankings.pop(i)
        '''
        profile = profile.remove_candidates(cands_to_remove)

        for cand in cands_to_remove:
            remaining_candidates.remove(cand)
        
        # If all candidates were removed in the round, then they are all the winners
        if remaining_candidates == []:
            return cands_to_remove
        
        '''
        # will trigger if all candidates have been eliminated
        if len(rankings) == 0:
            return remaining_candidates
        '''
        
        # clears cand_scores to all 0
        for i in range(len(cand_scores)):
            cand_scores[i] = 0
        

'''    
def coombs_with_uniform_truncation_e(profile):
    # Number of votes needed for a candidate to be elected
    majority = profile.strict_maj_size()

    # Candidates that haven't been eliminated yet, starts with all the candidates in the election
    remaining_candidates = profile.candidates

    # cand_scores keeps track of how many last place votes a candidate gets in a cycle as well as the amount of first place(later on) 
    cand_scores = list()
    for i in range(profile.num_cands):
        cand_scores.append(0)


    # Runs until a candidate has a majority of the votes, or all candidates are eliminated 
    while True:
        # List of all the rankings associated with the election
        rankings = profile.rankings

        i = 0
        while i < len(rankings):
            if len(rankings[i].ranks) == 0:
                rankings.pop(i)
            else:
                i += 1

        # calculate if there is a majority
        for rank in rankings:
            cand_scores[rank.first()[0]] += 1
        
        print(f"first place: {cand_scores}")

        # If there is more than one cand remaining, check whether a majority is present, otherwise return the only remaining candidate
        if len(remaining_candidates) > 1:
            winners = [remaining_candidates[0]]
            if max(cand_scores) >= majority:
                for i in range(1, len(remaining_candidates)):
                    if cand_scores[remaining_candidates[i]] > cand_scores[winners[0]]:
                        winners = [remaining_candidates[i]]
                    elif cand_scores[remaining_candidates[i]] == cand_scores[winners[0]]:
                        winners.append(remaining_candidates[i])
                print("winners")
                return winners
        else:
            print("remaining candidates")
            return remaining_candidates
        
        # clears cand_scores to all 0
        for i in range(len(cand_scores)):
            cand_scores[i] = 0

        # Iterates through the rankings and keeps track of last place votes for candidates
        for rank in rankings:
            last = strict_last(rank, remaining_candidates)
            #print(f"Last: {last}")
            
            for cand in last:
                cand_scores[cand] += 1
        
        print(f"last places: {cand_scores}")


        # List of cands to remove after each round
        cands_to_remove = list()

        # Iterates through all last place scores for candidates and updates the candidates that have to be removed
        for cand in remaining_candidates:
            if cands_to_remove == []:
                cands_to_remove.append(cand)
            elif cand_scores[cand] > cand_scores[cands_to_remove[0]]:
                cands_to_remove = [cand]
            elif cand_scores[cand] == cand_scores[cands_to_remove[0]]:
                cands_to_remove.append(cand)
        
        print(f"cands_to_remove: {cands_to_remove}")
        
        profile = profile.remove_candidates(cands_to_remove)

        for cand in cands_to_remove:
            remaining_candidates.remove(cand)
        
        # If all candidates were removed in the round, then they are all the winners
        if remaining_candidates == []:
            return cands_to_remove
        
        # clears cand_scores to all 0
        for i in range(len(cand_scores)):
            cand_scores[i] = 0
'''   

def plurality_with_runoff_profile_with_ties(profile, curr_cands = None):
    """If there is a majority winner then that candidate is the plurality with runoff winner. If there is no majority winner, then hold a runoff with  the top two candidates: either two (or more candidates) with the most first place votes or the candidate with the most first place votes and the candidate with the 2nd highest first place votes are ranked first by the fewest number of voters.   A candidate is a Plurality with Runoff winner in the profile restricted to ``curr_cands`` if it is a winner in a runoff between two pairs of first- or second- ranked candidates. If the candidates are all tied for the most first place votes, then all candidates are winners.
        
    Args:
        profile (Profile): An anonymous profile of linear orders on a set of candidates
        curr_cands (List[int], optional): If set, then find the winners for the profile restricted to the candidates in ``curr_cands``

    Returns: 
        A sorted list of candidates
        
    .. note:: 
        Plurality with Runoff is the same as Instant Runoff when there are 3 candidates, but give different answers with 4 or more candidates. 

    :Example: 

    .. exec_code:: 

        from pref_voting.profiles import Profile
        from pref_voting.iterative_methods import instant_runoff, plurality_with_runoff

        prof = Profile([[0, 1, 2, 3], [3, 1, 2, 0], [2, 0, 3, 1], [1, 2, 3, 0], [2, 3, 0, 1], [0, 3, 2, 1]], [2, 1, 2, 2, 1, 2])
        prof.display()
        instant_runoff.display(prof)
        plurality_with_runoff.display(prof)
    
    """    

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