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
Pydantic models representing Git repository metadata and indices.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .java_entities import JavaClass


class RepositoryMetadata(BaseModel):
    """
    Represents metadata about a Git repository.

    Attributes:
        url: Git repository URL
        branch: Branch name (e.g., "main", "master")
        local_path: Local filesystem path where repository is cloned
        last_cloned: Timestamp of last clone operation
        last_updated: Timestamp of last update (pull) operation
        commit_hash: Current commit hash
    """

    url: str = Field(..., description="Git repository URL")
    branch: str = Field(default="main", description="Branch name")
    local_path: str = Field(..., description="Local clone path")
    last_cloned: Optional[datetime] = Field(None, description="Last clone timestamp")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    commit_hash: Optional[str] = Field(None, description="Current commit hash")


class RepositoryIndex(BaseModel):
    """
    Represents an index of Java classes parsed from a repository.

    Attributes:
        repository: Repository metadata
        classes: List of Java classes parsed from this repository
        total_files: Total number of Java files parsed
        total_classes: Total number of classes found
        total_methods: Total number of methods found
        indexed_at: Timestamp when indexing completed
    """

    repository: RepositoryMetadata = Field(..., description="Repository metadata")
    classes: list[JavaClass] = Field(
        default_factory=list, description="Parsed Java classes"
    )
    total_files: int = Field(default=0, description="Total Java files parsed")
    total_classes: int = Field(default=0, description="Total classes found")
    total_methods: int = Field(default=0, description="Total methods found")
    indexed_at: Optional[datetime] = Field(
        None, description="Indexing completion timestamp"
    )

    def update_counts(self) -> None:
        """Update total counts based on current classes."""
        self.total_classes = len(self.classes)
        self.total_methods = sum(len(cls.methods) for cls in self.classes)
