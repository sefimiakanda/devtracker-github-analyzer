import sys
import requests
from rich.console import Console

console = Console()

def fetch_github_user(username: str):
    """
    Fetch profile data for a given GitHub username.
    Handles network timeouts, missing users, and API rate limiting.
    """
    url = f"https://api.github.com/users/{username}"
    
    try:
        # Request with a 5-second timeout to prevent the CLI from freezing
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        console.print("[bold red]Error: Request timed out. Please try again later.[/bold red]")
        sys.exit(1)
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 404:
            console.print(f"[bold yellow]User '{username}' not found. Please check the spelling.[/bold yellow]")
        elif status_code == 403:
            console.print("[bold red]Error: API rate limit exceeded.[/bold red]")
            console.print("[white]Please wait an hour or configure a GitHub Personal Access Token.[/white]")
        else:
            console.print(f"[bold red]Error: Server returned status code {status_code}.[/bold red]")
        
        sys.exit(1)
        
    except requests.exceptions.RequestException:
        console.print("[bold red]Network error: Failed to connect to GitHub. Check your internet connection.[/bold red]")
        sys.exit(1)

def main():
    console.print("[bold blue]DevTracker — GitHub User Analyzer[/bold blue]\n")
    
    # Input validation for empty strings or whitespace
    username = input("Enter GitHub username to analyze: ").strip()
    
    if not username:
        console.print("[bold red]Error: Username cannot be empty.[/bold red]")
        sys.exit(1)
        
    console.print(f"\nFetching data for {username}...\n")
    
    user_data = fetch_github_user(username)
    
    # Simple formatting for user data display
    console.print(f"[green]User data retrieved successfully.[/green]")
    console.print(f"Name: {user_data.get('name', 'N/A')}")
    console.print(f"Bio: {user_data.get('bio', 'N/A')}")
    console.print(f"Public Repositories: {user_data.get('public_repos', 0)}")

if __name__ == "__main__":
    main()