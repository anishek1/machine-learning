#!/usr/bin/env python3
"""
GitHub Contribution Graph Greener 🌱
====================================
Generates realistic backdated commits for a Machine Learning learning repository.
Makes your GitHub contribution graph look active with authentic-looking commit messages.

Usage:
    python green_graph.py --commits 50 --days 90
    python green_graph.py --commits 100 --days 180 --dry-run
"""

import subprocess
import random
import argparse
from datetime import datetime, timedelta
import os


# ============================================================================
# REALISTIC ML LEARNING COMMIT MESSAGES
# ============================================================================
# These are organized by topic to match your repository structure

COMMIT_MESSAGES = {
    "python_basics": [
        "feat: add notes on Python data types and type conversion",
        "docs: document list comprehension examples",
        "feat: implement practice exercises for loops and conditionals",
        "fix: correct indentation in function examples",
        "docs: add comments explaining lambda functions",
        "feat: create dictionary manipulation practice notebook",
        "refactor: clean up variable naming in basics module",
        "docs: add docstrings to helper functions",
        "feat: implement OOP concepts with class examples",
        "fix: resolve scope issues in nested function examples",
    ],
    "file_handling": [
        "feat: add file reading and writing examples",
        "docs: document context manager usage with 'with' statement",
        "feat: implement CSV file parsing practice",
        "fix: handle file encoding issues in read operations",
        "feat: add JSON file handling examples",
        "docs: explain binary vs text mode file operations",
        "refactor: improve error handling in file operations",
        "feat: create file path manipulation utilities",
    ],
    "data_manipulation": [
        "feat: add NumPy array operations notebook",
        "docs: document array slicing and indexing techniques",
        "feat: implement data cleaning functions",
        "fix: handle missing values in data transformation",
        "feat: add string manipulation for data prep",
        "docs: explain broadcasting in NumPy operations",
        "refactor: optimize data transformation pipeline",
        "feat: create data validation helper functions",
    ],
    "pandas": [
        "feat: add DataFrame creation and manipulation examples",
        "docs: document groupby operations with aggregations",
        "feat: implement data filtering and selection methods",
        "fix: resolve dtype issues in column operations",
        "feat: add merge and join operations practice",
        "docs: explain multi-index DataFrames",
        "refactor: optimize DataFrame operations for performance",
        "feat: create pivot table and crosstab examples",
        "fix: handle NaN values in aggregation functions",
        "docs: add notes on method chaining in pandas",
    ],
    "visualization": [
        "feat: add matplotlib basic plotting examples",
        "docs: document figure and axes customization",
        "feat: implement subplots and grid layouts",
        "fix: adjust figure sizing for better visibility",
        "feat: add histogram and distribution plots",
        "docs: explain color maps and styling options",
        "refactor: create reusable plotting functions",
        "feat: implement scatter plots with regression lines",
        "fix: resolve legend positioning issues",
        "docs: add annotations and text formatting examples",
    ],
    "seaborn": [
        "feat: add seaborn statistical visualization examples",
        "docs: document heatmap creation for correlations",
        "feat: implement categorical data plotting",
        "fix: adjust color palette for better contrast",
        "feat: add pair plots for multivariate analysis",
        "docs: explain FacetGrid usage for complex plots",
        "refactor: standardize plot styling across notebooks",
        "feat: create violin and box plot comparisons",
    ],
    "sql_sqlite": [
        "feat: add SQLite database connection examples",
        "docs: document CRUD operations with Python",
        "feat: implement parameterized queries for safety",
        "fix: close database connections properly",
        "feat: add SQL aggregation and grouping examples",
        "docs: explain joins with practical examples",
        "refactor: create database utility class",
        "feat: implement data export from SQL to pandas",
    ],
    "logging": [
        "feat: add logging configuration examples",
        "docs: document log levels and formatters",
        "feat: implement rotating file handlers",
        "fix: resolve logging in multimodule applications",
        "feat: add custom logger creation examples",
        "docs: explain logging best practices",
        "refactor: centralize logging configuration",
    ],
    "multithreading": [
        "feat: add threading basics with Thread class",
        "docs: document thread synchronization mechanisms",
        "feat: implement thread pool executor examples",
        "fix: resolve race condition in shared resource access",
        "feat: add multiprocessing for CPU-bound tasks",
        "docs: explain GIL and its implications",
        "refactor: optimize concurrent data processing",
        "feat: implement producer-consumer pattern",
    ],
    "flask": [
        "feat: add Flask app initialization and routing",
        "docs: document request handling and responses",
        "feat: implement form handling and validation",
        "fix: resolve template rendering issues",
        "feat: add REST API endpoints for ML model",
        "docs: explain request context and blueprints",
        "refactor: organize routes into blueprints",
        "feat: implement error handling middleware",
    ],
    "streamlit": [
        "feat: add Streamlit dashboard layout examples",
        "docs: document widget usage and callbacks",
        "feat: implement data visualization dashboard",
        "fix: optimize caching for large datasets",
        "feat: add file upload and processing functionality",
        "docs: explain session state management",
        "refactor: modularize dashboard components",
        "feat: create interactive ML model demo",
    ],
    "statistics": [
        "feat: add descriptive statistics calculations",
        "docs: document measures of central tendency",
        "feat: implement variance and standard deviation examples",
        "fix: handle edge cases in statistical functions",
        "feat: add correlation analysis notebook",
        "docs: explain distributions and their properties",
        "refactor: create statistical utility functions",
        "feat: implement outlier detection methods",
        "docs: add notes on sampling techniques",
    ],
    "probability": [
        "feat: add probability basics and rules notebook",
        "docs: document conditional probability examples",
        "feat: implement Bayes theorem calculations",
        "fix: correct probability distribution parameters",
        "feat: add random variable simulations",
        "docs: explain probability distributions",
        "feat: create Monte Carlo simulation examples",
    ],
    "inferential_statistics": [
        "feat: add hypothesis testing framework",
        "docs: document t-tests and z-tests",
        "feat: implement confidence interval calculations",
        "fix: adjust significance level handling",
        "feat: add chi-square test examples",
        "docs: explain p-values and statistical significance",
        "refactor: create hypothesis testing utilities",
        "feat: implement ANOVA analysis notebook",
        "docs: add notes on effect size calculations",
        "feat: create A/B testing simulation",
    ],
    "feature_engineering": [
        "feat: add feature scaling and normalization examples",
        "docs: document one-hot encoding techniques",
        "feat: implement feature selection methods",
        "fix: handle categorical variable encoding",
        "feat: add polynomial features creation",
        "docs: explain feature importance analysis",
        "refactor: create feature engineering pipeline",
        "feat: implement missing value imputation strategies",
        "docs: add notes on feature extraction techniques",
    ],
    "eda": [
        "feat: add exploratory data analysis workflow",
        "docs: document data profiling techniques",
        "feat: implement automated EDA functions",
        "fix: handle mixed data types in analysis",
        "feat: add univariate and bivariate analysis",
        "docs: explain correlation matrix interpretation",
        "refactor: create EDA report generator",
        "feat: implement outlier visualization methods",
        "docs: add notes on data quality assessment",
        "feat: create interactive EDA dashboard",
    ],
    "general": [
        "docs: update README with learning progress",
        "chore: add requirements.txt dependencies",
        "docs: improve code comments and documentation",
        "refactor: reorganize project folder structure",
        "chore: update .gitignore for Python projects",
        "docs: add module completion notes",
        "fix: resolve import path issues",
        "chore: clean up temporary files",
        "docs: add learning resources and references",
        "refactor: improve notebook organization",
        "docs: update progress tracker in README",
        "chore: add virtual environment setup instructions",
    ],
}

