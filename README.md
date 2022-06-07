## Project Description

This project is an implementation to create an energy dataset. The dataset is created by a combination of individual computer resources written in logs and energy measurements data from physical probes received via REST API server.

To perform stimuli on the different devices, the Phoronix software has been used. Each test carried out puts different loads on the servers, so we combine this data with the energy measured by different physically connected energy probes.

After having this data available, the data is processed to create a dataset that can be used to train a machine learning model. We demonstrate the usefulness of these data through some graphs, observing the correlation between the features.

You can start from any step that you choose, but the datasets are already provided in the repository. There are individual ones, but also one combined with all the data collected from the last attempt of each test in the UPM laboratory.

## Getting started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

### Installation

Follow the next steps to install the project locally. You may need to install additional dependencies.

Some scripts are provided externally in other GitHub repositories.

#### Virtual environment
```bash
python -m venv venv
[Linux/Mac] source venv/bin/activate
[Windows] venv\Scripts\activate
```
#### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Follow the instructions to get the entire cycle of development up and running. You start extracting data to end with a final analysis.

1. Data extraction
   1. Start [REST API server](https://github.com/Kaiser-14/rest-api-server) using energy data (external repository)
   2. Run charge [Phoronix script](https://github.com/gic81/charge_script_dataset) (external repository)
   3. Launch [data_server.py](src/data_extraction/data_server.py) to extract data from server into txt file
2. Data processing
   1. Execute file [prep_csv_upm.py](src/data_preparation/prep_csv_upm.py) to create the CSV files (log_test_pfeX.csv) combining logs from server (server.txt) and terminal (log_test_pfeX.txt)
3. Data analysis
   1. [EDA](src/data_analysis/eda.py) to get initial insights
   2. Execute file [analysis_csv_upm.py](src/data_analysis/analysis_upm.py) to extract results in terms of plots
4. Data summarization
   1. Run [individual_plot.py](src/data_summarization/individual_plot.py) to get the plots for each metric
   2. Extract a summary per test using [summary.py](src/data_summarization/summary.py)

