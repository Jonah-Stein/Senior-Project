from pref_voting.profiles import Profile
from pref_voting.generate_profiles_OLD import generate_profile, create_rankings_mallows, prob_models 
from pref_voting.margin_based_methods import beat_path as beat_path_faster
from pref_voting.weighted_majority_graphs import MarginGraph
from pref_voting.other_methods import bucklin
from pref_voting.iterative_methods import coombs
from ownmethods import coombs_with_uniform_truncation, bucklin_with_uniform_truncation, plurality_with_runoff_profile_with_ties, truncate_profile_uniformly, truncate_profile_probabilistically
import csv

# Creates Rankings
prof = create_rankings_mallows(4, 10, 0.5)
distribution = [0.5744624951135919, 0.07014791043554941, 0.010189183538032163, 0.3452004109128265]
# distribution = [0,0,0,1]
# Puts the ranking into a usable form
prof = Profile(prof[0], prof[1])
print(prof.rankings)
print(type(prof.rankings[0]))
new_prof = truncate_profile_uniformly(prof, 2)

# new_prof = truncate_profile_probabilistically(prof, distribution)
# for r in new_prof.rankings:
#     sliced = list(r.rmap.items())[:2]
#     print(sliced)
#     print(dict(sliced))

    #print(r.rmap.keys())
print("NEW RANKINGS")
new_prof = truncate_profile_uniformly(new_prof, 3)
for r in new_prof.rankings:
    print(r.rmap)
