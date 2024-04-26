import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('headered-final-data.csv')
df.replace(0, pd.NA, inplace=True)

methodnames = ['Schulze', 'Bucklin', 'Plurality With Runoff', 'Coombs']
voter_values = [100,200,300,400,500,600,2000]
for c in voter_values:
    plt.figure(figsize=(10, 6))

    cfiltered_df = df[(df['Voters'] == c)]

    schulze = cfiltered_df[(cfiltered_df['Voting Method'] == 'Schulze')].iloc[:, -7:].mean().reset_index()
    bucklin = cfiltered_df[(cfiltered_df['Voting Method'] == 'Bucklin')].iloc[:, -7:].mean().reset_index()
    plurality_with_runoff = cfiltered_df[(cfiltered_df['Voting Method'] == 'Plurality With Runoff')].iloc[:, -7:].mean().reset_index()
    coombs = cfiltered_df[(cfiltered_df['Voting Method'] == 'Coombs')].iloc[:, -7:].mean().reset_index() 

    votingmethods = [schulze, bucklin, plurality_with_runoff, coombs]

    for i in range(len(votingmethods)):
        votingmethods[i].columns = ['Ballot Length', 'Percentage True Winner Reached']
        sns.lineplot(data=votingmethods[i], x='Ballot Length', y='Percentage True Winner Reached', marker='X', markersize=5, label=methodnames[i])

    plt.title(f'Percentage True Winner Reached by Ballot Length Voters: {c}')
    plt.xlabel('Number of Candidates on the Ballot')
    plt.ylabel('Percentage True Winner Reached (%)')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.show()

    #----- Saving data in spreadsheet -----
    concat_df_list = []
    for method, vm_df in zip(methodnames, votingmethods):
        temp_df = vm_df['Percentage True Winner Reached'].transpose()
        temp_df.name = method  # Set the row name to the voting method
        concat_df_list.append(temp_df)

    # Concatenate into a single DataFrame
    combined_df = pd.concat(concat_df_list, axis=1)
    combined_df.columns = methodnames  # Set column names to the voting method names

    # Transpose to get the desired format (voting methods as rows, percentages as columns)
    final_df = combined_df.transpose()

    # Resetting index to add the voting method names as a regular column
    final_df.reset_index(inplace=True)
    final_df.rename(columns={'index': 'Voting Method'}, inplace=True)

    # Save the combined DataFrame to CSV
    final_df.to_csv(f'{c}_voters_isolated.csv', index=False)