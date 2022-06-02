from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="plexflo",
    version="1.0.1",
    author="Plexflo",
    author_email="hello@plexflo.com",
    description="Open-source Python wrapper around Plexflo's apps, APIs, and algorithms that help researchers, engineers and energy companies build intelligence, apps, and dashboards to accelerate clean-tech adoption across all communities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plexflo/plexflo",
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['numpy', 'pandas', 'sklearn', 'openpyxl', 'pathlib', 'tensorflow', 'matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)