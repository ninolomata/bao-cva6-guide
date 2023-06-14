from os import wait
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re
from matplotlib.ticker import PercentFormatter
import argparse
import sys

rootdir = os.getcwd()
parentdir = os.path.abspath("..")
print(parentdir)
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        mibench_dir = d + "/mibench/"
        os.system("python3 " + rootdir + "/mibench_plot.py" + " " + mibench_dir + " " + file + " " + parentdir)