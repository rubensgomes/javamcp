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
API indexer for organizing parsed Java classes and methods.
"""

from collections import defaultdict
from typing import Optional

from javamcp.logging import get_logger
from javamcp.models.java_entities import JavaClass, JavaMethod

# Module-level logger
logger = get_logger("indexer")


class APIIndexer:
    """
    Indexes Java classes and methods for fast lookup and searching.
    """

    def __init__(self):
        """Initialize the indexer with empty indices."""
        # Index by fully-qualified class name -> JavaClass
        self.class_index: dict[str, JavaClass] = {}

        # Index by simple class name -> list of JavaClass
        self.class_name_index: dict[str, list[JavaClass]] = defaultdict(list)

        # Index by package name -> list of JavaClass
        self.package_index: dict[str, list[JavaClass]] = defaultdict(list)

        # Index by repository URL -> list of JavaClass
        self.repository_index: dict[str, list[JavaClass]] = defaultdict(list)

        # Index by method name -> list of (JavaClass, JavaMethod)
        self.method_index: dict[str, list[tuple[JavaClass, JavaMethod]]] = defaultdict(
            list
        )

        # Index by class name -> list of methods
        self.class_method_index: dict[str, list[JavaMethod]] = defaultdict(list)

        self._is_built = False

    def add_class(self, java_class: JavaClass, repository_url: str) -> None:
        """
        Add a Java class to the index.

        Args:
            java_class: JavaClass to index
            repository_url: Repository URL this class belongs to
        """
        # Index by fully-qualified name
        self.class_index[java_class.fully_qualified_name] = java_class

        # Index by simple class name
        self.class_name_index[java_class.name].append(java_class)

        # Index by package
        self.package_index[java_class.package].append(java_class)

        # Index by repository
        self.repository_index[repository_url].append(java_class)

        # Index methods
        for method in java_class.methods:
            # Index by method name
            self.method_index[method.name].append((java_class, method))

            # Index by class name -> methods
            self.class_method_index[java_class.fully_qualified_name].append(method)

        self._is_built = True

    def add_classes(self, java_classes: list[JavaClass], repository_url: str) -> None:
        """
        Add multiple Java classes to the index.

        Args:
            java_classes: List of JavaClass objects to index
            repository_url: Repository URL these classes belong to
        """
        logger.info("Indexing %d classes from %s", len(java_classes), repository_url)
        for java_class in java_classes:
            self.add_class(java_class, repository_url)
        logger.debug(
            "Indexing complete: total classes=%d, total methods=%d",
            self.get_total_classes(),
            self.get_total_methods(),
        )

    def reindex_repository(
        self, repository_url: str, java_classes: list[JavaClass]
    ) -> None:
        """
        Re-index a repository by removing old entries and adding new ones.

        Args:
            repository_url: Repository URL to re-index
            java_classes: New list of JavaClass objects
        """
        logger.info(
            "Re-indexing repository: %s with %d classes",
            repository_url,
            len(java_classes),
        )
        # Remove old classes from this repository
        self._remove_repository(repository_url)

        # Add new classes
        self.add_classes(java_classes, repository_url)

    def get_class_by_fqn(self, fully_qualified_name: str) -> Optional[JavaClass]:
        """
        Get a class by its fully-qualified name.

        Args:
            fully_qualified_name: Fully-qualified class name

        Returns:
            JavaClass or None if not found
        """
        return self.class_index.get(fully_qualified_name)

    def get_classes_by_name(self, class_name: str) -> list[JavaClass]:
        """
        Get classes by simple class name.

        Args:
            class_name: Simple class name

        Returns:
            List of matching JavaClass objects
        """
        return self.class_name_index.get(class_name, [])

    def get_classes_by_package(self, package_name: str) -> list[JavaClass]:
        """
        Get classes in a specific package.

        Args:
            package_name: Package name

        Returns:
            List of JavaClass objects in package
        """
        return self.package_index.get(package_name, [])

    def get_classes_by_repository(self, repository_url: str) -> list[JavaClass]:
        """
        Get all classes from a specific repository.

        Args:
            repository_url: Repository URL

        Returns:
            List of JavaClass objects from repository
        """
        return self.repository_index.get(repository_url, [])

    def get_methods_by_name(
        self, method_name: str
    ) -> list[tuple[JavaClass, JavaMethod]]:
        """
        Get methods by method name across all classes.

        Args:
            method_name: Method name to search for

        Returns:
            List of (JavaClass, JavaMethod) tuples
        """
        return self.method_index.get(method_name, [])

    def get_methods_by_class(self, fully_qualified_name: str) -> list[JavaMethod]:
        """
        Get all methods for a specific class.

        Args:
            fully_qualified_name: Fully-qualified class name

        Returns:
            List of JavaMethod objects
        """
        return self.class_method_index.get(fully_qualified_name, [])

    def get_all_classes(self) -> list[JavaClass]:
        """
        Get all indexed classes.

        Returns:
            List of all JavaClass objects
        """
        return list(self.class_index.values())

    def get_total_classes(self) -> int:
        """
        Get total number of indexed classes.

        Returns:
            Total class count
        """
        return len(self.class_index)

    def get_total_methods(self) -> int:
        """
        Get total number of indexed methods.

        Returns:
            Total method count
        """
        return sum(len(methods) for methods in self.class_method_index.values())

    def is_built(self) -> bool:
        """
        Check if index has been built.

        Returns:
            True if index contains data
        """
        return self._is_built

    def clear(self) -> None:
        """Clear all indices."""
        logger.info(
            "Clearing all indices: %d classes, %d methods",
            self.get_total_classes(),
            self.get_total_methods(),
        )
        self.class_index.clear()
        self.class_name_index.clear()
        self.package_index.clear()
        self.repository_index.clear()
        self.method_index.clear()
        self.class_method_index.clear()
        self._is_built = False

    def _remove_repository(self, repository_url: str) -> None:
        """Remove all classes from a repository."""
        if repository_url not in self.repository_index:
            logger.debug(
                "Repository not in index, skipping removal: %s", repository_url
            )
            return

        # Get classes to remove
        classes_to_remove = self.repository_index[repository_url]
        logger.debug(
            "Removing %d classes from index for: %s",
            len(classes_to_remove),
            repository_url,
        )

        for java_class in classes_to_remove:
            # Remove from class index
            self.class_index.pop(java_class.fully_qualified_name, None)

            # Remove from class name index
            if java_class.name in self.class_name_index:
                self.class_name_index[java_class.name] = [
                    c
                    for c in self.class_name_index[java_class.name]
                    if c.fully_qualified_name != java_class.fully_qualified_name
                ]

            # Remove from package index
            if java_class.package in self.package_index:
                self.package_index[java_class.package] = [
                    c
                    for c in self.package_index[java_class.package]
                    if c.fully_qualified_name != java_class.fully_qualified_name
                ]

            # Remove methods from method index
            for method in java_class.methods:
                if method.name in self.method_index:
                    self.method_index[method.name] = [
                        (c, m)
                        for c, m in self.method_index[method.name]
                        if c.fully_qualified_name != java_class.fully_qualified_name
                    ]

            # Remove from class method index
            self.class_method_index.pop(java_class.fully_qualified_name, None)

        # Remove repository entry
        self.repository_index.pop(repository_url, None)
