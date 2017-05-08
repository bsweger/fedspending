# U.S. Federal Spending Scripts

On May 2014, President Obama signed the Digital Accountability and Transparency Act of 2014 (DATA Act) ([P.L. 113-101](https://www.gpo.gov/fdsys/pkg/PLAW-113publ101/pdf/PLAW-113publ101.pdf)) into law. As a result, U.S. federal agencies have started to report standardized data about their spending to the U.S. Department of the Treasury. This standardized data is surfaced via a beta API and a beta version of USAspending.gov

My day job involves working on the DATA Act, but everything in this repo has been done in my personal
capacity (_i.e._, unrelated to official government work). I'm a taxpayer eager to dive into the new data--especially the account-level data, which exposes entire areas of spending never before available in a convenient, unified format.

Everything here is obtainable via publicly-available resources.

## Setup Instructions (WIP)

### Show me the data

If you want to view the projects' data without running the scripts that create it:

1. The output .csv files are in the `data` folder.
2. Coming soon? A Jupyter notebook or two?

### Run the scripts

If you want to stand up a local Python development environment to run the scripts yourself:

1. Install the [miniconda Python package manager](http://conda.pydata.org/miniconda.html)

2. From a terminal, clone this project repository to your local machine:
        git clone git@github.com:bsweger/fedspending-scripts.git

3. If you don't have a GitHub account and want to get a read-only version of the code, use this command instead:
        git clone git://github.com/bsweger/fedspending-scripts.git

4. Change to the project directory:

        cd fedspending-scripts

5. Install Python and dependencies into a conda virtual environment called `fedspending-scripts`.

        conda env create
