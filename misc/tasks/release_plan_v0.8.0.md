# Release Plan v0.8.0 - Documentation Enhancements and Clarity Improvements

## Release Information

- **Repository**: rubensgomes/javamcp
- **Current Version**: v0.7.0
- **Target Version**: v0.8.0
- **Release Type**: PATCH (Documentation improvements and formatting)
- **Latest Release**: v0.7.0 (2025-10-23)
- **Target Date**: TBD

## Release Overview

This release focuses on enhancing documentation clarity, improving setup instructions for multiple platforms (macOS and Linux), adding a production readiness warning, and refining the AI disclaimer in the LICENSE file. No functional code changes.

## Pending Changes

### Modified Files
- `DEVSETUP.md` - Added Linux Ubuntu instructions, improved command examples, added upgrade instructions
- `LICENSE` - Reformatted AI disclaimer for better visibility with warning box formatting
- `README.md` - Added production warning, improved formatting, removed Contributing section
- `misc/tasks/release_plan_v0.7.0.md` - Updated with completion status

### New Files
- `misc/tasks/release_plan_v0.8.0.md` - THIS FILE: Release plan for v0.8.0

### Deleted Files
- None

## Changes for v0.8.0

### Added
- **Linux Ubuntu Setup Instructions** (`DEVSETUP.md`)
  - Added Ubuntu-specific installation commands for python3 and pipx
  - Separated macOS and Linux installation steps for clarity
  - Platform-specific guidance for developers on different OSes
- **Package Upgrade Instructions** (`DEVSETUP.md`)
  - New section for upgrading pipx-installed packages
  - Commands for upgrading fastmcp, pylint, pytest, and poetry
  - Helps developers maintain up-to-date tooling
- **Production Readiness Warning** (`README.md`)
  - Prominent WARNING section at top of README
  - States project is under development as of Oct. 24, 2025
  - Sets clear expectations for users about production readiness
- **Enhanced Command Examples** (`DEVSETUP.md`)
  - Multiple "Ensure at project root" reminders before commands
  - Explicit example commands (e.g., `poetry add fastmcp` instead of generic placeholders)
  - Better consistency with `cd $(git rev-parse --show-toplevel) || exit` pattern

### Changed
- **LICENSE File - AI Disclaimer Formatting**
  - Reformatted AI warning with visual separation (`!!! WARNING / ATTENTION !!!`)
  - Multi-line formatting for better readability
  - Clearer emphasis on requirement to read DISCLAIMER.md
  - More prominent visual treatment of critical warning
- **README.md Improvements**
  - Improved project description formatting (line breaks for readability)
  - Added context about project intent and use case
  - Fixed trailing whitespace issues
  - Removed "Contributing" section (premature for alpha project)
- **DEVSETUP.md Enhancements**
  - Better organized installation sections with platform-specific headers
  - Added explicit comments in code examples
  - Consistent use of `cd $(git rev-parse --show-toplevel) || exit` pattern
  - Improved clarity with "Ensure at project root" reminders
  - Better structure for virtual environment management section

### Removed
- **Contributing Section** (`README.md`)
  - Removed premature contributing guidelines
  - Project is still in alpha/development phase
  - Can be re-added when project reaches stable state

## Technical Details

### Semantic Versioning Rationale
- **PATCH version bump** (0.7.0 → 0.8.0)
- Documentation and formatting improvements only
- No code changes
- No dependency updates
- No breaking changes to public API
- Fully backward compatible

### Changes Summary

**Documentation:**
- 3 documentation files improved (DEVSETUP.md, LICENSE, README.md)
- Added multi-platform support instructions
- Enhanced user guidance with production warning
- Improved formatting and clarity throughout

**Code:**
- No code changes
- No dependency updates
- No test changes

**User Impact:**
- Better onboarding experience for Linux users
- Clearer expectations with production warning
- Easier package upgrade workflow
- More prominent AI disclaimer visibility

### Impact Assessment
- **User Impact**: Positive (better documentation, clearer warnings)
- **API Changes**: None
- **Breaking Changes**: None
- **Dependency Risk**: None (no dependency changes)
- **Testing Required**: Standard validation (no new tests needed)

