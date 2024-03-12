from pref_voting.generate_profiles_OLD import generate_profile, create_rankings_mallows, prob_models 
from pref_voting.profiles import Profile
for i in range(100):
    prof = generate_profile(3, 25, "Spatial", [4, None]).to_linear_profile()
    while type(prof) == None:
        print("while ran")
        prof = generate_profile(3, 25, "Spatial", [4, None]).to_linear_profile()
    print(type(prof))
