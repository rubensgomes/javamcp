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
Custom exceptions for repository operations.
"""


class RepositoryNotFoundError(Exception):
    """Raised when a repository is not found at the specified location."""


class CloneFailedError(Exception):
    """Raised when cloning a repository fails."""


class InvalidRepositoryError(Exception):
    """Raised when a path does not contain a valid Git repository."""


class GitOperationError(Exception):
    """Raised when a Git operation fails."""