# File patterns to modify (creates small, realistic changes)
LEARNING_NOTES = [
    "# Learning notes - {date}\n",
    "# Practiced on: {date}\n", 
    "# Review session: {date}\n",
    "# Study log entry\n",
]


def get_random_commit_message():
    """Get a random commit message from the collection."""
    category = random.choice(list(COMMIT_MESSAGES.keys()))
    message = random.choice(COMMIT_MESSAGES[category])
    return message


def generate_scattered_dates(days_back, total_commits):
    """
    Generate a list of naturally scattered dates that look like real human activity.
    Some days have multiple commits, many days have none - like real learning patterns.
    """
    dates = []
    
    # Create "active learning periods" - humans learn in bursts
    # Some weeks are busy, some are quiet
    all_days = list(range(1, days_back + 1))
    
    # Weight days - more recent days slightly more likely
    # Also simulate "learning sprints" - clusters of activity
    
    # Create ~15-25 "active periods" of 2-5 days each
    num_active_periods = random.randint(15, 30)
    active_days = set()
    
    for _ in range(num_active_periods):
        # Pick a random starting day
        start_day = random.randint(1, days_back - 5)
        # Active period lasts 1-5 days
        period_length = random.randint(1, 5)
        for d in range(period_length):
            if start_day + d <= days_back:
                active_days.add(start_day + d)
    
    # Also add some random scattered single days
    num_scattered = random.randint(20, 40)
    for _ in range(num_scattered):
        active_days.add(random.randint(1, days_back))
    
    active_days = sorted(list(active_days))
    
    # Now distribute commits across active days
    # Some active days get multiple commits (deep work sessions)
    commits_remaining = total_commits
    
    while commits_remaining > 0 and active_days:
        day = random.choice(active_days)
        
        # 60% chance of 1 commit, 25% chance of 2, 10% of 3, 5% of 4+
        roll = random.random()
        if roll < 0.60:
            num_commits_today = 1
        elif roll < 0.85:
            num_commits_today = 2
        elif roll < 0.95:
            num_commits_today = 3
        else:
            num_commits_today = random.randint(4, 6)
        
        num_commits_today = min(num_commits_today, commits_remaining)
        
        # Generate times for today's commits
        target_date = datetime.now() - timedelta(days=day)
        weekday = target_date.weekday()
        
        # Weekends: later start, possibly less activity
        if weekday >= 5:  # Saturday or Sunday
            base_hour = random.randint(11, 22)
        else:
            # Weekdays: could be morning, afternoon, or evening sessions
            session = random.choice(['morning', 'afternoon', 'evening', 'night'])
            if session == 'morning':
                base_hour = random.randint(7, 11)
            elif session == 'afternoon':
                base_hour = random.randint(14, 17)
            elif session == 'evening':
                base_hour = random.randint(18, 21)
            else:
                base_hour = random.randint(21, 23)
        
        for i in range(num_commits_today):
            # Commits in same session are ~10-45 mins apart
            hour = base_hour
            minute = random.randint(0, 59)
            if i > 0:
                minute = min(59, minute + random.randint(10, 45))
            second = random.randint(0, 59)
            
            commit_date = target_date.replace(hour=hour, minute=minute, second=second)
            dates.append(commit_date)
            commits_remaining -= 1
            
            if commits_remaining <= 0:
                break
    
    # Sort by date (oldest first) for natural commit order
    dates.sort()
    return dates


