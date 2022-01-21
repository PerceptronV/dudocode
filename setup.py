"""
“Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.

Software: Dudocode

License: GNU General Public License Version 3

Licensor: SONG YIDING

Dudocode is a pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478).
Copyright (C) 2021  SONG YIDING

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import setuptools
import dudocode

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dudocode",
    version=dudocode.__version__,
    author="PerceptronV",
    author_email="neutrinovs@gmail.com",
    description="A pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PerceptronV/dudocode",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'trilobyte',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'dudo = dudocode.dudo:main'
        ]
    },
    classifiers=[
        "Programming Language :: Other",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Interpreters",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Natural Language :: English"
    ],
    python_requires='>=3.3',
)
