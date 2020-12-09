<div align="center">
  <a href="https://github.com/andrewtavis/stdviz"><img src="https://raw.githubusercontent.com/andrewtavis/stdviz/master/resources/stdviz_logo_transparent.png" width="552" height="235"></a>
</div>

--------------------------------------

[![PyPI Version](https://badge.fury.io/py/stdviz.svg)](https://pypi.org/project/stdviz/)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/stdviz/)
[![GitHub](https://img.shields.io/github/license/andrewtavis/stdviz.svg)](https://github.com/andrewtavis/stdviz/blob/master/LICENSE)

### Standardized vizualization and object display in Python

**Jump to:** [View](#view) • [Plot](#plot) • [To-Do](#to-do)

**stdviz** is a Python package for standardized visualization. Routine and novel plotting approaches are formatted to allow for easy variation while providing quick and exact results. Helper functions for easier object display are also included.

# Installation via PyPi
```bash
pip install stdviz
```

```python
import stdviz
```

# View

[stdviz.view](https://github.com/andrewtavis/stdviz/blob/main/stdviz/view.py) contains helper functions to make object display easier.

```python
import pandas as pd
from stdviz.view import disp # a version of display that allows for dimension inputs

a_dict = {'a': 1, 'b': 2, 'c': 3}
disp(a_dict, 2) # number of key-value pairs
# {'a': 1, 'b': 2}

df = pd.DataFrame(dict(zip('ABCDE', range(1, 6))), range(4))
disp(df, 2, 3) # length and width
```
|   A |   B |   C |
|----:|----:|----:|
|   1 |   2 |   3 |
|   1 |   2 |   3 |

Also included are simple tools to make things a bit more readable:

```python
from stdviz.view import add_num_commas

add_num_commas(1234567.89)
# '1,234,567.89'
```

# Plot

Plotting methods within [stdviz/plot](https://github.com/andrewtavis/stdviz/tree/main/stdviz/plot) are tailored to provide quick results for staples of data visualization while at the same time including unique and novel tools. See [examples/plotting](https://github.com/andrewtavis/stdviz/blob/main/examples/plotting.ipynb) for all plotting styles that seamlessly combine graphing functions of seaborn, matplotlib, and pandas.

Examples of standard plotting made easy are:



Specifically for election analysis, stdviz provides a Python only implementation of parliament plots:

```python
import matplotlib.pyplot as plt
import stdviz

seat_allocations = [26, 9, 37, 12, 23, 5]
# German political parties
parties = ['CDU/CSU', 'FDP', 'Greens', 'Die Linke', 'SPD', 'AfD']
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']
```

```python
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

ax1 = stdviz.plot.parliament(seat_counts=seat_allocations, 
                             names=parties, colors=party_colors, 
                             style='rectangle', num_rows=4, marker_size=300, 
                             speaker=True, df_seat_lctns=None, axis=ax1)

ax2 = stdviz.plot.parliament(seat_counts=allocations, 
                             names=parties, colors=party_colors, 
                             style='semicircle', num_rows=4, marker_size=175, 
                             speaker=False, df_seat_lctns=None, axis=ax2)

plt.show()
#
```

A further novel addition to social science analysis is the **disproportionality bar plot**, which graphically depicts the disproportionality between expected and realized results. Bar widths are the proportion of shares (ex: votes received), and heights are the difference or relative difference between shares and allocations (ex: parliament seats received). 

An example follows:

```python
# Using the same variables from above
votes = [2700, 900, 3300, 1300, 2150, 500]

ax = stdviz.plot.dispr_bar(shares=votes, allocations=seat_allocations,
                           names=parties, colors=party_colors, 
                           total_shares=None, total_alloc=None,
                           percent_change=True, axis=None)

handles, labels = stdviz.plot.legend.gen_elements(counts=[round(v/sum(votes), 4) for v in votes], 
                                                  names=parties, colors=party_colors, 
                                                  size=15, marker='o', padding_indexes=None,
                                                  order=None)

ax.legend(handles=handles, labels=labels,
          title='Vote Percents (bar widths)', 
          title_fontsize=20, fontsize=15, 
          ncol=2, loc='top left', bbox_to_anchor=(0, 1), 
          frameon=False, facecolor='#ffffff', framealpha=1)

ax.axes.set_title('Seat-Share Disproportionality', fontsize=30)
ax.set_xlabel('Groups', fontsize=20)
ax.set_ylabel('Percent Shift', fontsize=20)

plt.show()
```

# To-Do

- Adding further plotting variations
- Adding more object display functions
- Finishing accurate allocations in the semicircle variation of `stdviz.plot.parliament`
- Finishing the coloration on the outer ring of `stdviz.plot.pie`
- Allowing all plotting variations to be seamlessly plotted from either lists or dataframe columns