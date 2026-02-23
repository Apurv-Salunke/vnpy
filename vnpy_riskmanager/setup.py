import os

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize


def get_version() -> str:
    """From __init__.py Read version number"""
    with open("vnpy_riskmanager/__init__.py", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "1.0.0"


# Define Cython extension to compile
extensions = [
    Extension(
        "vnpy_riskmanager.template",
        [os.path.join("vnpy_riskmanager", "template.pyx")],
    ),
    Extension(
        "vnpy_riskmanager.rules.active_order_rule_cy",
        [os.path.join("vnpy_riskmanager", "rules", "active_order_rule_cy.pyx")],
    ),
    Extension(
        "vnpy_riskmanager.rules.daily_limit_rule_cy",
        [os.path.join("vnpy_riskmanager", "rules", "daily_limit_rule_cy.pyx")],
    ),
    Extension(
        "vnpy_riskmanager.rules.duplicate_order_rule_cy",
        [os.path.join("vnpy_riskmanager", "rules", "duplicate_order_rule_cy.pyx")],
    ),
    Extension(
        "vnpy_riskmanager.rules.order_size_rule_cy",
        [os.path.join("vnpy_riskmanager", "rules", "order_size_rule_cy.pyx")],
    ),
    Extension(
        "vnpy_riskmanager.rules.order_validity_rule_cy",
        [os.path.join("vnpy_riskmanager", "rules", "order_validity_rule_cy.pyx")],
    )
]

# Cython compileConfig
compiler_directives = {
    "language_level": "3",              # Python 3 syntax
    "boundscheck": False,               # DisableboundaryCheck（performanceOptimization）
    "wraparound": False,                # Disablenegativeindex（performanceOptimization）
    "cdivision": True,                  # C style division（notCheckdiv by zero）
    "initializedcheck": False,          # DisableInitializeCheck
    "embedsignature": True,             # embedinFunctionSign（for debugging）
}

setup(
    name="vnpy_riskmanager",
    version=get_version(),
    packages=find_packages(),
    ext_modules=cythonize(
        extensions,
        compiler_directives=compiler_directives,
        annotate=False,     # Set to True to generate HTML performance analysis file
    ),
    package_data={
        "vnpy_riskmanager": ["*.pxd", "*.pyx"],  # Include Cython source files
    },
    zip_safe=False,         # Cython extendNot supported zip pack
)
