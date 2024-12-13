import os
import shutil
import time


def init_repo(repo_path="repo"):
    """
    Initialize a new mini-git repository.
    Creates 'working' and 'snapshots' directories inside the repo folder.
    """
    working_dir = os.path.join(repo_path, "working")
    snapshots_dir = os.path.join(repo_path, "snapshots")

    try:
        os.makedirs(working_dir, exist_ok=True)
        os.makedirs(snapshots_dir, exist_ok=True)
        print(f"Initialized empty mini-git repository in {os.path.abspath(repo_path)}")
    except Exception as e:
        print(f"Error initializing repository: {e}")


def take_snapshot(repo_path="repo", message=""):
    """
    Create a snapshot of the working directory.
    """
    snapshots_dir = os.path.join(repo_path, "snapshots")
    working_dir = os.path.join(repo_path, "working")

    # Determine the snapshot number
    existing_snapshots = os.listdir(snapshots_dir)
    snapshot_id = len(existing_snapshots)
    snapshot_dir = os.path.join(snapshots_dir, f"snapshot-{snapshot_id}")

    try:
        # Copy the working directory
        shutil.copytree(working_dir, snapshot_dir)

        # Add a message file
        with open(os.path.join(snapshot_dir, "message.txt"), "w") as message_file:
            message_file.write(f"{message}\nTimestamp: {time.ctime()}")

        print(f"Snapshot {snapshot_id} created successfully.")
    except Exception as e:
        print(f"Error creating snapshot: {e}")


def list_snapshots(repo_path="repo"):
    """
    List all snapshots in the repository.
    """
    snapshots_dir = os.path.join(repo_path, "snapshots")

    try:
        snapshots = sorted(os.listdir(snapshots_dir))
        if not snapshots:
            print("No snapshots found.")
            return

        print("Snapshots:")
        for snapshot in snapshots:
            snapshot_path = os.path.join(snapshots_dir, snapshot, "message.txt")
            with open(snapshot_path, "r") as message_file:
                print(f"{snapshot}: {message_file.readline().strip()}")
    except Exception as e:
        print(f"Error listing snapshots: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Mini-Git: A simple version control simulation."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize a new repository.")

    # Snapshot command
    snapshot_parser = subparsers.add_parser(
        "snapshot", help="Take a snapshot of the working directory."
    )
    snapshot_parser.add_argument(
        "-m", "--message", type=str, required=True, help="Message for the snapshot."
    )

    # List snapshots command
    list_parser = subparsers.add_parser("list", help="List all snapshots.")

    args = parser.parse_args()

    if args.command == "init":
        init_repo()
    elif args.command == "snapshot":
        take_snapshot(message=args.message)
    elif args.command == "list":
        list_snapshots()
    else:
        parser.print_help()
