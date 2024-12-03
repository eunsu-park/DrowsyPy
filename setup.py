from setuptools import setup, find_packages

setup(
    name="DrowsyPy",
    version="0.1.0",
    author="Eunsu Park",
    description="A Python library written in a drowsy and languid state, collecting and implementing codes for tasks I want to accomplish.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eunsu-park/DrowsyPy",  # GitHub URL 또는 프로젝트 홈페이지
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)