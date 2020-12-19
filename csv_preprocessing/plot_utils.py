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
    #ax1.title("".join("CLASSES BALANCE ORIGINAL"))
    ax1.bar (classes_orig.keys(), classes_orig.values())
    #ax2.title("".join("CLASSES BALANCE MODIFIED"))
    ax2.bar (classes_mod.keys(), classes_mod.values())
    plt.show()