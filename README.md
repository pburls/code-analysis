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
2. The custom `extract_git_logs.py` script.

### Extract code change history from Git logs
Next we need to extract all the code change history from the all the git repos in this project using the following helper Python script.

Assuming you are in you project root directory, run the following command:
```sh
$ python code-analysis/extract_git_logs.py
```