## Code Analysis using Code Maat

### Prerequisites
We assume you have a similar folder structure below with:
1. all the different project repos
2. a special `code-analysis` folder

```
.
├── code-analysis
├── content-storage
├── import-services
├── product-publishing-pipeline
├── publishing-system-frontend
└── relational-content-processing-microservice

```

Inside the `code-analysis` folder we expect the following scripts:
1. The entire [maat-scripts](https://github.com/adamtornhill/maat-scripts/tree/python3) repo of script cloned.
Check out the `python3` branch of the repo!
Also don't forget to install the python packages required by the scripts.
```sh
$ pip install -r requirements.txt
```

2. The custom `extract_git_logs.py` script

### Extract code change history from Git logs
Next we need to extract all the code change history from the all the git repos in this project using the following helper Python script.

Assuming you are in you project root directory, run the following command:
```sh
$ python code-analysis/extract_git_logs.py
```

### Running the code-maat analysis tool
#### Generating a summary of the code change history
```
java -jar code-analysis/code-maat-1.0.4-standalone.jar -l code-analysis/git-logs/<your log file here>.log -c git2 -a summary
```

#### Generating change frequency of files
```
java -jar code-analysis/code-maat-1.0.4-standalone.jar -l code-analysis/git-logs/<your log file here>.log -c git2 -a revisions
```

### Counting the lines of code in your project

Install the cloc tool: https://github.com/AlDanial/cloc?tab=readme-ov-file#install-via-package-manager

Run the following command in your project root directory:
```sh
$ cloc ./ --by-file --csv --quiet --report-file=maat_lines.csv --exclude-lang=SVG,JSON,CSV,XML,Text --exclude-dir=code-analysis,code
```
!warning! If the cloc command is taking a long time, it is likely due to npm `node_modules` folders inside some of your project repos. Please either delete these folders, checkout the repositories again or exclude them from the cloc command.

You can tweak the file types you want to exclude from your lines of code csv report by modifying the `--exclude-lang` flag.

You can also exclude directories from the cloc command by modifying the `--exclude-dir` flag.

## Merging the change frequency and lines of code data
Using the [merger pythons script](https://github.com/adamtornhill/maat-scripts/blob/python3/merge/merge_comp_freqs.py) in the maat-scripts repo, we can merge the change frequency data with the lines of code data.

```
python code-analysis/maat-scripts/merge/merge_comp_freqs.py revision.csv maat_lines.csv > hotspots-freq-comp.csv
```

## Generating and visualising the hotspots

### Generate json file for visualisation
First we need to generate a json file of all the files in the project and their lines of code.

To do this, we can use the following script in the maat-scripts transform folder:

```
python code-analysis/maat-scripts/transform/csv_as_enclosure_json.py --structure maat_lines.csv --weights hotspots-freq-comp.csv > code-analysis/maat-scripts/transform/hotspots.json
```

This will create a hotspots.json file in the transform folder for us to use with the d3 visualisation.

### Launch visualisation
We will use a python server in the maat-scripts transform folder to launch the visualisation.


```
cd code-analysis/maat-scripts/transform
python -m http.server 8888
```

Then you can browse to the following URL to see the visualisation:
http://localhost:8888/crime-scene-hotspots.html


## Complexity Trends over Time

### Generate complexity data for a module at the current time
Pick a hotspot module in your project to analyse from the visualisation. You can also find the module file path in the hotspots-freq-comp.csv file.

To generate a complexity trend over time, we can use the following command:

```
python code-analysis/maat-scripts/miner/complexity_analysis.py <file-to-analyse>
```

This should give you an output like:
```
n,total,mean,sd,max
1602,2035.0,1.27,0.95,6.0
```

### Generate complexity data for a module over time
To generate a complexity trend over time, we can use the following command:

```
cd <git repo>
python ../code-analysis/maat-scripts/miner/git_complexity_trend.py --start <start_git_revision>  --end <end_git_revision> --file <file-to-analyse>
```
- start_git_revision: The git revision hash of the start of the time period you want to analyse - use your git log file to find this towards the bottom. For the correct git repo!
- end_git_revision: The git revision hash of the end of the time period you want to analyse - use your git log file to find this towards the top. For the correct git repo!
- file-to-analyse: The file path of the module you want to analyse - exclude the git repo name from the path.
- git repo: The git repo the file you want to analyse is in