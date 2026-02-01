"""Graph generator"""
from typing import Tuple, Union
import numpy as np
import numpy.typing as npt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.typing as mplt
from matplotlib import figure, axes

__all__ = [
    "graph_setup"
]


def graph_setup(
    style: str,
    *args,
    **kwargs
) -> Tuple[
    figure.Figure,
    Union[
        axes.Axes,
        Tuple[
            axes.Axes, ...
        ],
        Tuple[
            Tuple[
                axes.Axes, ...
            ], ...
        ]
    ]
]:
    """Sets up the graph.

    Parameters
    ----------
    style : str
        The name of style.
    *args
        Arguments handed to ``plt.subplots()``.
    **kwargs
        Keyword arguments handed to ``subplots()``.

    Returns
    -------
    fig : Figure
        A ``Figure`` returned by ``plt.subplots``.
    axs : ``Axes`` or array of ``Axes``
        The returned ``Axes`` instances.
    """
    plt.style.use(style)
    return plt.subplots(*args, **kwargs)
