import subprocess
import sys


def ensure_local_db():
    """
    Start the local MongoDB instance if it's not already running.
    """
    try:
        result = subprocess.run(
            ['zsh', '-ic', 'mongodb'],
            capture_output=True,
            text=True,
            check=True
        )
        # Print MongoDB stdout and stderr
        print(result.stdout, end="")
        print(result.stderr, file=sys.stderr, end="")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start MongoDB: {e}", file=sys.stderr)
