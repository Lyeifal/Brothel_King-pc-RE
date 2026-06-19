#### Standard library imports for Ren'Py environment ####
## This file restores the 'python early:' imports that were originally
## in functions.rpy before it was split into focused modules.

python early:
    import os
    import sys
    import random
    import math
    from math import prod
    import copy
    import configparser
    import ast
    from collections import defaultdict
    import operator
    from fractions import Fraction
    from collections import OrderedDict
    import threading
    import re
    import time

    import gc
