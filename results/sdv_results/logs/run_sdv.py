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
        sdv_dir = d + "/sdv/"
        os.system("python3 " + rootdir + "/sdv_plot.py" + " " + sdv_dir + " " + file + " " + parentdir)