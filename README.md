<div align="center">
  <a href="https://github.com/andrewtavis/stdviz"><img src="https://raw.githubusercontent.com/andrewtavis/stdviz/master/resources/stdviz_logo_transparent.png" width="552" height="235"></a>
</div>

--------------------------------------

[![PyPI Version](https://badge.fury.io/py/stdviz.svg)](https://pypi.org/project/stdviz/)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/stdviz/)
[![GitHub](https://img.shields.io/github/license/andrewtavis/stdviz.svg)](https://github.com/andrewtavis/stdviz/blob/master/LICENSE)

### Standardized vizualization in Python

**Jump to:** [Plot](#plot) • [Advanced](#advanced) • [Standard](#standard) • [Novel](#novel) • [To-Do](#to-do)

**stdviz** is a Python package for standardized visualization. Advanced, routine and novel plotting approaches are formatted to allow for easy variation while providing quick and exact results. In short, this package provides plotting templates.

# Installation via PyPi
```bash
pip install stdviz
```

```python
import stdviz
```

# Plot

Plotting methods within [stdviz/plot](https://github.com/andrewtavis/stdviz/tree/main/stdviz/plot) are tailored to provide quick results for staples of data visualization while at the same time including unique and novel tools. 

### Advanced

Advanced standardized plots include t-SNE dimensional reduction for [Latent Dirichlet allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) models ran over a provided text corpus:

```python
corpus = [['corpus', 'of'], ['text', 'tokens']]

fig = stdviz.plot.t_sne(dimension='both', # 3D and 2D dimensional reduction
                        corpus=corpus, 
                        num_topics=10,
                        remove_3d_outliers=True)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/t_sne.png" width="600" />
</p>

### Routine

See [examples/plotting](https://github.com/andrewtavis/stdviz/blob/main/examples/plotting.ipynb) for all plotting styles that seamlessly combine graphing functions of seaborn, matplotlib, and pandas. 

Examples of routine plotting techniques made easy are:

```python
import matplotlib.pyplot as plt
import stdviz

# German political parties
parties = ['CDU/CSU', 'FDP', 'Greens', 'Die Linke', 'SPD', 'AfD']
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']

# Hypothetical seat allocations to the Bundestag (German parliament)
seat_allocations = [26, 9, 37, 12, 23, 5]
```

```python
# Bar plot options such as stacked and label bars are booleans
ax = stdviz.plot.bar(counts=seat_allocations, names=parties, 
                     faction_names=None, colors=party_colors, 
                     horizontal=False, stacked=False, 
                     label_bars=True, axis=None)

# Initialize empty handles and labels
handles, labels = stdviz.plot.legend.gen_elements()

# Add a majority line
ax.axhline(int(sum(seat_allocations)/2)+1, ls='--', color='black')
handles.insert(0, Line2D([0], [0], linestyle='--', color='black'))
labels.insert(0, 'Majority: {} seats'.format(int(sum(seat_allocations)/2)+1))

ax.legend(handles=handles, labels=labels,
          title='Bundestag: {} seats'.format(sum(seat_allocations)),
          loc='upper left', bbox_to_anchor=(0, 0.9),
          title_fontsize=20, fontsize=15, 
          frameon=True, facecolor='#FFFFFF', framealpha=1)

ax.set_ylabel('Seats', fontsize=15)
ax.set_xlabel('Party', fontsize=15)
```
<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/bar.png" width="600" />
</p>

```python
ax = stdviz.plot.semipie(counts=seat_allocations,
                         colors=party_colors, 
                         donut_ratio=0.5)

handles, labels = stdviz.plot.legend.gen_elements(counts=seat_allocations, names=parties, 
                                                  colors=party_colors, size=15, 
                                                  marker='o', padding_indexes=None,
                                                  order=None)

ax.legend(handles=handles, labels=labels,
          title='Bundestag: {} seats'.format(sum(seat_allocations)), 
          title_fontsize=20, fontsize=14, 
          ncol=2, loc='center', bbox_to_anchor=(0.5, 0.17), 
          frameon=False, facecolor='#ffffff', framealpha=1)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/semipie.png" width="600" />
</p>

### Novel

Specifically for election analysis, stdviz provides a Python only implementation of parliament plots:

```python
# Using the same variables from above
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

ax1 = stdviz.plot.parliament(seat_counts=seat_allocations, 
                             names=parties, colors=party_colors, 
                             style='rectangle', num_rows=4, marker_size=300, 
                             speaker=True, df_seat_lctns=None, axis=ax1)

ax2 = stdviz.plot.parliament(seat_counts=seat_allocations, 
                             names=parties, colors=party_colors, 
                             style='semicircle', num_rows=4, marker_size=175, 
                             speaker=False, df_seat_lctns=None, axis=ax2)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/rectangle_parliament.png" width="400" />
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/semicircle_parliament.png" width="400" /> 
</p>

A further novel addition to social science analysis is the [disproportionality bar plot](https://github.com/andrewtavis/stdviz/tree/main/stdviz/plot/disp_bar), which graphically depicts the disproportionality between expected and realized results. Bar widths are the proportion of shares (ex: votes received), and heights are the difference or relative difference between shares and allocations (ex: parliament seats received). 

An example follows:

```python
# Using the same variables from above
votes = [2700, 900, 3300, 1300, 2150, 500]

ax = stdviz.plot.dispr_bar(shares=votes, 
                           allocations=allocations,
                           names=parties, 
                           colors=party_colors, 
                           total_shares=None, 
                           total_alloc=None,
                           percent=True, 
                           axis=None)

handles, labels = stdviz.plot.legend.gen_elements(counts=[round(v/sum(votes), 4) for v in votes], 
                                                  names=parties, colors=party_colors, 
                                                  size=11, marker='o', padding_indexes=None,
                                                  order=None)

ax.legend(handles=handles, labels=labels,
          title='Vote Percents (bar widths)', 
          title_fontsize=15, fontsize=11, 
          ncol=2, loc='upper left', bbox_to_anchor=(0, 1), 
          frameon=True, facecolor='#ffffff', framealpha=1)

ax.axes.set_title('Seat to Vote Share Disproportionality', fontsize=30)
ax.set_xlabel('Groups', fontsize=20)
ax.set_ylabel('Percent Shift', fontsize=20)

plt.show()
```
<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/stdviz/main/resources/gh_images/dispr_bar.png" width="600" />
</p>

# To-Do

- Adding further plotting variations
- Finishing accurate allocations in the semicircle variation of `stdviz.plot.parliament`
- Finishing the coloration on the outer ring of `stdviz.plot.pie`
- Allowing all plotting variations to be seamlessly plotted from either lists or dataframe columns