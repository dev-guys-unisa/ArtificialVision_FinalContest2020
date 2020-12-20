MAX_JPGS = 150

def group_ages(ages, grouped_ages, final_dict):
    #ranges = []

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
            split = r//4
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