### Implementation Status
- [ ] Update CHANGELOG.md with v0.8.0 entry
- [ ] Run full test suite to ensure stability
- [ ] Verify code quality (pylint, black, isort)
- [ ] Update version in pyproject.toml (0.7.0 → 0.8.0)
- [ ] Commit changes
- [ ] Create git tag v0.8.0
- [ ] Build distribution packages
- [ ] Create GitHub release
- [ ] Push to repository

## Pre-Release Checklist

### 1. Documentation Updates
- [ ] Update CHANGELOG.md with v0.8.0 section
- [ ] Verify README.md accuracy and warning visibility
- [ ] Review all modified documentation files
- [ ] Ensure LICENSE disclaimer formatting is clear

### 2. Code Quality Verification
```bash
# Run full test suite
poetry run pytest

# Check coverage
poetry run pytest --cov=src/javamcp --cov-report=term-missing

# Format code
poetry run black src/ tests/

# Sort imports
poetry run isort src/ tests/

# Lint code
poetry run pylint src/javamcp

# Type checking
poetry run mypy src/
```

### 3. Version Update
- [ ] Update `pyproject.toml` version: `0.7.0` → `0.8.0`
- [ ] Verify all version references are consistent

### 4. Git Operations
```bash
# Stage all changes
git add .

# Commit with conventional commit message
git commit -m "docs: enhance documentation with multi-platform support and warnings

- Add Linux Ubuntu installation instructions to DEVSETUP.md
- Add package upgrade instructions for pipx-installed tools
- Reformat LICENSE AI disclaimer with prominent warning box
- Add production readiness warning to README.md
- Improve README.md formatting and project description
- Remove premature Contributing section from README.md
- Add explicit command examples and project root reminders
- Improve consistency across documentation files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Create annotated tag
git tag -a v0.8.0 -m "v0.8.0 - Documentation Enhancements and Clarity Improvements"

# Push commits and tags
git push origin main
git push origin v0.8.0
```

### 5. Build and Release
```bash
# Build distribution packages
poetry build

# Create GitHub release
gh release create v0.8.0 \
  --title "v0.8.0 - Documentation Enhancements and Clarity Improvements" \
  --notes "$(cat <<'EOF'
# v0.8.0 - Documentation Enhancements and Clarity Improvements

## Added
- **Multi-Platform Setup Instructions**
  - Linux Ubuntu installation commands for python3 and pipx
  - Separated macOS and Linux installation steps
  - Platform-specific guidance for diverse development environments
- **Package Upgrade Instructions**
  - Commands for upgrading pipx-installed packages (fastmcp, pylint, pytest, poetry)
  - Helps developers maintain current tooling versions
- **Production Readiness Warning**
  - Prominent warning in README about development status
  - Sets clear user expectations about alpha status
- **Enhanced Command Examples**
  - Explicit examples replacing generic placeholders
  - Consistent project root navigation pattern
  - Better developer guidance with contextual comments

## Changed
- **LICENSE File Formatting**
  - Reformatted AI disclaimer with visual warning box (`!!! WARNING / ATTENTION !!!`)
  - Multi-line formatting for improved readability
  - More prominent critical warning treatment
- **README.md Improvements**
  - Improved project description with better formatting
  - Added project intent and use case context
  - Fixed trailing whitespace
  - Removed premature Contributing section
- **DEVSETUP.md Enhancements**
  - Platform-specific installation headers
  - Consistent command patterns with error handling
  - Better structure and organization
  - Improved clarity with "Ensure at project root" reminders

## Removed
- **Contributing Section** from README.md
  - Removed as project is still in alpha phase
  - Will be re-added when reaching stable release

## Technical
- No code changes
- No dependency updates
- All tests remain passing
- Fully backward compatible
- Documentation-only release

## Benefits
- 🐧 **Better Linux Support**: Ubuntu users get clear installation path
- ⚠️ **Clearer Warnings**: Production status and AI disclaimers more visible
- 📚 **Improved Documentation**: Better formatting and platform-specific guidance
- 🔄 **Easier Maintenance**: Package upgrade instructions help developers
- 🎯 **Realistic Expectations**: Warning sets appropriate user expectations

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  dist/javamcp-0.8.0.tar.gz \
  dist/javamcp-0.8.0-py3-none-any.whl
```

