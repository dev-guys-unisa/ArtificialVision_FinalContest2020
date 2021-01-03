'''
    This function randomly takes THRESHOLD images for each group, except for the 3rd group from which it takes THRESHOLD+DELTA.
    If a group contains less than the desired number of images, they are all taken and the remaining images 
    (for reaching the threshold) are randomly chosen between the images not already taken.
    It takes two dicts:
        - GROUPED_AGES => {identity:{group_age:[jpgs]}}}
        - FINAL_DICT {identity:jpgs}
    and return 
        - FINAL_DICT {identity:jpgs}
'''

import random as rd

# parameters
THRESHOLD = 30
DELTA = 30
N_GROUPS = 4

rd.seed(42)

def recover_identities(grouped_ages,final_dict):
    for id in grouped_ages.keys():
        remaining_jpgs = []
        adjust = False
        to_retrieve = 0
        final_dict[id] = []
        for i in range(1, N_GROUPS+1):
            try:
                jpgs = grouped_ages[id]["group{}".format(i)]
            except:
                print(id)
            # if it's the 3rd group, take random 60 elements
            if i == 3:
                if len(jpgs)>THRESHOLD+DELTA:
                    sampling = rd.sample(jpgs, k=THRESHOLD+DELTA)
                    final_dict[id].extend(sampling)
                    for s in sampling:
                        jpgs.remove(s)
                    remaining_jpgs.extend(jpgs)
                else: # take all
                    final_dict[id].extend(jpgs)
                    adjust = True
                    to_retrieve += THRESHOLD+DELTA - len(jpgs)
            # otherwise take random 30 elements
            elif len(jpgs) > THRESHOLD: 
                sampling = rd.sample(jpgs, k=THRESHOLD)
                final_dict[id].extend(sampling)
                for s in sampling:
                    jpgs.remove(s)
                remaining_jpgs.extend(jpgs)
            else:  # take all
                final_dict[id].extend(jpgs)
                adjust = True
                to_retrieve += THRESHOLD - len(jpgs)
        # if a group hasn't 30 values, take the remaining values to reach 150 samples from remaining groups
        if adjust:
            sampling = rd.sample(remaining_jpgs, k=to_retrieve)
            final_dict[id].extend(sampling)
    
    return final_dict
