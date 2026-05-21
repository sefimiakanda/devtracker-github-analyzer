import sys
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def fetch_github_user(username: str):
    """
    Fetch profile data for a given GitHub username.
    """
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        console.print("[bold red]Error: Request timed out. Please try again later.[/bold red]")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            console.print(f"[bold yellow]User '{username}' not found.[/bold yellow]")
        else:
            console.print(f"[bold red]Error: Server returned status code {e.response.status_code}.[/bold red]")
        sys.exit(1)
    except requests.exceptions.RequestException:
        console.print("[bold red]Network error: Failed to connect to GitHub.[/bold red]")
        sys.exit(1)

def fetch_user_repos(username: str):
    """
    Fetch all public repositories for a given GitHub username.
    """
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        console.print("[bold red]Error: Failed to fetch repositories.[/bold red]")
        sys.exit(1)

def analyze_developer_data(user_data: dict, repos: list):
    """
    Process raw repository data to calculate custom statistics and activity score.
    """
    public_repos_count = user_data.get("public_repos", 0)
    
    # EDGE CASE: Handling users with zero public repositories
    if not repos or public_repos_count == 0:
        return {
            "top_languages": [],
            "most_popular_repo": "N/A",
            "total_stars": 0,
            "total_forks": 0,
            "activity_score": 0
        }

    total_stars = 0
    total_forks = 0
    languages_count = {}
    most_popular_repo = repos[0]

    for repo in repos:
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        total_stars += stars
        total_forks += forks

        if stars > most_popular_repo.get("stargazers_count", 0):
            most_popular_repo = repo

        lang = repo.get("language")
        if lang:
            languages_count[lang] = languages_count.get(lang, 0) + 1

    sorted_languages = sorted(languages_count.items(), key=lambda x: x[1], reverse=True)
    top_languages = [lang[0] for lang in sorted_languages[:3]]

    # Custom metric calculation
    activity_score = (total_stars * 3) + (total_forks * 2) + public_repos_count

    return {
        "top_languages": top_languages,
        "most_popular_repo": most_popular_repo.get("name", "N/A"),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "activity_score": activity_score
    }

def display_results(username: str, user_data: dict, stats: dict):
    """
    Render analysis metrics using a clean, professional terminal table layout.
    """
    console.print(Panel(f"[bold branch]DevTracker Analysis: {username}[/bold branch]", expand=False))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", width=25)
    table.add_column("Value", style="white")

    table.add_row("Full Name", user_data.get('name', 'N/A'))
    table.add_row("Public Repositories", str(user_data.get('public_repos', 0)))
    table.add_row("Total Stars", str(stats['total_stars']))
    table.add_row("Total Forks", str(stats['total_forks']))
    table.add_row("Most Popular Repo", stats['most_popular_repo'])
    table.add_row("Top Languages", ", ".join(stats['top_languages']) if stats['top_languages'] else "N/A")
    table.add_row("Custom Activity Score", f"[bold green]{stats['activity_score']}[/bold green]")

    console.print(table)
    console.print("\n")

def main():
    console.print("[bold blue]DevTracker — GitHub User Analyzer[/bold blue]\n")
    
    username = input("Enter GitHub username to analyze: ").strip()
    if not username:
        console.print("[bold red]Error: Username cannot be empty.[/bold red]")
        sys.exit(1)
        
    console.print(f"\nFetching data for {username}...")
    
    user_data = fetch_github_user(username)
    repos_data = fetch_user_repos(username)
    stats = analyze_developer_data(user_data, repos_data)
    
    print("") # Spacer
    display_results(username, user_data, stats)

if __name__ == "__main__":
    main()