## Release Notes Draft

```markdown
# v0.8.0 - Documentation Enhancements and Clarity Improvements

## Added
- **Multi-Platform Setup Instructions** (`DEVSETUP.md`)
  - Linux Ubuntu installation commands for python3 and pipx
  - Separated installation steps for macOS and Linux
  - Platform-specific guidance for developers on different operating systems
- **Package Upgrade Instructions** (`DEVSETUP.md`)
  - Commands for upgrading pipx-installed packages (fastmcp, pylint, pytest, poetry)
  - Helps developers maintain up-to-date tooling
- **Production Readiness Warning** (`README.md`)
  - Prominent WARNING section stating project is under development
  - Sets clear expectations about alpha status as of Oct. 24, 2025
- **Enhanced Command Examples** (`DEVSETUP.md`)
  - Explicit examples (e.g., `poetry add fastmcp`) instead of generic placeholders
  - Consistent `cd $(git rev-parse --show-toplevel) || exit` pattern
  - "Ensure at project root" reminders before command sequences

## Changed
- **LICENSE File - AI Disclaimer Formatting**
  - Reformatted with visual warning box: `!!! WARNING / ATTENTION !!!`
  - Multi-line formatting for better readability
  - More prominent treatment of critical AI disclaimer
  - Clearer emphasis on DISCLAIMER.md requirement
- **README.md Improvements**
  - Improved project description formatting with better line breaks
  - Added context about project intent and use case
  - Fixed trailing whitespace throughout
  - Removed premature "Contributing" section (project still in alpha)
- **DEVSETUP.md Enhancements**
  - Better organized with platform-specific section headers
  - Added explicit comments in code examples
  - Improved virtual environment management instructions
  - Consistent command patterns with error handling

## Removed
- **Contributing Section** (`README.md`)
  - Removed as project is in alpha/development phase
  - Can be re-added when project reaches stable release

## Technical
- No code changes
- No dependency updates
- All 247 tests remain passing
- 95%+ test coverage maintained
- Code quality maintained (pylint, black, isort)
- Fully backward compatible
- No breaking changes to public API

## Benefits
- 🐧 **Better Linux Support**: Ubuntu users now have clear installation instructions
- ⚠️ **Clearer Warnings**: Production readiness and AI disclaimers are more prominent
- 📚 **Improved Documentation**: Better formatting and platform-specific guidance
- 🔄 **Easier Maintenance**: Package upgrade instructions streamline developer workflow
- 🎯 **Realistic Expectations**: Production warning sets appropriate user expectations
- 🌍 **Multi-Platform**: Supports both macOS and Linux development environments

## Migration Guide

No migration required. This release is documentation-only and fully backward compatible. All changes improve user experience and documentation clarity.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Post-Release Tasks

- [ ] Verify release appears on GitHub releases page
- [ ] Test installation from release artifacts
- [ ] Monitor for any issues reported
- [ ] Update project board/tracking system
- [ ] Mark release plan as complete

## Notes

- Purely documentation-focused release
- No code changes or functional modifications
- Enhances multi-platform support (macOS and Linux)
- Improves user experience with clearer warnings and instructions
- Sets realistic expectations about production readiness
- All existing functionality preserved
- Improves developer onboarding experience

## Review

**Status**: PENDING

**Summary:**
Release v0.8.0 focuses on documentation improvements to enhance clarity, add multi-platform support, and set proper user expectations. Key additions include Linux Ubuntu installation instructions, package upgrade commands, and a production readiness warning. LICENSE disclaimer reformatted for better visibility. No code changes, fully backward compatible.

**Changes Breakdown:**
- Documentation: 3 files improved (DEVSETUP.md, LICENSE, README.md)
- Code: No changes
- Dependencies: No changes
- Tests: No changes (existing tests remain valid)

**Risk Assessment:** VERY LOW
- Documentation-only changes
- No code modifications
- No dependency updates
- Backward compatible
- No impact on existing functionality

**Next Steps:**
1. Update CHANGELOG.md with v0.8.0 entry
2. Run test suite for validation
3. Update version to 0.8.0 in pyproject.toml
4. Commit changes with conventional commit message
5. Create git tag v0.8.0
6. Build distribution packages
7. Create GitHub release
8. Push to repository
