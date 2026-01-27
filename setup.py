# setup.py
# Backward-compatible setup for older pip versions
# All modern configuration is in pyproject.toml

from setuptools import setup
import sys

# For Python < 3.6, we need to explicitly handle version reading
# since f-strings and some modern features aren't available
if sys.version_info < (3, 6):
    import os
    here = os.path.abspath(os.path.dirname(__file__))
    
    def get_version():
        """Read version from __init__.py for older Python versions"""
        version_file = os.path.join(here, 'seqlogo', '__init__.py')
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    # Extract version string
                    delim = '"' if '"' in line else "'"
                    return line.split(delim)[1]
        raise RuntimeError("Unable to find version string.")
    
    def get_long_description():
        """Read README for older Python versions"""
        readme_file = os.path.join(here, 'README.md')
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return "Python port of the R Bioconductor seqlogo package"
    
    # Fallback setup for Python 3.4-3.5
    setup(
        name='seqlogo',
        version=get_version(),
        description='Python port of the R Bioconductor `seqlogo` package',
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        url='https://github.com/betteridiot/seqlogo',
        author='Marcus D. Sherman',
        author_email='mdsherman@betteridiot.tech',
        license='BSD-3-Clause',
        install_requires=[
            'numpy',
            'pandas',
            'weblogo',
        ],
        extras_require={
            'svg': ['ghostscript'],
            'test': ['pytest'],
            'dev': ['pytest', 'ghostscript']
        },
        packages=['seqlogo', 'seqlogo.tests'],
        package_dir={'seqlogo': './seqlogo'},
        package_data={'seqlogo': ['docs/*']},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
        ],
        keywords='sequence logo seqlogo bioinformatics genomics weblogo',
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.4',
    )
else:
    # For Python 3.6+, use pyproject.toml configuration
    setup()

