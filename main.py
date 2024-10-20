import pandas as pd
import re
from pyrankvote import Candidate, Ballot, preferential_block_voting, single_transferable_vote
import numpy as np
import argparse

DEFAULT_DOUBLE_ROLES = ('president', 'treasurer')
DEFAULT_ROLE_ORDER = ['president', 'treasurer', 'outreach/publicity chair', 'social chair', 'mechanical chair', 'electrical chair', 'cs chair', 'secretary']
DEFAULT_QUESTION_PATTERN = r"Please rank your choices for (.+) - (.+)"
DEFAULT_CALCULATION_METHOD = 'stv'

CALCULATION_METHODS = {
    'stv': single_transferable_vote,
    'pbv': preferential_block_voting
}


def calculate_results(data, double_roles, role_order, question_pattern, calculation_method):
    print('')
    roles = {}

    # parsing candidates & roles from column headers
    for col_header in data.columns:
        match = re.search(question_pattern, col_header)

        if match is not None:
            role = match.group(1).lower()
            candidate_name = match.group(2)

            if roles.get(role) is None:
                roles[role] = {"candidates": [], "ballots": []}

            roles[role]['candidates'].append((col_header, Candidate(candidate_name)))
    
    if not roles:
        exit("ERROR: Could not parse file headers. Are you sure your question_pattern regex is correct?")

    winners = []
    for role in role_order:
        if roles.get(role) is not None:
            candidate_count = len(roles[role]['candidates'])

            # getting rid of candidates who have already won something
            roles[role]['candidates'] = [x for x in roles[role]['candidates'] if x[1] not in winners]

            print(f'-----{role.upper()}-----\n')
            if len(roles[role]['candidates']) != 0:
                # collect rankings for this role from all ballots
                for _, row in data.iterrows():
                    ranking = [None for _ in range(candidate_count)]

                    for col, candidate in roles[role]['candidates']:
                        val = row[col]

                        if np.isnan(val):
                            break

                        ranking[int(val) - 1] = candidate

                    if any(x is not None for x in ranking):
                        ranking = [x for x in ranking if x is not None]
                        roles[role]['ballots'].append(Ballot(ranked_candidates=ranking))

                # calculating and printing the winner
                num_spots = 2 if role in double_roles else 1

                if num_spots >= len(roles[role]['candidates']):
                    print(" and ".join([cand[1].name for cand in roles[role]['candidates']]), "won by default")
                    for _, cand in roles[role]['candidates']:
                        winners.append(cand)
                else:
                    result = calculation_method([cand[1] for cand in roles[role]['candidates']], roles[role]['ballots'], 2 if role in double_roles else 1)
                    print(result)
                    winners += result.get_winners()

                print('')  
            else:
                print('No Candidates', '\n')


if __name__ == "__main__":
    # parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help="path to election results csv")
    parser.add_argument('--roles', help=f"comma-separated list of roles in order of priority. if not specified, defaults to {','.join(DEFAULT_ROLE_ORDER)}.")
    parser.add_argument('--double_roles', help=f"comma-separated list of roles for which 2 candidates should be chosen. if not specified, defaults to {','.join(DEFAULT_DOUBLE_ROLES)}.")
    parser.add_argument('--question_pattern', help=f'regex pattern for parsing column names in results csv. see README for more details.')
    parser.add_argument('--calculation_method', help=f'method for calculating votes (only affects double roles). see README for more details.', default=DEFAULT_CALCULATION_METHOD)

    args = parser.parse_args()

    if args.roles:
        role_order = args.roles.split(',')
    else:
        role_order = DEFAULT_ROLE_ORDER
    
    if args.double_roles:
        double_roles = args.double_roles.split(',')
    else:
        double_roles = DEFAULT_DOUBLE_ROLES
    
    if args.question_pattern:
        question_pattern = args.question_pattern
    else:
        question_pattern = DEFAULT_QUESTION_PATTERN

    calc_method_str = args.calculation_method.lower()
    calculation_method = CALCULATION_METHODS.get(calc_method_str)

    if calculation_method is None:
        print(f"WARNING: {calc_method_str} is not a valid calculation method; defaulting to {DEFAULT_CALCULATION_METHOD}")
        calculation_method = CALCULATION_METHODS[DEFAULT_CALCULATION_METHOD]

    # calculating the results!
    data = pd.read_csv(args.data_file)

    calculate_results(data, double_roles, role_order, question_pattern, calculation_method)
