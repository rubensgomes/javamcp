# Add Apache 2.0 License Headers

## Plan

- [x] Add license header to all Python source files in src/javamcp/
- [x] Add license header to all Python test files in tests/
- [x] Verify all files have been updated correctly

## Details

Total files to update: 71 Python files

License header to add:
```python
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
```

## Implementation Approach

Will add the license header to the top of each Python file, checking first if the file already has a license header to avoid duplicates.

## Review

Successfully added Apache 2.0 license headers to all 68 Python files in the project:
- Updated 65 files that didn't have the license header
- Skipped 3 files that already had the license header
- All source files in `src/javamcp/` now have the license header
- All test files in `tests/` now have the license header
- Verification confirms all Python files now contain the SPDX-License-Identifier and full Apache 2.0 license text