def get_random_date(days_back, commit_index, total_commits):
    """Legacy function - not used in scattered mode."""
    pass


def create_learning_file(repo_path, date):
    """Create or modify a learning notes file."""
    notes_dir = os.path.join(repo_path, "learning_logs")
    os.makedirs(notes_dir, exist_ok=True)
    
    # Create a file with the date
    filename = f"notes_{date.strftime('%Y%m%d')}.md"
    filepath = os.path.join(notes_dir, filename)
    
    note_content = random.choice(LEARNING_NOTES).format(date=date.strftime('%Y-%m-%d'))
    
    topics = [
        "- Reviewed {} concepts\n".format(random.choice([
            "NumPy array", "pandas DataFrame", "matplotlib plotting",
            "statistical analysis", "data cleaning", "feature engineering",
            "hypothesis testing", "probability", "EDA", "visualization"
        ])),
        "- Practiced {} exercises\n".format(random.choice([
            "Python coding", "data manipulation", "SQL queries",
            "data visualization", "statistical tests", "ML preprocessing"
        ])),
        "- Studied {} topics\n".format(random.choice([
            "machine learning", "data science", "Python programming",
            "statistics", "probability theory", "inferential statistics"
        ])),
    ]
    
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(note_content)
        f.write(random.choice(topics))
    
    return filepath


