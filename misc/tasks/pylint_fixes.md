# Pylint Fixes Plan

## Overview
Fix all pylint issues to improve code quality (current score: 1.33/10)

## Tasks

- [ ] Fix logging f-string issues (use lazy % formatting)
- [ ] Fix broad exception catching and add explicit re-raise chains
- [ ] Remove unused imports and variables
- [ ] Fix unnecessary elif after return statements
- [ ] Fix missing final newlines
- [ ] Remove unnecessary pass statements in exceptions
- [ ] Add pylintrc to disable warnings for Pydantic models and ANTLR4 generated files
- [ ] Run pylint again to verify all fixes

## Issues to Fix

### High Priority (Code Quality)
1. **Logging issues** - Use lazy % formatting instead of f-strings
2. **Exception handling** - Add explicit re-raise chains with `from e`
3. **Unused imports/variables** - Clean up unused code
4. **Code style** - Fix elif after return, missing final newlines

### Low Priority (Configuration)
5. **Pydantic models** - Disable "too-few-public-methods" for data models
6. **ANTLR4 files** - Exclude generated files from linting

## Review
- Verify pylint score improves significantly after fixes
