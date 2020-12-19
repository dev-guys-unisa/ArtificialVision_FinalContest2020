from get_ages_from_csv import read_csv
from group_ages import group_ages
from recover_identities import recover_identities
from plot_utils import vs_plot

ages = {}  # {identity:{jpg:age}}
grouped_ages = {} #{identity:{group_age:[jpgs]}}
final_dict = {} #{identity:jpgs}

print("Getting ages...")
ages = read_csv(ages)
print("Getting ages... DONE")

print("Grouping ages...")
grouped_ages, final_dict = group_ages(ages, grouped_ages, final_dict)
print("Grouping ages... DONE")

print ("Recovering identities from groups...")
final_dict = recover_identities(grouped_ages,final_dict)
print ("Recovering identities from groups...DONE")

print("NUMBER OF TAKEN IDENTITIES: {}".format(len(final_dict.keys()))) #8421
cnt = 0
for jpgs in final_dict.values():
    cnt += len(jpgs)
print("NUMBER OF TAKEN SAMPLES: {}".format(cnt)) #1261462

print ("Plotting...")
vs_plot(ages,final_dict)
print ("Plotting...DONE")