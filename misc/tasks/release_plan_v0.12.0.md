# Release Plan v0.12.0

## Overview
- **Repository**: rubensgomes/javamcp
- **Current Version**: 0.11.0
- **Target Version**: 0.12.0
- **Release Type**: Minor (new features, backward compatible)

## Summary of Changes

### Fixed
- **ANTLR4 Parser Python Compatibility**
  - Fixed semantic predicates using Java-style `this.` syntax - changed to Python `self.`
  - Added `IsNotIdentifierAssign()` and `DoLastRecordComponent()` predicate methods
  - Regenerated parser from updated grammar

- **AST Visitor Parameter Extraction**
  - Fixed `formalParameterList()` call to use indexed access `formalParameterList(0)`
  - Removed obsolete `_extract_last_parameter()` method (varargs handled in `formalParameter`)

### Changed
- **Grammar Updates** (`grammars/JavaParser.g4`)
  - Updated annotation parsing with new `annotationFieldValues` and `annotationFieldValue` rules
  - Simplified `formalParameterList` - removed separate `lastFormalParameter` rule
  - Added `classType` and `packageName` rules for better type parsing
  - Varargs (`...`) now handled within `formalParameter` directly

### Technical
- All 287 tests passing
- Backward compatible - no breaking API changes
- Parser regenerated with ANTLR4

---

## Pre-Release Checklist

- [x] All tests pass: `poetry run pytest`
- [x] Code quality checks pass: `poetry run pylint --ignore-paths='^.*/antlr4/.*' "src/javamcp"`
- [x] Type checking passes: `poetry run mypy "src/javamcp"` (pre-existing errors, not blocking)
- [x] Code formatted: `poetry run black src/ tests/` and `poetry run isort src/ tests/`

## Release Steps

- [x] 1. Clean up untracked files (`grammars/gen/`, `src/javamcp/antlr4/JavaParserVisitor.py`)
- [x] 2. Update version in `pyproject.toml` from `0.11.0` to `0.12.0`
- [x] 3. Update `CHANGELOG.md` with v0.12.0 changes
- [x] 4. Commit all changes with message: `feat: release v0.12.0 with ANTLR4 parser fixes`
- [x] 5. Create git tag: `git tag v0.12.0`
- [ ] 6. Push to remote: `git push origin main && git push origin v0.12.0` (requires manual auth)

## Post-Release Verification

- [ ] Verify tag appears on GitHub
- [ ] Verify tests still pass after release commit

---

## Files Changed

| File | Change |
|------|--------|
| `grammars/JavaParser.g4` | Fixed `this.` → `self.`, updated grammar rules |
| `src/javamcp/antlr4/JavaParser.py` | Regenerated + added predicate methods |
| `src/javamcp/parser/ast_visitor.py` | Fixed `formalParameterList()`, removed unused method |
| `pyproject.toml` | Version bump |
| `CHANGELOG.md` | Release notes |
