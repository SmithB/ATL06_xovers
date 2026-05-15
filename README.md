# ATL06_xovers

This repo contains sample code for working with ATL06 crossover files that are generated as part of ATL11 production.  The example files are set up to work on NASA's discover cluster using shared data from the ICESat-2 project.  Please see find_outliers.ipynb in the notebooks directory.

To setup this repo, you can install the libraries needed for the notebooks by cloning the pointCollection repo, then installing the current repo.
To to this, run these commands in the ATL06_xovers directory:

 >> pushd ..; [ -d pointCollection ] || git clone https://github.com/SmithB/pointCollection.git; popd
 >> pip install -r requirements.txt


