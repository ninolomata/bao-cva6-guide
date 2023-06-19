from os import wait
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re
from matplotlib.ticker import PercentFormatter
import argparse
from matplotlib.backends.backend_pdf import PdfPages
import sys
import matplotlib.colors as mcolors

rootdir = sys.argv[1]
parentdir = sys.argv[3]

pdf = PdfPages(parentdir + "/results/" + str(sys.argv[2]) + ".pdf")

rx_dict = {
    'val': re.compile(r'(?P<val>\d+[.]\d+)\s+\([+-](?P<err>\d+[.]\d+)\)\s+\#'),
    'dataset': re.compile(r'(?P<dataset>^\w+\-(qcif|sqcif))'),
    'runs': re.compile(r'(?P<runs>\d+)\s+(runs)'),
    'event': re.compile(r'(?P<count>\d+)\s+(r)(?P<name>\d+)\s+'),
}

events_dict = {
    'r1': "ICache Miss",
    'r2': "Dache Miss",
    'r3': "ITLB Miss",
    'r4': "DTLB Miss",
    'r5': "Load",
    'r6': "Store",
    'r7': "Exception",
}


def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def parse_file(filepath,scenario):
    data = []
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            # extract school name
            if key == 'dataset':
                dataset = match.group('dataset')
            if key == 'runs':
                runs = match.group('runs')
                runs = int(runs)
                i = 0
                while i < runs:
                    # extract grade
                    line = file_object.readline()
                    key, match = _parse_line(line)
                    if key == 'val':
                        val = match.group('val')
                        val = float(val)
                        i += 1
                        row = {
                        'val': val,
                        'dataset': dataset,
                        'scenario': scenario
                        }
                        data.append(row)
            line = file_object.readline()
        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
    return data

def search_event(event):
    return events_dict[event]

def event_parse_file(filepath,scenario):
    data = []
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            # extract school name
            if key == 'dataset':
                dataset = match.group('dataset')
            if key == 'event':
                count = match.group('count')
                count = int(count)
                name = match.group('name')
                name = 'r' + name
            #print(name)
            #    print(count)
                row = {
                    'count': count,
                    'name': search_event(name),
                    'dataset': dataset,
                    'scenario': scenario
                }
                data.append(row)
            line = file_object.readline()
        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
    return data
def  apply_precentile_event(in_data):
    data = []

    #found 1 case and apply precentile
    arr_data = np.array(in_data)
    print(arr_data)
    scenario, counts = np.unique(arr_data[:,3], return_counts=True)
    dataset, counts = np.unique(arr_data[:,2], return_counts=True)
    names, counts = np.unique(arr_data[:,1], return_counts=True)
    print(scenario)
    print(dataset)
    print(names)

    for setup in scenario:
        scenario_arr = arr_data[np.where(arr_data[:, 3] == setup)]
        for set in dataset:
            scenario_dataset_arr = scenario_arr[np.where(scenario_arr[:, 2] == set)]
            for name in names:
                scenario_names_arr = scenario_arr[np.where(scenario_dataset_arr[:, 1] == name)]
                arr_perc_max = np.percentile(scenario_names_arr[:, 0], 95)
                arr_perc_min = np.percentile(scenario_names_arr[:, 0], 5)

                arr_top95 = scenario_names_arr[np.where((scenario_names_arr[:, 0] <= arr_perc_max) & (scenario_names_arr[:, 0] >= arr_perc_min))]
                for x in arr_top95:
                    row = {
                         'count': x[0],
                         'name': name,
                          'dataset': set,
                            'scenario': setup
                            }
                data.append(row)
    data = pd.DataFrame(data)
    return data

def apply_precentile(in_data):
    data = []
    #found 1 case and apply precentile
    arr_data = np.array(in_data)
    print(arr_data)
    scenario, counts = np.unique(arr_data[:,2], return_counts=True)
    dataset, counts = np.unique(arr_data[:,1], return_counts=True)
    print(scenario)
    print(dataset)

    for setup in scenario:
        scenario_arr = arr_data[np.where(arr_data[:, 2] == setup)]
        print("hello")
        print(scenario_arr)
        for set in dataset:
            print(set)
            scenario_dataset_arr = scenario_arr[np.where(scenario_arr[:, 1] == set)]
            print(scenario_dataset_arr)
            arr_perc_75 = np.percentile(scenario_dataset_arr[:, 0], 75)
            arr_perc_25 = np.percentile(scenario_dataset_arr[:, 0], 25)
            IRQ =  arr_perc_75 - arr_perc_25
            lower_bond = arr_perc_25 - (1.5 * IRQ)
            upper_bond = arr_perc_75 + (1.5 * IRQ)

            arr_top95 = scenario_dataset_arr[np.where((scenario_dataset_arr[:, 0] <= arr_perc_75) & (scenario_dataset_arr[:, 0] >= arr_perc_25))]
            for x in arr_top95:
                row = {
                      'val': x[0],
                        'dataset': set,

                        'scenario': setup
                        }
                data.append(row)
    data = pd.DataFrame(data)
    return data

