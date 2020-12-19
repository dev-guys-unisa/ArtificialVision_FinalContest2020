import random as rd

# GROUPED_AGES => {identity:{group_age:[jpgs]}} = {str:{str:list<str>}}
# FINAL_DICT #{identity:jpgs}

rd.seed(42)

def recover_identities(grouped_ages,final_dict):
    for id in grouped_ages.keys():
        remaining_jpgs = []
        adjust = False
        to_retrieve = 0
        for i in range(1, 4):
            final_dict[id] = []
            try:
                jpgs = grouped_ages[id]["group{}".format(i)]
            except:
                print(id)
            if len(jpgs) > 50:
                # take random 50 elements
                sampling = rd.sample(jpgs, k=50)
                final_dict[id].extend(sampling)
                for s in sampling:
                    jpgs.remove(s)
                remaining_jpgs.extend(jpgs)
            else:  # take all
                final_dict[id].extend(jpgs)
                adjust = True
                to_retrieve += 50 - len(jpgs)
        if adjust:  # if a group hasn't 50 values, take the remaining values to reach 150 samples from remaining groups
            sampling = rd.sample(remaining_jpgs, k=to_retrieve)
            final_dict[id].extend(sampling)
    
    return final_dict
