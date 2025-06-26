from setuptools import setup, find_packages

setup(
    name="error_404_modelsembeddinggecko001_is_not_found",
    version="1.0.0",
    description="A desktop application created with Stable Desktop",
    author="Stable Desktop",
    packages=find_packages(),
    install_requires=[
        "pillow>=8.0.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "error_404_modelsembeddinggecko001_is_not_found=main:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)