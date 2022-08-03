from setuptools import setup, find_packages

long_description = """"
## Plexflo
Plexflo offers a comprehensive ecosystem of tools and libraries that lets you build Deep Learning powered applications for effective management of grid with accurate forecasting and analytics.

### Plexflo's Open-Source library
We have built an Open-Source library datastream that aids researchers and engineers to try our Deep Learning models for detection of EVs (Electric Vehicles) charging events from smart home meter data.

### datastream
datastream helps researchers and engineers to try our Deep Learning models for detection of Electric Vehicles charging events from smart home meter data.

### connect
connect helps users to leverage our easy-to-use socket programming wrapper for hassle free client-server use-cases.

### loadprofiles
loadprofiles helps researchers and engineers to try our pre-defined 24-hour load profiles for various scenarios in their load forecasting use-cases.

### utils
utils helps users take advantage of our easy-to-use mathematical and statistical functions.
"""

setup(
    name="plexflo",
    version="1.2.0",
    author="Plexflo",
    author_email="hello@plexflo.com",
    description="Open-source Python wrapper around Plexflo's apps, APIs, and algorithms that help researchers, engineers and energy companies build intelligence, apps, and dashboards to accelerate clean-tech adoption across all communities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plexflo/plexflo",
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['numpy', 'pandas', 'sklearn', 'openpyxl', 'pathlib', 'matplotlib', 'scipy', 'fitter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)