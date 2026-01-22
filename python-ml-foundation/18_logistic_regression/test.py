#!/usr/bin/env python3
"""
Auto-Commit Watcher Script
===========================
Watches your project for file changes and automatically commits with smart,
descriptive commit messages based on what changed.

Usage:
    python auto_commit_watcher.py              # Watch current directory
    python auto_commit_watcher.py --interval 5 # Commit every 5 minutes
    python auto_commit_watcher.py --push       # Also push to remote after commit

Stop with Ctrl+C
"""

import os
import sys
import time
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
DEFAULT_INTERVAL_MINUTES = 1.5  # How often to check and commit (1.5 minutes = 90 seconds)
IGNORED_PATTERNS = [
    '.git', '__pycache__', '.ipynb_checkpoints', 'venv', 'env',
    '.venv', 'node_modules', '.idea', '.vscode', '*.pyc', '*.pyo',
    '.DS_Store', 'Thumbs.db', '*.log', '.env', '*.egg-info'
]

# File type categories for smart messages
FILE_CATEGORIES = {
    'notebooks': ['.ipynb'],
    'python': ['.py'],
    'data': ['.csv', '.json', '.xlsx', '.xls', '.parquet', '.pkl', '.pickle'],
    'models': ['.h5', '.keras', '.pt', '.pth', '.onnx', '.joblib', '.model'],
    'docs': ['.md', '.txt', '.rst', '.pdf', '.docx'],
    'config': ['.yaml', '.yml', '.toml', '.ini', '.cfg', '.config'],
    'web': ['.html', '.css', '.js', '.jsx', '.ts', '.tsx'],
    'images': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'],
    'sql': ['.sql'],
}

# Action keywords based on diff analysis
ACTION_KEYWORDS = {
    'add': ['add', 'create', 'implement', 'introduce', 'new'],
    'update': ['update', 'modify', 'change', 'improve', 'enhance'],
    'fix': ['fix', 'correct', 'repair', 'resolve', 'patch'],
    'remove': ['remove', 'delete', 'clean', 'drop'],
    'refactor': ['refactor', 'restructure', 'reorganize', 'optimize'],
}


def get_git_root():
    """Get the root directory of the git repository."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None


def get_changed_files():
    """Get list of changed files (staged and unstaged)."""
    try:
        # Get all changes (staged, unstaged, untracked)
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, text=True, check=True
        )
        
        changes = {'added': [], 'modified': [], 'deleted': [], 'untracked': []}
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            status = line[:2]
            filepath = line[3:].strip()
            
            # Handle renamed files
            if ' -> ' in filepath:
                filepath = filepath.split(' -> ')[1]
            
            if status.strip() == '??':
                changes['untracked'].append(filepath)
            elif 'D' in status:
                changes['deleted'].append(filepath)
            elif 'A' in status or status.strip() == 'A':
                changes['added'].append(filepath)
            else:
                changes['modified'].append(filepath)
        
        return changes
    except subprocess.CalledProcessError:
        return {'added': [], 'modified': [], 'deleted': [], 'untracked': []}


def get_file_category(filepath):
    """Determine the category of a file based on extension."""
    ext = Path(filepath).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'other'


def analyze_notebook_changes(filepath):
    """Analyze what changed in a Jupyter notebook."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--', filepath],
            capture_output=True, text=True
        )
        diff = result.stdout.lower()
        
        indicators = []
        if 'matplotlib' in diff or 'plt.' in diff or 'seaborn' in diff:
            indicators.append('visualizations')
        if 'train' in diff or 'fit' in diff or 'model' in diff:
            indicators.append('model training')
        if 'import' in diff and '+' in diff:
            indicators.append('dependencies')
        if 'read_csv' in diff or 'load' in diff:
            indicators.append('data loading')
        if 'clean' in diff or 'fillna' in diff or 'dropna' in diff:
            indicators.append('data cleaning')
        if 'feature' in diff or 'engineer' in diff:
            indicators.append('feature engineering')
        if 'accuracy' in diff or 'score' in diff or 'metric' in diff:
            indicators.append('evaluation')
        
        return indicators if indicators else ['notebook updates']
    except:
        return ['notebook updates']


