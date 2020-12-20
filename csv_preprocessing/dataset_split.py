from sklearn.model_selection import train_test_split

def train_test_val_split(ages, final_dict, train_perc=0.7, test_perc=0.1):
    x_train, y_train, x_val, y_val, x_test, y_test = [],[],[],[],[],[]
    splitted_dict_samples = {} # {id:{"train":[jpgs]}}
    splitted_dict_labels = {} # {id:{"train":[ages]}}

    for id in list(final_dict.keys()):
        splitted_dict_samples[id], splitted_dict_labels[id] = {},{}
        splitted_dict_samples[id]["train"], splitted_dict_labels[id]["train"] = [],[]
        splitted_dict_samples[id]["val"], splitted_dict_labels[id]["val"] = [],[]
        splitted_dict_samples[id]["test"], splitted_dict_labels[id]["test"] = [],[]
        labels = []
        
        data = list(final_dict[id])
        for jpg in data:
            labels.append(ages[id][jpg])
        
        x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_perc, random_state=18, shuffle=True)
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size=train_perc, random_state=18, shuffle=True)

        splitted_dict_samples[id]["train"].extend(x_train)
        splitted_dict_samples[id]["val"].extend(x_val)
        splitted_dict_samples[id]["test"].extend(x_test)

        splitted_dict_labels[id]["train"].extend(y_train)
        splitted_dict_labels[id]["val"].extend(y_val)
        splitted_dict_labels[id]["test"].extend(y_test)
    
    return splitted_dict_samples, splitted_dict_labels

