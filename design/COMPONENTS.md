## GitRepositoryManager

The GitRepositoryManager should handle the cloning and updating of the Git
repositories. Its main focus should be to clone the remote Git repositories in
local persistent folders in the local machine. It should first check if the Git
repository already exists locally in a specific temporary folder. If it does,
then it should sync the local repository with the remote. Otherwise, it should
do a fresh clone of the remote repository.

The GitRepositoryManager should take as inputs:

- A list of Git repository URLs.
- A local directory path where the repositories will be cloned or updated.

The GitRepositoryManager should output:

- A list of local directory paths where the Git repositories are cloned or
  updated.

The GitRepositoryManager should report errors if any repository cannot be cloned
or updated.

For simplicity, the following limitations apply:

1. Private repositories and authentication are not supported.
2. Only the main Git Repository branch is cloned/updated.

## JavaPathIndexer

The JavaPathIndexer should be responsible for indexing Java source files in the
cloned Git repositories. It should traverse the directory structure of each
cloned repository and identify all Java source files located under the
`src/main/java` directory. Then it should create a list of paths to these Java
source files, and stores them in a suitable data structure for further
processing.

The JavaPathIndexer should take as inputs:

- A list of local directory paths where the Git repositories are cloned.
- It should output a list of paths to Java source files found in the
  `src/main/java` directories of the cloned repositories.
- The JavaPathIndexer should report errors if any directory cannot be accessed
  or if no Java source files are found.
