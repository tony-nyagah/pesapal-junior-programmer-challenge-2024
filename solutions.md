## 1: Image Hash Spoofing
This tool modifies a PNG or JPEG image by inserting invisible data that doesn't affect how the image is displayed, but changes the file's SHA-256 hash. The goal is to produce an output file whose hash begins with a specified hexadecimal prefix.

**TLDR:** 
* Here is the code: [spoof.go](image-hash-spoofer/spoof.go)
* This video shows how it works: 

https://github.com/user-attachments/assets/0daefe64-243f-45e8-b49b-d802a64e11c2



**Note:**
* This code inserts a custom ancillary chunk for PNGs or a COM (comment) segment for JPEGs.
* The displayed image remains visually identical to the original.
* The process is brute force: it keeps trying different inserted values until it finds a file hash starting with the desired prefix.

---

### Features
* Supports PNG and JPEG input images.
* Uses SHA-256 for hashing.
* Allows specifying a hex prefix (e.g., `0x24`) to search for in the resulting file's hash.

### Requirements
* Go 1.18+ (or compatible version) installed on your system.
* A PNG or JPEG image to test.
* Sufficient computing power (the process can be quick or may take a while, depending on how difficult the prefix is to achieve).

---

### Building the Tool
1. Clone or download the repository containing the `spoof.go` file.
2. Open a terminal or command prompt in the repository directory where the `spoof.go` file is located.
3. Run the following command to build the binary:
```bash
go build -o spoof spoof.go
```
This produces an executable named `spoof` (on Linux or macOS) or `spoof.exe` (on Windows).

### Usage
To run the tool, use the following command format:
```bash
./spoof <hex_prefix> <input_image> <output_image>
```

#### Arguments:
* `hex_prefix`: The desired hex prefix for the resulting file's SHA-256 hash.
    * You can specify the prefix with or without `0x`. For example, `0x24` or `24` are both valid.

* `input_image`: The path to the original image (PNG or JPEG).
* `output_image`: The path where the modified image should be saved.

### Examples
There are example files saved in the `images` directory.
**Example 1 (JPEG):**
```bash
./spoof 0x24 images/original.jpg images/altered.jpg
```
This command attempts to produce a JPEG file `altered.jpg` whose SHA-256 hash starts with `24`.

**Example 2 (PNG):**
```bash
./spoof 0x24 images/original.png images/altered.png
```

### Understanding the Output
* **Original file hash:** The tool first prints the hash of the original file.
* **Progress messages:** Every 1000 attempts, it prints a message to show you what prefix it currently has.
* **Success message:** Once the tool finds a file whose hash starts with the desired prefix, it prints "Success after X attempts!" and shows the resulting hash.

For example, you might see:
```bash
Original file hash: a4f7e9...f3492a  original.jpg
Attempt 1000: current hash prefix: "38"
Attempt 2000: current hash prefix: "1c"
Success after 2357 attempts!
Resulting hash: 2448a6512f...93de43f4b5b  altered.jpg
```

### Notes
* The search may be quick for shorter prefixes (e.g., `24`) and longer for larger prefixes (e.g., `0000deadbeef`).
* Adjusting the length of the prefix changes the difficulty significantly.
* This approach brute forces by trying random 32-byte segments, so there is no guarantee of quick success, but for small prefixes, it usually doesn't take too long.


## 2. Source Control System
Inspired by Git’s design and [The Git Parable](https://tom.preston-werner.com/2009/05/19/the-git-parable.html).

**Mini-Git** is a simplified version control system written in Python. Inspired by Git, it allows users to manage project versions using commands for initializing repositories, staging changes, committing snapshots, and managing branches. This project is built for educational purposes to understand the fundamental workings of Git-like systems.

---

### Features

- Repository Initialization
- File Staging
- Committing Changes
- Snapshot Storage using Hash-based Naming
- Branch Management

---

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd mini-git
   ```

3. Ensure you have Python 3 installed:
   ```bash
   python --version
   ```

4. Run the script:
   ```bash
   python mini-gity.py
   ```

---

### Usage

#### Commands:

##### 1. Initialize a repository:
   ```bash
   python mini-gity.py init
   ```
   - Creates a `.mini-git` directory to store version control metadata.

##### 2. Stage files:
   ```bash
   python mini-gity.py stage <file1> <file2> ...
   ```
   - Adds files to the staging area for the next commit.

##### 3. Commit changes:
   ```bash
   python mini-gity.py commit -m "Your commit message"
   ```
   - Saves a snapshot of the staged changes with a unique hash-based identifier.

##### 4. View the commit log:
   ```bash
   python mini-gity.py log
   ```
   - Displays a history of commits in the repository.

##### 5. Create a new branch:
   ```bash
   python mini-gity.py branch <branch-name>
   ```
   - Creates a new branch to allow parallel development.

##### 6. Switch to a branch:
   ```bash
   python mini-gity.py switch <branch-name>
   ```
   - Changes the working branch.

##### 7. Help menu:
   ```bash
   python mini-gity.py
   ```
   - Displays the list of commands and their usage.

---

### How it Works

#### Hash-Based Snapshots
Mini-Git uses a SHA-256 hash of the committed files’ content and metadata (e.g., timestamp) to uniquely identify each snapshot.

#### Staging Area
The staging area acts as a preparation zone where users add files before committing. Only staged files are included in a commit.

#### Branch Management
Each branch represents a separate timeline of development. You can create and switch between branches for isolated work.

---

### Example Workflow

1. Initialize the repository:
   ```bash
   python mini-gity.py init
   ```

2. Stage files for a commit:
   ```bash
   python mini-gity.py stage file1.txt file2.txt
   ```

3. Commit the staged changes:
   ```bash
   python mini-gity.py commit -m "Initial commit"
   ```

4. Create and switch to a new branch:
   ```bash
   python mini-gity.py branch feature-branch
   python mini-gity.py switch feature-branch
   ```

5. Stage and commit more changes:
   ```bash
   python mini-gity.py stage file3.txt
   python mini-gity.py commit -m "Added new feature"
   ```

6. View the commit history:
   ```bash
   python mini-gity.py log
   ```