def normalize_data(in_data):
    mean = in_data.groupby(['scenario','dataset'], as_index=False)['val'].mean()
    std = in_data.groupby(['scenario','dataset'], as_index=False)['val'].std()
    norm = mean[(mean['scenario'] == '0-baseline')]
    out_data = mean
    out_data['norm_val_percent'] = 0.0
    out_data['norm_std_percent'] = 0.0
    for x in out_data.index:
        value = norm[norm['dataset'] == out_data['dataset'][x]]['val']
        #out_data['norm_val_percent'][x] = float(((out_data['val'][x] - value) / value) * 1.0) + 1.0
        #out_data['norm_std_percent'][x] = float(((std['val'][x]- value) / value) * 1.0) + 1.0
        out_data['norm_val_percent'][x] = abs(float(((out_data['val'][x] - value) / value) * 1.0)) + 1.0
        out_data['norm_std_percent'][x] = float(((std['val'][x]- value) / value) * 1.0) + 1.0
    return out_data

def normalize_event_data(in_data):
    mean = in_data.groupby(['scenario','name'], as_index=False)['count'].mean()
    std = in_data.groupby(['scenario','name'], as_index=False)['count'].std()
    norm = mean[(mean['scenario'] == '0-baseline')]
    out_data = mean
    out_data['norm_val_percent'] = 0.0
    out_data['norm_std_percent'] = 0.0
    for x in out_data.index:
        value = norm[norm['name'] == out_data['name'][x]]['count']
        out_data['norm_val_percent'][x] = float((out_data['count'][x] / value) * 100.0)
        out_data['norm_std_percent'][x] = float((std['count'][x] / value) * 100.0)
    return out_data


dat = pd.DataFrame()
dat.to_csv('data.csv')
event = pd.DataFrame()
min = pd.DataFrame()

for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        scenario = file
        data = rootdir + "/" + scenario + "/"
        for log in os.listdir(data):
            data = data + log
        result = parse_file(data,scenario)
        res_event = event_parse_file(data,scenario)
        event = pd.concat([event,res_event], ignore_index=True)
        dat = pd.concat([dat,result], ignore_index=True)

dat.to_csv(rootdir + "/" + "data.csv")
#mean = dat.groupby(['scenario','dataset'], as_index=False)['val'].mean()
#std = dat.groupby(['scenario','dataset'], as_index=False)['val'].std()
#min = mean.groupby('dataset', as_index=False)['val'].min()

#for x in mean.index:
#    value = min[min['dataset'] == mean['dataset'][x]]['val']
#    mean['val'][x] = mean['val'][x] / value
#norm_data = normalize_data(dat)

