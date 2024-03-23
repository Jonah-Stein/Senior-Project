from pref_voting.profiles import Profile
from pref_voting.generate_profiles_OLD import generate_profile, create_rankings_mallows, prob_models 
from pref_voting.margin_based_methods import beat_path as beat_path_faster
from pref_voting.weighted_majority_graphs import MarginGraph
from pref_voting.other_methods import bucklin
from pref_voting.iterative_methods import coombs
from ownmethods import coombs_with_uniform_truncation, bucklin_with_uniform_truncation, plurality_with_runoff_profile_with_ties, truncate_profile_uniformly, truncate_profile_probabilistically
from refinedvotingmethods import bucklin_with_variable_lengths
import csv

# Creates Rankings
prof = create_rankings_mallows(4, 100, 0.5)
distribution = [0.5744624951135919, 0.07014791043554941, 0.010189183538032163, 0.3452004109128265]
#distribution = [0.6097431871894862, 0.08698258554486002, 0.04149472859529119, 0.019716119160653467, 0.00429439528521086, 0.005497163261379343, 0.23227182096311894]
#distribution = [0,1,0,0]
# Puts the ranking into a usable form
prof = Profile(prof[0], prof[1])

#prof = Profile([(2, 0, 3, 1), (3, 2, 0, 1), (3, 1, 2, 0), (1, 2, 3, 0), (0, 3, 1, 2), (3, 2, 1, 0), (1, 0, 2, 3), (1, 3, 0, 2), (0, 2, 3, 1), (3, 0, 1, 2)])
# print(prof.rankings)
# print(type(prof.rankings[0]))
#print(isinstance(prof.rankings[0], tuple))
#new_prof = truncate_profile_uniformly(prof, 2)

new_prof = truncate_profile_probabilistically(prof, distribution)
new_prof.use_extended_strict_preference()

# prof.display_margin_graph()
# new_prof.display_margin_graph()

    #print(r.rmap.keys())
print("NEW RANKINGS")
new_prof = truncate_profile_uniformly(new_prof, 1)
new_prof.use_extended_strict_preference()
new_prof.display_rankings()
print(bucklin_with_variable_lengths(new_prof))
print(beat_path_faster(new_prof))
print(coombs_with_uniform_truncation(new_prof))
print(plurality_with_runoff_profile_with_ties(new_prof))
# for r in new_prof.rankings:
#     print(r.rmap)
