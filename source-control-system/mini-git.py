import os
import sys
import json
import hashlib


class MiniGit:
    def __init__(self):
        """
        Initialize a new MiniGit repository.
        """
        self.repo_path = ".mini_git"
        self.staging_file = os.path.join(self.repo_path, "staging.json")
        self.snapshots_file = os.path.join(self.repo_path, "snapshots.json")
        self.branches_file = os.path.join(self.repo_path, "branches.json")
        self.current_branch_file = os.path.join(self.repo_path, "current_branch.txt")

    def init(self):
        """
        Initializes a new mini-git repository.

        Creates the following files in the `.mini_git` directory:
        - `staging.json`: empty list to store staged files
        - `snapshots.json`: empty dictionary to store snapshots
        - `branches.json`: dictionary with a single key "main" and an empty list as the value
        - `current_branch.txt`: file containing the name of the current branch, "main"

        If the repository is already initialized, prints a message indicating so.
        """
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            with open(self.staging_file, "w") as f:
                json.dump([], f)
            with open(self.snapshots_file, "w") as f:
                json.dump({}, f)
            with open(self.branches_file, "w") as f:
                json.dump({"main": []}, f)
            with open(self.current_branch_file, "w") as f:
                f.write("main")
            print("Initialized empty mini-git repository.")
        else:
            print("Repository already initialized.")

    def stage(self, file):
        """
        Stages a file, adding it to the list of files to be committed in the next snapshot.

        Args:
            file (str): The name of the file to stage.

        Returns:
            None
        """
        if not os.path.exists(file):
            print(f"Error: {file} does not exist.")
            return
        with open(self.staging_file, "r") as f:
            staging = json.load(f)
        if file not in staging:
            staging.append(file)
            with open(self.staging_file, "w") as f:
                json.dump(staging, f)
            print(f"Staged {file}.")
        else:
            print(f"{file} is already staged.")

    def unstage(self, file):
        """
        Unstages a file, removing it from the list of files to be committed in the next snapshot.

        Args:
            file (str): The name of the file to unstage.

        Returns:
            None
        """
        with open(self.staging_file, "r") as f:
            staging = json.load(f)
        if file in staging:
            staging.remove(file)
            with open(self.staging_file, "w") as f:
                json.dump(staging, f)
            print(f"Unstaged {file}.")
        else:
            print(f"{file} is not staged.")

    def staged(self):
        """
        Prints the list of staged files.

        Returns:
            None
        """
        with open(self.staging_file, "r") as f:
            staging = json.load(f)
        if staging:
            print("Staged files:")
            for file in staging:
                print(f"- {file}")
        else:
            print("No files staged.")

    def snapshot(self, message):
        """
        Creates a new snapshot of the current repository state, using the list of staged files and a commit message.

        The snapshot is stored in the "snapshots.json" file, and the ID of the snapshot is printed to the console.

        The list of staged files is cleared after the snapshot is created.

        Args:
            message (str): The commit message for the snapshot.

        Returns:
            None
        """

        with open(self.staging_file, "r") as f:
            staging = json.load(f)
        if not staging:
            print("Nothing to snapshot.")
            return

        with open(self.snapshots_file, "r") as f:
            snapshots = json.load(f)

        with open(self.current_branch_file, "r") as f:
            current_branch = f.read().strip()

        branch_snapshots = snapshots.get(current_branch, [])

        snapshot_content = {
            "files": {file: self.hash_file(file) for file in staging},
            "message": message,
        }

        snapshot_hash = hashlib.sha1(json.dumps(snapshot_content).encode()).hexdigest()

        branch_snapshots.append({"id": snapshot_hash, "content": snapshot_content})
        snapshots[current_branch] = branch_snapshots

        with open(self.snapshots_file, "w") as f:
            json.dump(snapshots, f, indent=4)

        with open(self.staging_file, "w") as f:
            json.dump([], f)

        print(f"Snapshot created with ID: {snapshot_hash[:7]}.")

    def hash_file(self, file):
        """
        Computes the SHA-1 hash of the given file.

        Args:
            file (str): The path to the file to hash.

        Returns:
            str: The SHA-1 hash of the file as a hexadecimal string.
        """
        with open(file, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()

    def branch(self, action, name=None):
        """
        Creates a new branch or switches to an existing one.

        Args:
            action (str): One of "create" or "switch".
            name (str, optional): The name of the branch to create or switch to.

        Returns:
            None
        """
        with open(self.branches_file, "r") as f:
            branches = json.load(f)
        if action == "create":
            if name in branches:
                print(f"Branch {name} already exists.")
            else:
                branches[name] = []
                with open(self.branches_file, "w") as f:
                    json.dump(branches, f, indent=4)
                print(f"Branch {name} created.")
        elif action == "switch":
            if name not in branches:
                print(f"Branch {name} does not exist.")
            else:
                with open(self.current_branch_file, "w") as f:
                    f.write(name)
                print(f"Switched to branch {name}.")
        else:
            print("Invalid branch action. Use 'create' or 'switch'.")

    def show_help(self):
        help_text = """
        Usage: python mini_git.py <command> [<args>]

        Commands:
            init                      Initialize a new mini-git repository
            stage <file>              Stage a file for the next snapshot
            unstage <file>            Unstage a file
            staged                    List staged files
            snapshot -m "message"    Create a snapshot with a message
            branch create <name>      Create a new branch
            branch switch <name>      Switch to an existing branch
        """
        print(help_text)


def main():
    mini_git = MiniGit()

    if len(sys.argv) < 2:
        mini_git.show_help()
        return

    command = sys.argv[1]

    if command == "init":
        mini_git.init()
    elif command == "stage" and len(sys.argv) == 3:
        mini_git.stage(sys.argv[2])
    elif command == "unstage" and len(sys.argv) == 3:
        mini_git.unstage(sys.argv[2])
    elif command == "staged":
        mini_git.staged()
    elif command == "snapshot" and len(sys.argv) >= 3 and sys.argv[2] == "-m":
        message = " ".join(sys.argv[3:])
        mini_git.snapshot(message)
    elif command == "branch" and len(sys.argv) >= 4:
        action = sys.argv[2]
        name = sys.argv[3]
        mini_git.branch(action, name)
    else:
        mini_git.show_help()


if __name__ == "__main__":
    main()
