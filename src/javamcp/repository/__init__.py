# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Rubens Gomes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Git repository management functionality.
"""

from .exceptions import (CloneFailedError, GitOperationError,
                         InvalidRepositoryError, RepositoryNotFoundError)
from .git_operations import (checkout_branch, clone_repository,
                             get_current_commit_hash, is_git_repository,
                             pull_repository)
from .manager import RepositoryManager

__all__ = [
    # Exceptions
    "RepositoryNotFoundError",
    "CloneFailedError",
    "InvalidRepositoryError",
    "GitOperationError",
    # Git operations
    "clone_repository",
    "pull_repository",
    "checkout_branch",
    "is_git_repository",
    "get_current_commit_hash",
    # Manager
    "RepositoryManager",
]
