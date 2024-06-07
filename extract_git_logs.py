import os
from datetime import datetime

HISTORY_FILE_EXT = ".log"
CODE_ANALYSIS_DIR = "code-analysis"

# Function to create a directory if it does not exist
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to extract the git history logs of each repo and prepend their names to the filenames in the log entries
def extract_git_logs(repos, output_dir):
    for repo in repos:
        # Print the repo directory we're trying to extract git logs for
        print(f"Getting logs for: {repo}")

        # Change to the git repository directory
        os.chdir(repo)

        # Run our git log command here and capture the output
        output = os.popen("git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames").read() #--after=YYYY-MM-DD

        # Create a file to store the output in the original directory
        output_file = os.path.join(output_dir, repo + HISTORY_FILE_EXT)
        with open(output_file, "w") as f:
            for line in output.splitlines():
                parts = line.split()
                
                # Prepend the repo name to the file paths
                if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                    added_lines = parts[0]
                    removed_lines = parts[1]
                    file_path = parts[2]
                    
                    new_file_path = os.path.join(repo, file_path)
                    line = f"{added_lines}\t{removed_lines}\t{new_file_path}"
                    
                f.write(line + '\n')

        # Change back to the original directory
        os.chdir("..")

# Function to combine the individual git log files for each repo into one big, combined history log file
def combine_history(logs_dir, output_dir, timestamp):
    combined_hist_output_file = f"{output_dir}/combined-repo-history_{timestamp}.log"
    print(f"Combining '{HISTORY_FILE_EXT}' files from '{logs_dir}' to file '{combined_hist_output_file}'")
    
    # Pick the files based on file extension
    file_paths = [os.path.join(logs_dir, file_name) for file_name in os.listdir(logs_dir) if file_name.endswith(HISTORY_FILE_EXT)]

    # Use the maat-scripts combine repos python script
    combine_repos_script = f"./{CODE_ANALYSIS_DIR}/maat-scripts/combine-repos/combine_repos.py"
    command = f"{combine_repos_script} {' '.join(file_paths)} --output {combined_hist_output_file}"
    print(f"Running command: {command}")
    os.system(command)


# Main function
def main():
    # Get the current working directory
    base_dir = os.getcwd()
    print(f"Current working directory: {base_dir}")
    
    # Get the current timestamp and format it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Our list of repos to analyse for the project
    repos = [
        "content-storage",
        "import-services",
        "product-publishing-pipeline",
        "publishing-system-frontend",
        "relational-content-processing-microservice"
    ]

    # Extract the logs into one directory
    git_logs_dir = f"{CODE_ANALYSIS_DIR}/git-logs"

    # Create the destination directory if it does not exist
    create_directory(git_logs_dir)

    # Create an output folder
    output_dir = os.path.join(base_dir, git_logs_dir, timestamp)
    create_directory(output_dir)
    print(f"Output directory: {output_dir}")

    print(f"Extracting git history logs to '{output_dir}' for each repo")
    extract_git_logs(repos, output_dir)

    print(f"Combining git log files from '{output_dir}'")
    combine_history(output_dir, git_logs_dir, timestamp)


if __name__ == "__main__":
    main()