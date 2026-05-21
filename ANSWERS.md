# Assessment Answers

### 1. How to run
To run this project on a fresh machine, execute the following commands in order:
```bash
git clone https://github.com/sefimiakanda/devtracker-github-analyzer.git
python -m venv venv
source venv/bin/activate  #On Windows
pip install -r requirements.txt
python main.py
```

### 2. Stack choice
Chosen Stack: Python 3.x (with requests and rich libraries).

Justification: Python was selected because it is optimal for quick, lightweight CLI scripting. The requests library provides straightforward, synchronous HTTP management required for sequential API queries. The rich library ensures clean, human-readable terminal rendering via robust data framing without overhead.

Worse Choice: C++ or Java would have been a significantly worse choice. They introduce verbose boilerplate for HTTP requests, require heavy build configurations (like Maven/Gradle or CMake), and make JSON parsing unnecessarily complex for a single-file pipeline task.

### 3. One real edge case
The Edge Case: A GitHub user who has 0 public repositories or whose repository payload returns empty.

Location: File main.py, Lines 43-52 (inside analyze_developer_data).

Handling & Consequence: Without explicit handling, iterating over an empty repository list or attempting to calculate metrics would cause runtime errors or empty state collisions when reading repos[0]. The code explicitly intercepts this condition early, short-circuits the pipeline, and safely returns a normalized dictionary payload with structured default values (N/A and 0), preventing application crashes.

### 4. AI usage
Tool used: ChatGPT / Gemini.

Prompting: Guided the iterative development steps, boilerplate layout generation, and standardizing the exception blocks for requests.

Modifications made: The initial AI code output included excessive cosmetic styling, verbose conversational logging, and emoji outputs. I removed all emojis, refactored every console string and structural code comment into clean, formal English, and stripped back decorative terminal blocks to enforce professional codebase aesthetics suitable for an enterprise engineering submission.

### 5. Honest gap
The Gap: The current implementation does not support pagination for users with more than 100 repositories. The API client enforces a hard limit via per_page=100.

The Solution: Given another day, I would rewrite fetch_user_repos to inspect the HTTP Link header in the GitHub API response and implement a while loop to follow next-page pagination tokens until all repositories are fetched, guaranteeing absolute analytical accuracy for high-profile developer accounts.