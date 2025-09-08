To install the Macaulay2 Jupyter kernel and start Jupyter, run the following.  Note that Macaulay2 should already be installed on your system.

```
mkdir m2-jupyter
python3 -m venv m2-jupyter
source m2-jupyter/bin/activate
pip install git+https://github.com/Macaulay2/Macaulay2-Jupyter-Kernel
python3 -m m2_kernel.install
jupyter lab
```

At this point, your web browser should open with an instance of JupyterLab.  Click on the "M2" icon to open up to a new Macaulay2 notebook.

After it's installed, then further sessions only need the following:

```
source m2-jupyter/bin/activate
jupyter lab
```

Try out one of the following to change to a "prettier" output mode:

```m2
--%mode=webapp
```

```m2
--%mode=texmacs
```

See also [this demo notebook](https://nbviewer.org/urls/nbviewer.org/github/Macaulay2/Macaulay2-Jupyter-Kernel/blob/master/demo/demo.ipynb) and the [kernel git repository](https://github.com/Macaulay2/Macaulay2-Jupyter-Kernel).