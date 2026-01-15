# General Disclaimer
#
# **AI Generated Content**
#
# This project's source code and documentation were generated predominantly
# by an Artificial Intelligence Large Language Model (AI LLM). The project
# lead, [Rubens Gomes](https://rubensgomes.com), provided initial prompts,
# reviewed, and made refinements to the generated output. While human review and
# refinement have occurred, users should be aware that the output may contain
# inaccuracies, errors, or security vulnerabilities
#
# **Third-Party Content Notice**
#
# This software may include components or snippets derived from third-party
# sources. The software's users and distributors are responsible for ensuring
# compliance with any underlying licenses applicable to such components.
#
# **Copyright Status Statement**
#
# Copyright protection, if any, is limited to the original human contributions and
# modifications made to this project. The AI-generated portions of the code and
# documentation are not subject to copyright and are considered to be in the
# public domain.
#
# **Limitation of liability**
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# **No-Warranty Disclaimer**
#
# THIS SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

"""
Query engine for searching and filtering indexed Java APIs.
"""

from typing import Optional

from javamcp.logging import get_logger
from javamcp.models.java_entities import JavaClass, JavaMethod

from .exceptions import IndexNotBuiltError, RepositoryNotIndexedError
from .indexer import APIIndexer

# Module-level logger
logger = get_logger("indexer.query")


