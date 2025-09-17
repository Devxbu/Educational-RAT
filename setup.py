from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="educational-rat",
    version="1.0.0",
    author="Bahri",
    author_email="bahri.official@protonmail.com", 
    description="A modular remote administration tool for educational purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devxbu/Educational-RAT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyautogui>=0.9.54",
        "opencv-python>=4.8.0",
        "requests>=2.31.0",
        "requests-toolbelt>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "edurat-server=main:main",
            "edurat-client=test_client:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
