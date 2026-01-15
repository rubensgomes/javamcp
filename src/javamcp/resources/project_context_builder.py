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
Project context builder for generating comprehensive project documentation.
"""

from pathlib import Path
from typing import Optional

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.logging import get_logger
from javamcp.repository.manager import RepositoryManager

# Module-level logger
logger = get_logger("resources.project_context")


class ProjectContextBuilder:
    """
    Builds comprehensive contextual information about a Java API project.

    Aggregates information from README files, llms.txt, Javadocs,
    and indexed API data to create rich project documentation.
    """

    def __init__(
        self,
        repository_manager: RepositoryManager,
        indexer: APIIndexer,
        query_engine: QueryEngine,
    ):
        """
        Initialize project context builder.

        Args:
            repository_manager: Repository manager for accessing repo files
            indexer: API indexer for accessing indexed classes
            query_engine: Query engine for searching APIs
        """
        self.repository_manager = repository_manager
        self.indexer = indexer
        self.query_engine = query_engine
        self.context_builder = ContextBuilder()

    def build_project_context(self, repository_url: str) -> dict:
        """
        Build comprehensive project context for a repository.

        Args:
            repository_url: Repository URL to build context for

        Returns:
            Dictionary containing complete project context
        """
        logger.info("Building project context for: %s", repository_url)
        metadata = self.repository_manager.get_repository_metadata(repository_url)
        if not metadata:
            logger.warning("Repository not found: %s", repository_url)
            return {"error": f"Repository not found: {repository_url}"}

        repo_path = Path(metadata.local_path)
        repository_name = self._extract_repository_name(repository_url)

        context = {
            "repository_name": repository_name,
            "repository_url": repository_url,
            "description": self._format_project_description(repository_url, repo_path),
            "readme_content": self._extract_readme_content(repo_path),
            "llms_txt_content": self._extract_llms_txt(repo_path),
            "statistics": self._build_api_statistics(repository_url),
            "packages": self._build_package_summary(repository_url),
            "top_classes": self._build_top_classes_summary(repository_url, limit=10),
            "javadoc_coverage": self._calculate_javadoc_coverage(repository_url),
        }

        logger.info(
            "Project context built: %d packages, %d classes",
            len(context["packages"]),
            context["statistics"]["total_classes"],
        )
        return context

    def _extract_repository_name(self, repository_url: str) -> str:
        """
        Extract repository name from URL.

        Args:
            repository_url: Repository URL

        Returns:
            Repository name
        """
        name = repository_url.rstrip("/").split("/")[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name

    def _extract_readme_content(self, repo_path: Path) -> Optional[str]:
        """
        Extract README.md content from repository.

        Args:
            repo_path: Path to repository

        Returns:
            README content or None if not found
        """
        readme_candidates = ["README.md", "README", "readme.md", "Readme.md"]

        for readme_name in readme_candidates:
            readme_path = repo_path / readme_name
            if readme_path.exists() and readme_path.is_file():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    logger.debug("Found README at: %s", readme_path)
                    return content
                except (OSError, UnicodeDecodeError) as e:
                    logger.warning("Failed to read README at %s: %s", readme_path, e)
                    continue

        logger.debug("No README found in repository: %s", repo_path)
        return None

    def _extract_llms_txt(self, repo_path: Path) -> Optional[str]:
        """
        Extract llms.txt or LLMs.txt content from repository.

        Args:
            repo_path: Path to repository

        Returns:
            llms.txt content or None if not found
        """
        llms_candidates = ["llms.txt", "LLMs.txt", "LLMS.txt"]

        for llms_name in llms_candidates:
            llms_path = repo_path / llms_name
            if llms_path.exists() and llms_path.is_file():
                try:
                    content = llms_path.read_text(encoding="utf-8")
                    logger.debug("Found llms.txt at: %s", llms_path)
                    return content
                except (OSError, UnicodeDecodeError) as e:
                    logger.warning("Failed to read llms.txt at %s: %s", llms_path, e)
                    continue

        logger.debug("No llms.txt found in repository: %s", repo_path)
        return None

    def _build_api_statistics(self, repository_url: str) -> dict:
        """
        Build API statistics for repository.

        Args:
            repository_url: Repository URL

        Returns:
            Dictionary with statistics
        """
        try:
            classes = self.query_engine.get_all_apis_from_repository(repository_url)
            total_methods = sum(len(cls.methods) for cls in classes)

            packages = set(cls.package for cls in classes)

            stats = {
                "total_classes": len(classes),
                "total_methods": total_methods,
                "total_packages": len(packages),
                "average_methods_per_class": (
                    round(total_methods / len(classes), 2) if classes else 0
                ),
            }
            logger.debug("API statistics for %s: %s", repository_url, stats)
            return stats
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Failed to build API statistics for %s: %s", repository_url, e
            )
            return {
                "total_classes": 0,
                "total_methods": 0,
                "total_packages": 0,
                "average_methods_per_class": 0,
            }

    def _build_package_summary(self, repository_url: str) -> list[dict]:
        """
        Build summary of packages in repository.

        Args:
            repository_url: Repository URL

        Returns:
            List of package summaries
        """
        try:
            classes = self.query_engine.get_all_apis_from_repository(repository_url)

            packages_map = {}
            for cls in classes:
                if cls.package not in packages_map:
                    packages_map[cls.package] = []
                packages_map[cls.package].append(cls)

            package_summaries = []
            for package_name, package_classes in packages_map.items():
                total_methods = sum(len(cls.methods) for cls in package_classes)

                package_summaries.append(
                    {
                        "name": package_name,
                        "class_count": len(package_classes),
                        "method_count": total_methods,
                        "classes": [cls.name for cls in package_classes[:5]],
                    }
                )

            result = sorted(
                package_summaries, key=lambda x: x["class_count"], reverse=True
            )
            logger.debug(
                "Built package summary for %s: %d packages", repository_url, len(result)
            )
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Failed to build package summary for %s: %s", repository_url, e
            )
            return []

    def _build_top_classes_summary(
        self, repository_url: str, limit: int = 10
    ) -> list[dict]:
        """
        Build summary of top N classes with most context.

        Args:
            repository_url: Repository URL
            limit: Maximum number of classes to include

        Returns:
            List of class summaries with Javadocs
        """
        try:
            classes = self.query_engine.get_all_apis_from_repository(repository_url)

            classes_with_docs = [cls for cls in classes if cls.javadoc]

            sorted_classes = sorted(
                classes_with_docs,
                key=lambda x: len(x.methods) + (10 if x.javadoc else 0),
                reverse=True,
            )

            top_classes = []
            for cls in sorted_classes[:limit]:
                context = self.context_builder.build_class_context(
                    cls, include_methods=False
                )
                top_classes.append(
                    {
                        "name": cls.name,
                        "fully_qualified_name": cls.fully_qualified_name,
                        "package": cls.package,
                        "summary": context.get("summary", ""),
                        "method_count": len(cls.methods),
                        "type": context.get("type", "class"),
                    }
                )

            logger.debug(
                "Built top classes summary for %s: %d classes",
                repository_url,
                len(top_classes),
            )
            return top_classes
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Failed to build top classes summary for %s: %s", repository_url, e
            )
            return []

    def _calculate_javadoc_coverage(self, repository_url: str) -> dict:
        """
        Calculate Javadoc coverage metrics.

        Args:
            repository_url: Repository URL

        Returns:
            Dictionary with coverage metrics
        """
        try:
            classes = self.query_engine.get_all_apis_from_repository(repository_url)

            total_classes = len(classes)
            classes_with_javadoc = sum(1 for cls in classes if cls.javadoc)

            total_methods = sum(len(cls.methods) for cls in classes)
            methods_with_javadoc = sum(
                sum(1 for method in cls.methods if method.javadoc) for cls in classes
            )

            coverage = {
                "class_documentation_rate": (
                    round((classes_with_javadoc / total_classes) * 100, 2)
                    if total_classes > 0
                    else 0
                ),
                "method_documentation_rate": (
                    round((methods_with_javadoc / total_methods) * 100, 2)
                    if total_methods > 0
                    else 0
                ),
                "documented_classes": classes_with_javadoc,
                "total_classes": total_classes,
                "documented_methods": methods_with_javadoc,
                "total_methods": total_methods,
            }
            logger.debug("Javadoc coverage for %s: %s", repository_url, coverage)
            return coverage
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Failed to calculate javadoc coverage for %s: %s", repository_url, e
            )
            return {
                "class_documentation_rate": 0,
                "method_documentation_rate": 0,
                "documented_classes": 0,
                "total_classes": 0,
                "documented_methods": 0,
                "total_methods": 0,
            }

    def _format_project_description(self, repository_url: str, repo_path: Path) -> str:
        """
        Generate comprehensive project description.

        Args:
            repository_url: Repository URL
            repo_path: Path to repository

        Returns:
            Formatted project description
        """
        repository_name = self._extract_repository_name(repository_url)
        stats = self._build_api_statistics(repository_url)

        description_parts = [
            f"# {repository_name}",
            "",
            f"Repository: {repository_url}",
            "",
            "## API Statistics",
            f"- Total Classes: {stats['total_classes']}",
            f"- Total Methods: {stats['total_methods']}",
            f"- Total Packages: {stats['total_packages']}",
            f"- Average Methods per Class: {stats['average_methods_per_class']}",
            "",
        ]

        readme_content = self._extract_readme_content(repo_path)
        if readme_content:
            description_parts.extend(
                [
                    "## Project Overview (from README)",
                    "",
                    readme_content[:1000]
                    + ("..." if len(readme_content) > 1000 else ""),
                    "",
                ]
            )

        return "\n".join(description_parts)