class QueryEngine:
    """
    Provides search and filtering capabilities over indexed Java APIs.
    """

    def __init__(self, indexer: APIIndexer):
        """
        Initialize query engine with an indexer.

        Args:
            indexer: APIIndexer instance to query
        """
        self.indexer = indexer

    def search_methods(
        self,
        method_name: str,
        class_name: Optional[str] = None,
        case_sensitive: bool = False,
    ) -> list[tuple[JavaClass, JavaMethod]]:
        """
        Search for methods by name with optional class filter.

        Args:
            method_name: Method name to search for
            class_name: Optional class name filter
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of (JavaClass, JavaMethod) tuples

        Raises:
            IndexNotBuiltError: If index is not built
        """
        logger.debug(
            "Searching methods: name=%s, class=%s, case_sensitive=%s",
            method_name,
            class_name,
            case_sensitive,
        )
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        results = []

        # Get all methods matching the name
        if case_sensitive:
            matching_methods = self.indexer.get_methods_by_name(method_name)
        else:
            # Case-insensitive search
            matching_methods = []
            for name, methods in self.indexer.method_index.items():
                if name.lower() == method_name.lower():
                    matching_methods.extend(methods)

        # Apply class name filter if specified
        if class_name:
            if case_sensitive:
                results = [
                    (cls, method)
                    for cls, method in matching_methods
                    if cls.name == class_name
                ]
            else:
                results = [
                    (cls, method)
                    for cls, method in matching_methods
                    if cls.name.lower() == class_name.lower()
                ]
        else:
            results = matching_methods

        logger.debug("Method search returned %d results", len(results))
        return results

    def search_methods_partial(
        self, method_name_pattern: str, case_sensitive: bool = False
    ) -> list[tuple[JavaClass, JavaMethod]]:
        """
        Search for methods by partial name matching.

        Args:
            method_name_pattern: Partial method name pattern
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of (JavaClass, JavaMethod) tuples

        Raises:
            IndexNotBuiltError: If index is not built
        """
        logger.debug(
            "Searching methods partial: pattern=%s, case_sensitive=%s",
            method_name_pattern,
            case_sensitive,
        )
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        results = []

        # Search through all method names
        for name, methods in self.indexer.method_index.items():
            if case_sensitive:
                if method_name_pattern in name:
                    results.extend(methods)
            else:
                if method_name_pattern.lower() in name.lower():
                    results.extend(methods)

        logger.debug("Partial method search returned %d results", len(results))
        return results

    def search_class(
        self, class_name: str, case_sensitive: bool = False
    ) -> Optional[JavaClass]:
        """
        Search for a class by fully-qualified name.

        Args:
            class_name: Fully-qualified class name
            case_sensitive: Whether search is case-sensitive

        Returns:
            JavaClass or None if not found

        Raises:
            IndexNotBuiltError: If index is not built
        """
        logger.debug(
            "Searching class: name=%s, case_sensitive=%s", class_name, case_sensitive
        )
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        if case_sensitive:
            result = self.indexer.get_class_by_fqn(class_name)
            logger.debug("Class search result: %s", "found" if result else "not found")
            return result

        # Case-insensitive search
        for fqn, java_class in self.indexer.class_index.items():
            if fqn.lower() == class_name.lower():
                logger.debug("Class search result: found (case-insensitive match)")
                return java_class
        logger.debug("Class search result: not found")
        return None

    def filter_classes_by_repository(self, repository_url: str) -> list[JavaClass]:
        """
        Filter classes by repository URL.

        Args:
            repository_url: Repository URL to filter by

        Returns:
            List of JavaClass objects from repository

        Raises:
            IndexNotBuiltError: If index is not built
            RepositoryNotIndexedError: If repository not in index
        """
        logger.debug("Filtering classes by repository: %s", repository_url)
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        classes = self.indexer.get_classes_by_repository(repository_url)

        if not classes:
            logger.warning("Repository not indexed: %s", repository_url)
            raise RepositoryNotIndexedError(f"Repository not indexed: {repository_url}")

        logger.debug("Found %d classes in repository", len(classes))
        return classes

    def filter_classes_by_package(
        self, package_name: str, repository_url: Optional[str] = None
    ) -> list[JavaClass]:
        """
        Filter classes by package name with optional repository filter.

        Args:
            package_name: Package name to filter by
            repository_url: Optional repository URL filter

        Returns:
            List of JavaClass objects in package

        Raises:
            IndexNotBuiltError: If index is not built
        """
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        classes = self.indexer.get_classes_by_package(package_name)

        # Apply repository filter if specified
        if repository_url:
            repo_classes = set(
                c.fully_qualified_name
                for c in self.indexer.get_classes_by_repository(repository_url)
            )
            classes = [c for c in classes if c.fully_qualified_name in repo_classes]

        return classes

    def get_all_apis_from_repository(self, repository_url: str) -> list[JavaClass]:
        """
        Get all APIs from a specific repository.

        Args:
            repository_url: Repository URL

        Returns:
            List of all JavaClass objects from repository

        Raises:
            IndexNotBuiltError: If index is not built
            RepositoryNotIndexedError: If repository not in index
        """
        return self.filter_classes_by_repository(repository_url)

    def get_all_apis_from_package(
        self, package_name: str, repository_url: str
    ) -> list[JavaClass]:
        """
        Get all APIs from a specific package in a repository.

        Args:
            package_name: Package name
            repository_url: Repository URL

        Returns:
            List of JavaClass objects

        Raises:
            IndexNotBuiltError: If index is not built
        """
        return self.filter_classes_by_package(package_name, repository_url)

    def get_classes_by_name(
        self, class_name: str, case_sensitive: bool = False
    ) -> list[JavaClass]:
        """
        Get classes by simple class name.

        Args:
            class_name: Simple class name
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of matching JavaClass objects

        Raises:
            IndexNotBuiltError: If index is not built
        """
        if not self.indexer.is_built():
            raise IndexNotBuiltError("Index has not been built")

        if case_sensitive:
            return self.indexer.get_classes_by_name(class_name)

        # Case-insensitive search
        results = []
        for name, classes in self.indexer.class_name_index.items():
            if name.lower() == class_name.lower():
                results.extend(classes)
        return results

    def get_statistics(self) -> dict[str, int]:
        """
        Get index statistics.

        Returns:
            Dictionary with statistics (total_classes, total_methods, etc.)
        """
        return {
            "total_classes": self.indexer.get_total_classes(),
            "total_methods": self.indexer.get_total_methods(),
            "total_repositories": len(self.indexer.repository_index),
            "total_packages": len(self.indexer.package_index),
        }