def plot_bw_bench(data):
    precentile_data = apply_precentile(data)
    #normalize data
    norm_data = normalize_data(precentile_data)
    # get xticks labels
    xticks_labels = data['dataset'].unique()
    xticks_labels = [elem.replace('-', '\n') for elem in xticks_labels]
    xticks_labels.sort()
    # determine number of existing scenarios
    scenarios = data['scenario'].unique()
    scenarios.sort()
    #scenarios = scenarios[::-1]
    # labels location
    x = np.arange(len(xticks_labels))
    # the width of the bars
    total_width = 0.9
    width = total_width / len(scenarios)
    fig, axs = plt.subplots(1)
    fig.set_figheight(8)
    fig.set_figwidth(29)
    fig.tight_layout()
    #clist = ['#5A5A5A','#346888','#5886a5','#7aa6c2','#FFDB58','#E1AD01','#a5cbe1','#c1e7ff']
    #clist = ['#1694B2','#CD3700','#D24B1A' ,'#D75F33','#DC734D','#E18766','#E69B80','#EBAF99','#F0C3B3','#F5D7CC','#FAEBE6']
    clist = ["#1695b4", "#ee1f24", "#d4b8b2", "#245789", "#f2d402", "#b0614e", "#76e8ca", "#c9245d", "#8f98e5", "#7f8861"]
    # get x and y for each scenario and type
    for i,scene in enumerate(scenarios) :
        temp = norm_data.loc[norm_data['scenario'] == scene]
        mean = temp['norm_val_percent'].values
        std = temp['norm_std_percent'].values
        bar_base_loc = x - total_width/2
        bar_loc = bar_base_loc + ((i + 1) * width) - (width/2)
        #if i == 0 :
        #    bar_loc = x - width/2
        #else :
        #    bar_loc = x + width/2
        axs.grid(zorder=0)
        hbars = axs.bar(bar_loc, mean, width, label=scene, color=clist[i])
        axs.errorbar(bar_loc, mean, yerr=std, xerr=None, fmt='', capsize=3, color='black', linestyle='',zorder=3)
        # Add some text for labels, title and custom x-axis tick labels, etc.
        axs.margins(x=0)
        axs.set_ylabel('Normalized Speedup',fontsize=28)
        axs.set_xlabel('Benchmark',fontsize=28)
        if i == 0:
            labels = temp['val'].values
            labels =['%.2f s' % l for l in labels]
            axs.bar_label(hbars, labels=labels, label_type='edge', rotation=90, padding=18,fontsize=25)
        axs.set_axisbelow(True)
        axs.set_title("San Diego Vision Subset performance results for PPA selected designs",fontsize=25)
        #axs.set_title(size)
        axs.set_xticks(x, xticks_labels,rotation=0,fontsize=25)
        axs.legend(fontsize=30)
        axs.set_ylim([0.96, 1.22])
        start, end = axs.get_ylim()
        axs.set_yticks(np.arange(start, end, 0.02),rotation=0,fontsize=24)
        axs.yaxis.set_tick_params(labelsize=24)
    # set the spacing between subplots
    plt.subplots_adjust(top=0.935,
                        bottom=0.250,
                        left=0.045,
                        right=0.995,
                        hspace=0.34,
                        wspace=0.22)
    plt.legend(ncol=3,fontsize=21, loc='upper right')
    # plt.savefig('/home/ninolomata/Desktop/Development/openpiton-hyp-guide/benchmarking_paper/Results/Images_V4/sstc.png')
    pdf.savefig(fig)

def plot_event_bench(data,dataset):
    precentile_data = apply_precentile_event(data)
    #normalize data
    norm_data = normalize_event_data(precentile_data)
    # get xticks labels
    xticks_labels = data['name'].unique()
    xticks_labels.sort()
    # determine number of existing scenarios
    scenarios = data['scenario'].unique()
    scenarios.sort()
    scenarios = scenarios[::-1]
    # labels location
    x = np.arange(len(xticks_labels))
    # the width of the bars
    total_width = 0.7
    width = total_width / len(scenarios)
    fig, axs = plt.subplots(1)
    fig.set_figheight(15)
    fig.set_figwidth(60)
    fig.tight_layout()
    # get x and y for each scenario and type
    for i,scene in enumerate(scenarios) :
        temp = norm_data.loc[norm_data['scenario'] == scene]
        mean = temp['norm_val_percent'].values
        std = temp['norm_std_percent'].values
        bar_base_loc = x - total_width/2
        bar_loc = bar_base_loc + ((i + 1) * width) - (width/2)
        hbars = axs.bar(bar_loc, mean, width, label=scene)
        axs.errorbar(bar_loc, mean, yerr=std, xerr=None, fmt='', capsize=3, color='black', linestyle='')
        # Add some text for labels, title and custom x-axis tick labels, etc.
        axs.margins(x=0)
        axs.set_ylabel('Relative performance (%)',fontsize=35)
        axs.set_xlabel('Events',fontsize=35)
        if i == 0:
            labels = temp['count'].values
            labels =['%.2f' % l for l in labels]
            axs.bar_label(hbars, labels=labels, label_type='edge', rotation=90, padding=18,fontsize=35)
        axs.set_title(dataset)
        axs.set_xticks(x, xticks_labels,rotation=45,fontsize=35)
        axs.legend(fontsize=35)
        axs.set_ylim([70, 1000])
    # set the spacing between subplots
    plt.subplots_adjust(top=0.935,
                        bottom=0.250,
                        left=0.045,
                        right=0.995,
                        hspace=0.34,
                        wspace=0.22)
    pdf.savefig(fig)
plot_bw_bench(dat)
#datasets = event['dataset'].unique()
#for i,sets in enumerate(datasets) :
##    temp = event.loc[event['dataset'] == sets]
#   plot_event_bench(temp,sets)

#sns.catplot(x="dataset", y="norm_val_percent", hue="scenario", kind="bar", data=norm_data)
pdf.close()
#plt.show()
