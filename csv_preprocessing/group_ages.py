'''
    This function allows to group ages associated to a specific identity into N_GROUPS groups of MAX_JPGS length.
    If an identity has less than MAX_JPGS images, they are all taken.
    It takes
        - ages -> {identity:{jpg_path:age}}
    and returns 2 dictionaries:
        - grouped_ages -> {identity:{group_age:[jpgs]}} of images grouped by ages
        - final_dict -> {identity:jpgs} of chosen images per identity
'''

MAX_JPGS = 150
N_GROUPS = 4

def group_ages(ages):
    #ranges = []
    grouped_ages, final_dict = {}, {}

    for id in ages.keys():
        vals = list(ages[id].values())
        if len(vals)<=MAX_JPGS: #take all jpgs
            final_dict[id] = ages[id].keys()
        else:
            grouped_ages[id]={}
            grouped_ages[id]["group1"] = []
            grouped_ages[id]["group2"] = []
            grouped_ages[id]["group3"] = []
            grouped_ages[id]["group4"] = []
            cnt = -1
            min_val = min(vals)
            max_val = max(vals)
            r = max_val - min_val
            split = r//N_GROUPS
            for v in vals:
                cnt += 1
                if min_val<= v <min_val+split:
                    grouped_ages[id]["group1"].append(list(ages[id].keys())[cnt])
                elif min_val+split<= v <min_val+2*split:
                    grouped_ages[id]["group2"].append(list(ages[id].keys())[cnt])
                elif min_val+2*split<= v <min_val+3*split:
                    grouped_ages[id]["group3"].append(list(ages[id].keys())[cnt])
                else:
                    grouped_ages[id]["group4"].append(list(ages[id].keys())[cnt])
        #ranges.append(r)
    return grouped_ages,final_dict

#print ("max range {}".format(max(ranges))) #78.0