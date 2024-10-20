# Tufts Robotics Club Election Results Calculator

This script translates the raw qualtrics results (downloaded as a csv) into a list of winners :)

## Dependencies

This script was developted using python 3.11.7. Libraries used are listed in [requirements.txt](./requirements.txt); you can install them by running `pip install -r requrements.txt`.

## How to Run

The script can be run using the following command:

`python main.py [-h] [--roles ROLES] [--double_roles DOUBLE_ROLES] [--question_pattern QUESTION_PATTERN] [--calculation_method CALCULATION_METHOD] data_file`

where `data_file` is a path to a csv of the raw qualitrics reports (see [Input format](#input-format) below). The optional parameters are as follows:

- `roles`: A comma-separated list of roles in order of priority. Note that these role names must be spelled exactly as they are in the column headers of the raw data, though the lettesr do NOT have to match in case. Defaults to `president,treasurer,outreach/publicity chair,social chair,mechanical chair,electrical chair,cs chair,secretary`.
- `double_roles`: Comma-separated list of roles for which 2 winners should be chosen instead of 1. The same spelling/case rules apply as with `roles`. Defaults to `president,treasurer`.
- `question_pattern`: Regex pattern for parsing column names in the input CSV. Assuming you had 5 candidates for president, the qualtrics output will have 5 columns for this question, each of which as a header of the form "\[question\] - \[candidate name\]". This regex pattern needs to be able to isolate both the role name and candidate name out of each of these column headers.
    - For example, if your questions were all phrased like "Please rank your choices for \[role\]", one of your president columns will be "Please rank your choices for President - Emma Bethel". The regex pattern `"Please rank your choices for (.+) - (.+)"` would successfully extract "President" and "Emma Bethel" from this string.
    - This script assumes you phrased all your questions the same. If you phrased each question slightly differently... idk man I guess you can either change the code, figure out something reeeeeally smart with regex, or manually change the column headers in the csv so they can all match.
    - Pro regex tip: just chatgpt it 🤫 Also you can use [this website](https://regex101.com/) to test your patterns on example strings.
    - Defaults to `"Please rank your choices for (.+) - (.+)"`.
- `calculation_method`: A string indicating which method to use for calculating the winners for double roles (if you were on e-board in Spring 2024... apologies for the war flashbacks). Acceptable inputs are `pbv` (preferential block voting) and `stv` (single transferable vote). Defaults to `stv`.
    - An explanation of what these are can be found in the [pyrankvote documentation](https://pypi.org/project/pyrankvote/), and/or on Wikipedia&mdash; essentially it boils down to a choice between whether there is a meaningful distinction between people's first and second choices on these two-winner roles.

## Input Format

Unfortunately I no longer have qualitrics access so cannot give exact instructions, but there should be a way to download the results of a form as a csv. You should then **delete the second row** (ngl I forgot why-- I think it's just metadata or something?), and then you should be good to go :) See [spring_2024.csv](spring_2024.csv) for an example.

(If you&mdash; yeah, *you*&mdash; want to make these instructions more detailed, please do!!)

## Troubleshooting

If you have an issues running this script... ask me lol. Or if it's way far in the future and I'm no longer on Slack, ask whoever ran elections the previous year, and they can ask the person before them, and so on and so forth until it (hopefully) gets back to me, or at least to someone who knows how to fix it. Also, while we're at it, thank you for helping keep this club afloat!!!
