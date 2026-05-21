# DevTracker — GitHub User Analyzer

DevTracker is a production-ready Command Line Interface (CLI) application built in Python that analyzes any public GitHub profile. It aggregates user statistics and calculates a custom developer activity score, delivering actionable insights directly in the terminal.

## Features
- Profile Summary: Fetches base user profile details safely.
- Repository Analytics: Aggregates total stars, forks, and identifies the user's top 3 programming languages.
- Custom Activity Metric: Calculates a custom score to evaluate overall developer engagement based on weighted metrics.
- Resilient Architecture: Implements production-level input validation, custom timeout constraints, and robust API error management.

## Installation & How to Run

Follow these steps to set up and run the project on a fresh machine:

# Clone the repository
```bash
git clone https://github.com/sefimiakanda/devtracker-github-analyzer.git
cd devtracker-github-analyzer

# Set up a virtual environment

python -m venv venv
source venv/Scripts/activate

# Install required dependencies

pip install -r requirements.txt

# Execute the application

python main.py