def analyze_python_changes(filepath):
    """Analyze what changed in a Python file."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--', filepath],
            capture_output=True, text=True
        )
        diff = result.stdout
        
        indicators = []
        
        # Count additions and deletions
        additions = diff.count('\n+') - diff.count('\n+++')
        deletions = diff.count('\n-') - diff.count('\n---')
        
        if 'def ' in diff and '+def ' in diff:
            indicators.append('new functions')
        if 'class ' in diff and '+class ' in diff:
            indicators.append('new classes')
        if 'import ' in diff and '+import ' in diff:
            indicators.append('imports')
        if 'fix' in diff.lower() or 'bug' in diff.lower():
            indicators.append('bug fixes')
        
        if not indicators:
            if additions > deletions * 2:
                indicators.append('new code')
            elif deletions > additions * 2:
                indicators.append('code cleanup')
            else:
                indicators.append('code changes')
        
        return indicators
    except:
        return ['code changes']


def generate_smart_message(changes):
    """Generate a smart, descriptive commit message based on changes."""
    all_files = (changes['added'] + changes['modified'] + 
                 changes['untracked'] + changes['deleted'])
    
    if not all_files:
        return None
    
    # Group files by category
    categories = defaultdict(list)
    for f in all_files:
        cat = get_file_category(f)
        categories[cat].append(f)
    
    # Determine primary action
    if changes['added'] or changes['untracked']:
        if changes['modified']:
            action = "Add and update"
        else:
            action = "Add"
    elif changes['deleted']:
        if changes['modified']:
            action = "Update and remove"
        else:
            action = "Remove"
    else:
        action = "Update"
    
    # Build message based on what changed
    parts = []
    
    # Handle notebooks specially
    if 'notebooks' in categories:
        notebooks = categories['notebooks']
        if len(notebooks) == 1:
            nb_name = Path(notebooks[0]).stem
            # Analyze notebook changes for more detail
            if notebooks[0] in changes['modified']:
                indicators = analyze_notebook_changes(notebooks[0])
                parts.append(f"{nb_name}: {', '.join(indicators[:2])}")
            else:
                parts.append(f"{nb_name} notebook")
        else:
            parts.append(f"{len(notebooks)} notebooks")
    
    # Handle Python files
    if 'python' in categories:
        py_files = categories['python']
        if len(py_files) == 1:
            py_name = Path(py_files[0]).stem
            if py_files[0] in changes['modified']:
                indicators = analyze_python_changes(py_files[0])
                parts.append(f"{py_name}.py: {', '.join(indicators[:2])}")
            else:
                parts.append(f"{py_name}.py")
        elif len(py_files) <= 3:
            names = [Path(f).stem for f in py_files]
            parts.append(f"Python: {', '.join(names)}")
        else:
            parts.append(f"{len(py_files)} Python files")
    
    # Handle data files
    if 'data' in categories:
        data_files = categories['data']
        if len(data_files) == 1:
            parts.append(f"data: {Path(data_files[0]).name}")
        else:
            parts.append(f"{len(data_files)} data files")
    
    # Handle models
    if 'models' in categories:
        model_files = categories['models']
        if len(model_files) == 1:
            parts.append(f"model: {Path(model_files[0]).name}")
        else:
            parts.append(f"{len(model_files)} model files")
    
    # Handle docs
    if 'docs' in categories:
        doc_files = categories['docs']
        if len(doc_files) == 1:
            parts.append(f"docs: {Path(doc_files[0]).name}")
        else:
            parts.append(f"{len(doc_files)} documentation files")
    
    # Handle other categories briefly
    other_cats = set(categories.keys()) - {'notebooks', 'python', 'data', 'models', 'docs'}
    for cat in other_cats:
        count = len(categories[cat])
        if count == 1:
            parts.append(Path(categories[cat][0]).name)
        else:
            parts.append(f"{count} {cat} files")
    
    # Compose final message
    if not parts:
        return f"{action} {len(all_files)} files"
    
    if len(parts) == 1:
        return f"{action} {parts[0]}"
    elif len(parts) == 2:
        return f"{action} {parts[0]} and {parts[1]}"
    else:
        return f"{action} {parts[0]}, {parts[1]} (+{len(parts)-2} more)"


def stage_all_changes():
    """Stage all changes for commit."""
    try:
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error staging changes: {e}")
        return False


def commit_changes(message):
    """Commit staged changes with the given message."""
    try:
        subprocess.run(
            ['git', 'commit', '-m', message],
            check=True, capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        if 'nothing to commit' in e.stdout.decode() if e.stdout else '':
            return False
        print(f"❌ Error committing: {e}")
        return False


def push_changes():
    """Push commits to remote."""
    try:
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Push failed (you may need to push manually): {e}")
        return False


def print_banner():
    """Print a nice banner."""
    print("\n" + "="*60)
    print("🔄 AUTO-COMMIT WATCHER")
    print("="*60)
    print(f"📁 Watching: {os.getcwd()}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("Press Ctrl+C to stop\n")


def main():
    parser = argparse.ArgumentParser(description='Auto-commit watcher with smart messages')
    parser.add_argument('--interval', '-i', type=float, default=DEFAULT_INTERVAL_MINUTES,
                        help=f'Check interval in minutes (default: {DEFAULT_INTERVAL_MINUTES})')
    parser.add_argument('--push', '-p', action='store_true',
                        help='Also push to remote after each commit')
    parser.add_argument('--once', '-o', action='store_true',
                        help='Run once and exit (no watching)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show what would be committed without actually committing')
    
    args = parser.parse_args()
    
    # Check if we're in a git repo
    git_root = get_git_root()
    if not git_root:
        print("❌ Error: Not in a git repository!")
        print("   Run 'git init' first or navigate to a git repository.")
        sys.exit(1)
    
    os.chdir(git_root)
    
    if not args.once:
        print_banner()
        print(f"⚙️  Check interval: {args.interval} minutes")
        print(f"📤 Auto-push: {'Yes' if args.push else 'No'}")
        print(f"🏃 Mode: {'Dry run' if args.dry_run else 'Live'}\n")
    
    commit_count = 0
    
    try:
        while True:
            changes = get_changed_files()
            total_changes = sum(len(v) for v in changes.values())
            
            if total_changes > 0:
                message = generate_smart_message(changes)
                
                if message:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    if args.dry_run:
                        print(f"[{timestamp}] 🔍 Would commit: {message}")
                        print(f"           Files: {total_changes} changed")
                        for category, files in changes.items():
                            if files:
                                print(f"           - {category}: {', '.join(files[:3])}" + 
                                      (f" (+{len(files)-3} more)" if len(files) > 3 else ""))
                    else:
                        if stage_all_changes() and commit_changes(message):
                            commit_count += 1
                            print(f"[{timestamp}] ✅ Committed: {message}")
                            
                            if args.push:
                                if push_changes():
                                    print(f"[{timestamp}] 📤 Pushed to remote")
                        else:
                            print(f"[{timestamp}] ℹ️  No changes to commit")
            else:
                if not args.once:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] 👀 Watching... (no changes)")
            
            if args.once:
                break
            
            # Wait for next check
            time.sleep(args.interval * 60)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("👋 Watcher stopped!")
        print(f"📊 Total commits made: {commit_count}")
        print("="*60 + "\n")


if __name__ == '__main__':
    main()
