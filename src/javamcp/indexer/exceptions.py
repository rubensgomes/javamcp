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
Custom exceptions for indexer operations.
"""


class IndexNotBuiltError(Exception):
    """Raised when attempting to query an index that hasn't been built."""


class ClassNotFoundError(Exception):
    """Raised when a class is not found in the index."""


class MethodNotFoundError(Exception):
    """Raised when a method is not found in the index."""


class RepositoryNotIndexedError(Exception):
    """Raised when a repository has not been indexed."""
