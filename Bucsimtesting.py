# required packages
from pref_voting.profiles import Profile
from generate_profiles_OLD import generate_profile, prob_models 
from pref_voting.margin_based_methods import beat_path as beat_path_faster
from pref_voting.weighted_majority_graphs import MarginGraph
from pref_voting.other_methods import bucklin
from pref_voting.iterative_methods import coombs
from ownmethods import coombs_with_uniform_truncation, bucklin_with_uniform_truncation, plurality_with_runoff_profile_with_ties, truncate_profile_uniformly, truncate_profile_probabilistically
from refinedvotingmethods import bucklin_with_variable_lengths, bucklin_with_variable_lengths_logged
import csv

import matplotlib.pyplot as plt

# Writes the data to a csv file for later analysis
# data_file = open("data.csv", "w")
# data_writer = csv.writer(data_file)

# Variables for the simulation
times_per_permutation = 10000
candidates = [4]
voters = [50]
dimension_values = [2]

# Probability models:
probability_models = {4: [0.5744624951135919, 0.07014791043554941, 0.010189183538032163, 0.3452004109128265],
5: [0.6296228387845766, 0.07036969294216873, 0.018869240820955528, 0.004423945698945408, 0.2767142817533538],
6: [0.6167639840605066, 0.08185508198359971, 0.03812115871362543, 0.008904520940563022, 0.0062718298205612436, 0.248083424481144],
7: [0.6097431871894862, 0.08698258554486002, 0.04149472859529119, 0.019716119160653467, 0.00429439528521086, 0.005497163261379343, 0.23227182096311894]}

e = False
# Nested for loops run through the various permutations of the test
for candidate_value in candidates:
    if e: break
    for voter_value in voters:
        if e: break
        for dimension_value in dimension_values:
            if e: break
            for i in range(times_per_permutation):
                if e: break
                if i % 250 == 0:
                    print(i)
                success_at_length_bucklin = [0,0,0,0]
                # Creates Rankings
                prof = generate_profile(candidate_value, voter_value, "Spatial", [dimension_value, None]).to_linear_profile()
                # Puts the ranking into a usable form
                #prof = Profile(prof[0], prof[1])
                prof = truncate_profile_probabilistically(prof, probability_models[candidate_value])
                prof.use_extended_strict_preference()
                #print("Very original number of candidates: ", prof.candidates)

                #Records the true winners under each voting system
            
                true_bucklin = bucklin_with_variable_lengths(prof)
                


                # Runs through the different truncation levels for each profile
                for ballot_length in range(1,candidate_value + 1):
                    #print("BALLOT LENGTH: ", ballot_length)
                    new_prof = truncate_profile_uniformly(prof, ballot_length, list(range(0, candidate_value)))
                    new_prof.use_extended_strict_preference()
                    #print("OLD: ", prof.candidates, prof.num_cands, "new number of CANDIDATES:", new_prof.num_cands)

                    # Keeps track of each voting system's winners at the level of truncation
                    winners_bucklin = bucklin_with_variable_lengths(new_prof)


                    # Checks if the truncated profile had the same winner under each voting system as its true winner
                    
                    if winners_bucklin == true_bucklin:
                        success_at_length_bucklin[ballot_length - 1] += 1
                    elif ballot_length == 3:
                        print(f"TRUE: {true_bucklin}")
                        print(f"ONE CAND REMOVED: {winners_bucklin}")

                        print("BROKEN \n BROKEN")

                        print("NO TRUNCATION -----------")
                        true_bucklin = bucklin_with_variable_lengths_logged(prof)
                


                        # Runs through the different truncation levels for each profile
                        for ballot_length in range(1,candidate_value + 1):
                            #print("BALLOT LENGTH: ", ballot_length)
                            new_prof = truncate_profile_uniformly(prof, ballot_length, list(range(0, candidate_value)))
                            new_prof.use_extended_strict_preference()
                            #print("OLD: ", prof.candidates, prof.num_cands, "new number of CANDIDATES:", new_prof.num_cands)

                            # Keeps track of each voting system's winners at the level of truncation
                            print(f"{ballot_length} TRUNCATION -----------")
                            winners_bucklin = bucklin_with_variable_lengths_logged(new_prof)
                            print(f"WINNER WITH {ballot_length} TRUNCATION: {winners_bucklin}")


                        prof.display_rankings()
                        e = True
                        break




