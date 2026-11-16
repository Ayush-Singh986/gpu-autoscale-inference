
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git(command):
    result = subprocess.run(
        ["git"] + command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Git error:", result.stderr)
        sys.exit(1)

    return result.stdout.strip()


def main():
    if not Path(".git").exists():
        print("Error: Run this script inside a Git repository.")
        return

    status = run_git(["status", "--porcelain"])

    if not status:
        print("No actual changes found. Nothing to commit.")
        return

    print("\nChanges detected:")
    print(status)

    message = input("\nEnter your contribution message: ").strip()

    if not message:
        print("Commit cancelled.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    run_git(["add", "-A"])

    run_git([
        "commit",
        "-m", f"{message} ({timestamp})"
    ])

    branch = run_git(["branch", "--show-current"])

    print(f"\nPushing changes to {branch}...")

    run_git(["push", "origin", branch])

    print("\nSuccessfully pushed actual project changes!")
    print("Check your GitHub contribution graph.")


if __name__ == "__main__":
    main()
