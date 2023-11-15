
GeoRunes
----------
[![License](https://img.shields.io/github/license/dugucrypter/georunes)]()

GeoRunes is a bunch of tools and classes written to generate geochemical diagrams using matplotlib. 

**georunes.plot** assits the representation of geochemical data in binary diagrams, ternary diagrams and normalized spider diagrams. It uses plotting parameters (category, color, marker, label ...) defined in the data source file along with geochemical data to construct the required figures.

**georunes.modmin** estimates the modal mineralogy of some whole rock compositions, provided a list of minerals with their composition.

## Features

- Data source supported formats: .csv, .xls or .xlsx,
- Data loaded as pandas DataFrames,
- Plotting parameters (color, marker, label, drawing order ...) configurable automatically (see examples/preprocess_files.py),
- Support scaling of axes, layout padding, adjusting figure ratio, transparency and size of markers, configuring legends,
- Chemical conversion from wt.% oxide to element (in millications or ppm),
- Ternary diagram (based on the package **python-ternary**),
- Inner geochemical normalization and multiple plotting style in spider diagrams,
- Handling of translations (using gettext, pass the lang_cfg parameter as a dict{'lang', 'domain' if different, 'locales' if different}),
- CIPW norm calculation and estimation (optimization) of modal mineralogy from whole rock and mineral compositions,
- Available methods for estimation of modal mineralogy : bounded-variable least squares, non-negative least squares, gradient descent, or a random research,
- Components of a solid solution can be fixed for estimation a mineralogy,

## Dependencies

- matplotlib
- pandas
- numpy
- scipy
- python-ternary

## Installation

* Install stable version with pip command:

        pip install georunes

* Install updated version from github:

        git clone https://github.com/dugucrypter/georunes.git
        cd georunes
        python setup.py install --user


This code was tested with **Python 3.11**, **matplotlib 3.7.2**, **pandas 2.1.0**, **numpy 1.24.3**, and **scipy 1.10.0**.

## Working with GeoRunes

### Short example

```python
import matplotlib.pyplot as plt
from georunes.plot.binary.versus import DiagramVs

# Initialize diagram class
diag_nb_ta = DiagramVs(datasource="path/to/data.xls", sheet="sheet1",
                       group_name='Category',  # Attribute used for categorization
                       xvar="Nb", yvar="Ta",  # Variables to plot
                       xlabel="Nb (ppm)", ylabel="Ta (ppm)",  # Labels to write in axes
                       xscale='log', yscale='log',  # Custom scaling
                       )

# Plot data
diag_nb_ta.plot()

# Show the figure
plt.show()
```

More examples with an arbitrary geochemical dataset are proposed in the \examples directory.

<img src="examples/preview.png">

## Roadmap

Supplementary whole-rocks and mineral-based geochemical diagrams will be added in the following versions. Long-term updates might provide utilities for geochemical modelling and normative mineralogy.

### Author

W.M.-E. Bonzi, 2021-2023.

### License

This work is under MIT License.