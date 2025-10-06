"""
Integration test demonstrating GitRepositoryManager persistent storage.

This test verifies that GitRepositoryManager:
1. Persists repositories to local folders
2. Checks if repository exists before cloning
3. Syncs existing repositories instead of re-cloning
"""

from pathlib import Path

import pytest

from javamcp.repositories import GitRepositoryManager


class TestPersistentStorage:
    """Test persistent storage and check-before-clone behavior."""

    def test_persistent_storage_and_check_before_clone(
        self,
        test_repository_url: str,
        tmp_path: Path
    ) -> None:
        """
        Verify persistent storage and check-before-clone logic.

        This test demonstrates that GitRepositoryManager:
        - Stores repositories in a persistent local folder
        - Checks if repository exists before attempting to clone
        - Syncs existing repositories instead of re-cloning

        Args:
            test_repository_url: URL of the test repository
            tmp_path: Temporary directory for testing
        """
        persistent_folder = tmp_path / "persistent_repos"

        print("\n" + "=" * 60)
        print("PERSISTENT STORAGE DEMONSTRATION")
        print("=" * 60)

        # =====================================================
        # STEP 1: First clone - repository does not exist
        # =====================================================
        print(
            f"\n[STEP 1] First run - repository does not exist yet"
        )
        print(
            f"[STEP 1] Persistent folder: {persistent_folder}"
        )

        manager1 = GitRepositoryManager(
            [test_repository_url],
            persistent_folder
        )

        print(
            f"[STEP 1] Checking if repository exists locally..."
        )
        repo_config = manager1.repositories[0]
        exists_before_clone = manager1._repository_exists(
            repo_config
        )

        print(
            f"[STEP 1] Repository exists: {exists_before_clone}"
        )
        assert not exists_before_clone, (
            "Repository should not exist before first clone"
        )

        print("[STEP 1] Processing repositories (will clone)...")
        results1 = manager1.process_repositories()

        assert len(results1) == 1
        assert results1[0].success

        cloned_path = results1[0].repository.local_path

        print(
            f"[STEP 1] ✅ Repository cloned to: {cloned_path}"
        )
        assert cloned_path.exists()
        assert (cloned_path / ".git").exists()

        # =====================================================
        # STEP 2: Second run - repository already exists
        # =====================================================
        print(
            f"\n[STEP 2] Second run - repository already exists"
        )

        manager2 = GitRepositoryManager(
            [test_repository_url],
            persistent_folder
        )

        print(
            f"[STEP 2] Checking if repository exists locally..."
        )
        repo_config2 = manager2.repositories[0]
        exists_before_sync = manager2._repository_exists(
            repo_config2
        )

        print(
            f"[STEP 2] Repository exists: {exists_before_sync}"
        )
        assert exists_before_sync, (
            "Repository should exist from previous clone"
        )

        print(
            "[STEP 2] Processing repositories "
            "(will sync, not re-clone)..."
        )
        results2 = manager2.process_repositories()

        assert len(results2) == 1
        assert results2[0].success

        synced_path = results2[0].repository.local_path

        print(
            f"[STEP 2] ✅ Repository synced at: {synced_path}"
        )
        assert synced_path == cloned_path, (
            "Sync should use same path as clone"
        )
        assert synced_path.exists()
        assert (synced_path / ".git").exists()

        # =====================================================
        # STEP 3: Verify persistent folder structure
        # =====================================================
        print("\n[STEP 3] Verifying persistent folder structure")

        print(
            f"[STEP 3] Persistent folder: {persistent_folder}"
        )
        assert persistent_folder.exists()
        assert persistent_folder.is_dir()

        repo_folders = list(persistent_folder.iterdir())
        print(
            f"[STEP 3] Repository folders: "
            f"{[f.name for f in repo_folders]}"
        )

        assert len(repo_folders) == 1
        assert repo_folders[0] == cloned_path

        # =====================================================
        # STEP 4: Summary
        # =====================================================
        print("\n" + "=" * 60)
        print("PERSISTENT STORAGE VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Repository URL: {test_repository_url}")
        print(f"Persistent folder: {persistent_folder}")
        print(f"Repository stored at: {cloned_path}")
        print(f"First run: CLONED ✅")
        print(f"Second run: SYNCED (not re-cloned) ✅")
        print(f"Persistent storage: VERIFIED ✅")
        print(f"Check-before-clone: VERIFIED ✅")
        print("=" * 60)
