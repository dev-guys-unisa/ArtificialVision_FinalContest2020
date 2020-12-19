import matplotlib.pyplot as plt

def plot_balancing_original(ages): 
    #ages = {}  # {identity:{jpg:age}}
    classes = {}
    for id in list(ages.keys()):
        for age in ages[id].values():
            try:
                classes[age] += 1
            except:
                classes[age] = 1

    return classes


def plot_balancing_modified(ages, final_dict):
    #final_dict = {} #{identity:[jpgs]}
    classes = {}
    for id in list(final_dict.keys()):
        for jpg in final_dict[id]:
            age = ages[id][jpg]
            try:
                classes[age] += 1
            except:
                classes[age] = 1

    return classes


def vs_plot(ages, final_dict):
    classes_orig = plot_balancing_original(ages)
    classes_mod = plot_balancing_modified(ages, final_dict)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("CLASSES BALANCE ORIGINALvsMODIFIED (3 AGE GROUPS)")
    ax1.bar (classes_orig.keys(), classes_orig.values())
    ax1.title.set_text("ORIGINAL TS")
    ax1.set_xlabel("age classes")
    ax1.set_ylabel("number of occurences")
    ax2.bar (classes_mod.keys(), classes_mod.values())
    ax2.title.set_text("MODIFIED TS")
    ax2.set_xlabel("age classes")
    ax2.set_ylabel("number of occurences")
    plt.show()