def run_git_command(cmd, cwd, env=None):
    """Run a git command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def create_backdated_commit(repo_path, commit_date, message, dry_run=False):
    """
    Create a commit with a backdated timestamp.
    """
    date_str = commit_date.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Set up environment with backdated dates
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    if dry_run:
        print(f"  [DRY RUN] Would create commit: {message}")
        print(f"            Date: {date_str}")
        return True
    
    # Create a small file change
    filepath = create_learning_file(repo_path, commit_date)
    
    # Stage the file
    if not run_git_command(f'git add "{filepath}"', repo_path):
        print(f"  [ERROR] Failed to stage file")
        return False
    
    # Create the commit with the backdated timestamp
    commit_cmd = f'git commit -m "{message}" --date="{date_str}"'
    
    # Use environment variables for author/committer dates
    result = subprocess.run(
        commit_cmd,
        cwd=repo_path,
        env=env,
        capture_output=True,
        text=True,
        shell=True
    )
    
    if result.returncode == 0:
        print(f"  ✅ {commit_date.strftime('%Y-%m-%d')} | {message[:50]}...")
        return True
    else:
        print(f"  ❌ Failed: {result.stderr[:100]}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic backdated commits for your ML learning repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python green_graph.py --commits 50 --days 90
  python green_graph.py --commits 100 --days 180 --dry-run
  
This script will:
  1. Create learning log files with realistic content
  2. Make commits with backdated timestamps
  3. Use authentic ML learning commit messages
  
After running, push to GitHub with:
  git push origin main
        """
    )
    
    parser.add_argument(
        '--commits', '-c',
        type=int,
        default=50,
        help='Number of commits to generate (default: 50)'
    )
    
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=90,
        help='Number of days to spread commits over (default: 90)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview commits without actually creating them'
    )
    
    args = parser.parse_args()
    
    # Get the repository path (current directory or parent)
    repo_path = os.path.dirname(os.path.abspath(__file__))
    
    # Verify we're in a git repository
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("❌ Error: Not a git repository. Run this script from your repo root.")
        return
    
    print("=" * 60)
    print("🌱 GitHub Graph Greener - ML Learning Edition")
    print("=" * 60)
    print(f"📁 Repository: {repo_path}")
    print(f"📝 Commits to create: {args.commits}")
    print(f"📅 Days to spread over: {args.days}")
    print(f"🔍 Dry run: {args.dry_run}")
    print("=" * 60)
    
    if not args.dry_run:
        confirm = input("\n⚠️  This will create real commits. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return
    
    print("\n📝 Generating scattered commit dates...\n")
    
    # Generate all dates upfront for natural scatter
    commit_dates = generate_scattered_dates(args.days, args.commits)
    
    success_count = 0
    used_messages = set()  # Avoid duplicate messages
    
    for i, commit_date in enumerate(commit_dates):
        # Get unique message
        message = get_random_commit_message()
        attempts = 0
        while message in used_messages and attempts < 50:
            message = get_random_commit_message()
            attempts += 1
        used_messages.add(message)
        
        if create_backdated_commit(repo_path, commit_date, message, args.dry_run):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully created {success_count}/{args.commits} commits")
    
    if not args.dry_run:
        print("\n📤 Next steps:")
        print("   1. Review your commits: git log --oneline -20")
        print("   2. Push to GitHub: git push origin main")
        print("\n🎉 Your contribution graph will update after pushing!")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
