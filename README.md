<div align="center">
  <a href="https://github.com/andrewtavis/pltviz"><img src="https://raw.githubusercontent.com/andrewtavis/pltviz/main/resources/pltviz_logo_transparent.png" width=488 height=157></a>
</div>

--------------------------------------

[![rtd](https://img.shields.io/readthedocs/pltviz.svg?logo=read-the-docs)](http://pltviz.readthedocs.io/en/latest/)
[![ci](https://img.shields.io/github/workflow/status/andrewtavis/pltviz/CI?logo=github)](https://github.com/andrewtavis/pltviz/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/andrewtavis/pltviz/branch/main/graphs/badge.svg)](https://codecov.io/gh/andrewtavis/pltviz)
[![quality](https://img.shields.io/codacy/grade/df8099ad194f4b478ce3afd36643667f?logo=codacy)](https://app.codacy.com/gh/andrewtavis/pltviz/dashboard)
[![pyversions](https://img.shields.io/pypi/pyversions/pltviz.svg?logo=python&logoColor=FFD43B&color=306998)](https://pypi.org/project/pltviz/)
[![pypi](https://img.shields.io/pypi/v/pltviz.svg?color=4B8BBE)](https://pypi.org/project/pltviz/)
[![pypistatus](https://img.shields.io/pypi/status/pltviz.svg)](https://pypi.org/project/pltviz/)
[![license](https://img.shields.io/github/license/andrewtavis/pltviz.svg)](https://github.com/andrewtavis/pltviz/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/coc-Contributor%20Covenant-ff69b4.svg)](https://github.com/andrewtavis/pltviz/blob/main/.github/CODE_OF_CONDUCT.md)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![colab](https://img.shields.io/badge/%20-Open%20in%20Colab-097ABB.svg?logo=google-colab&color=097ABB&labelColor=525252)](https://colab.research.google.com/github/andrewtavis/pltviz)

### Standardized plots and visualizations in Python

**pltviz** is a Python package for standardized visualization. Routine and novel plotting approaches are formatted to allow for easy variation while providing quick and exact results. Coloration functions are also included for precise colors across plots and to assure that all functions can be ran with color hexes.

# **Contents**<a id="contents"></a>
- [plot](#plot)
- [To-Do](#to-do)

# Installation

pltviz can be downloaded from PyPI via pip or sourced directly from this repository:

```bash
pip install pltviz
```

```bash
git clone https://github.com/andrewtavis/pltviz.git
cd pltviz
python setup.py install
```

```python
import pltviz
```

# plot [`↩`](#contents) <a id="plot"></a>

Plotting methods within [pltviz](https://github.com/andrewtavis/pltviz/tree/main/pltviz) are tailored to provide quick results for staples of data visualization.

See [examples/plot](https://github.com/andrewtavis/pltviz/blob/main/examples/plot.ipynb) for all plotting styles that seamlessly combine graphing functions of seaborn, matplotlib, and pandas.

```python
import matplotlib.pyplot as plt
import pltviz
```

Examples of routine plotting techniques made easy are:

```python
# The following will be used for the remaining examples

# German political parties
parties = ['CDU/CSU', 'FDP', 'Greens', 'Die Linke', 'SPD', 'AfD']
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']

# Hypothetical seat allocations to the Bundestag (German parliament)
seat_allocations = [26, 9, 37, 12, 23, 5]
```

The following shows [pltviz.bar](https://github.com/andrewtavis/pltviz/blob/main/pltviz/bar.py) that allows all common options to be selected as binaries:

```python
# Bar plot options such as stacked and label bars are booleans
ax = pltviz.bar(
    counts=seat_allocations,
    labels=parties,
    colors=party_colors,
    horizontal=False,
    stacked=False,
    label_bars=True,
)

# Initialize empty handles and labels
handles, labels = pltviz.legend.gen_elements()

# Add a majority line
ax.axhline(int(sum(seat_allocations) / 2) + 1, ls="--", color="black")
handles.insert(0, Line2D([0], [0], linestyle="--", color="black"))
labels.insert(0, "Majority: {} seats".format(int(sum(seat_allocations) / 2) + 1))

ax.legend(
    handles=handles,
    labels=labels,
    title="Bundestag: {} seats".format(sum(seat_allocations)),
    loc="upper left",
    bbox_to_anchor=(0, 0.9),
    title_fontsize=20,
    fontsize=15,
    frameon=True,
    facecolor="#FFFFFF",
    framealpha=1,
)

ax.set_ylabel("Seats", fontsize=15)
ax.set_xlabel("Party", fontsize=15)
```
<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/pltviz/main/resources/gh_images/bar.png" width="600" />
</p>

Also included is a [pltviz.semipie](https://github.com/andrewtavis/pltviz/blob/main/pltviz/semipie.py) via matplotlib artists for cases where a simple and condensed plot is needed:

```python
ax = pltviz.semipie(counts=seat_allocations, colors=party_colors, donut_ratio=0.5)

handles, labels = pltviz.legend.gen_elements(
    counts=seat_allocations,
    labels=parties,
    colors=party_colors,
)

ax.legend(
    handles=handles,
    labels=labels,
    title="Bundestag: {} seats".format(sum(seat_allocations)),
    title_fontsize=20,
    fontsize=14,
    ncol=2,
    loc="center",
    bbox_to_anchor=(0.5, 0.17),
    frameon=False,
    facecolor="#FFFFFF",
    framealpha=1,
)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/pltviz/main/resources/gh_images/semipie.png" width="600" />
</p>

pltviz also includes specialized plots such as [pltviz.gini](https://github.com/andrewtavis/pltviz/blob/main/pltviz/gini.py) to visualize [gini coefficients](https://en.wikipedia.org/wiki/Gini_coefficient) of inequality:

```python
global_gdp_deciles = [0.49, 0.59, 0.69, 0.79, 1.89, 2.55, 5.0, 10.0, 18.0, 60.0]

ax, gini_coeff = pltviz.gini(shares=global_gdp_deciles)

handles, labels = pltviz.legend.gen_elements(labels=["Lorenz Curve", "Perfect Equality"])

ax.legend(
    handles=handles,
    labels=labels,
    loc='upper left',
    bbox_to_anchor=(0, 0.9),
    fontsize=20,
    frameon=True,
    facecolor='#FFFFFF',
    framealpha=1)

ax.set_title(f'Gini: {gini_coeff}', fontsize=20)
ax.set_ylabel('Cuumlative Share of Global GDP', fontsize=15)
ax.set_xlabel('Income Deciles', fontsize=15)

plt.show()
```

<p align="middle">
  <img src="https://raw.githubusercontent.com/andrewtavis/pltviz/main/resources/gh_images/gini.png" width="600" />
</p>

# To-Do [`↩`](#contents) <a id="to-do"></a>

Please see the [contribution guidelines](https://github.com/andrewtavis/pltviz/blob/main/.github/CONTRIBUTING.md) if you are interested in contributing to this project. Work that is in progress or could be implemented includes:

- Adding standardized examples of further plots and visualizations

- Finishing the coloration on the outer ring of [pltviz.pie](https://github.com/andrewtavis/pltviz/tree/main/pltviz/plot/pie)

- Improving [tests](https://github.com/andrewtavis/pltviz/tree/main/tests) for greater [code coverage](https://codecov.io/gh/andrewtavis/pltviz)

- Improving [code quality](https://app.codacy.com/gh/andrewtavis/pltviz/dashboard) by refactoring large functions and checking conventions

- Allowing all plotting variations to be seamlessly plotted from either lists or dataframe columns where applicable
