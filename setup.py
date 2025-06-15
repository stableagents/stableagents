from setuptools import setup, find_packages

setup(
    name="stableagents-ai",
    version="0.2.1",
    packages=find_packages(include=['stableagents', 'stableagents.*']),
    install_requires=[
        "requests>=2.28.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "psutil>=5.9.0",
        "pyppeteer>=1.0.2",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'stableagents-ai=stableagents.run_cli:main',
        ],
    },
    package_data={
        'stableagents': ['*.py', 'core/*.py', 'logic/*.py', 'memory/*.py', 'utils/*.py'],
    },
    include_package_data=True,
    extras_require={
        'local': ['llama-cpp-python>=0.2.0'],
        'all': ['llama-cpp-python>=0.2.0'],
    },
) 