import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="SPF50-security-fuzzer",
    version=os.getenv('PKG_VERSION', '0.0.1'),
    author="VivaSecuris",
    author_email="vivasecuris@pm.me",
    description="Security Fuzzer for Healthcare LLMs",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/VivaSecuris/SPF50",
    packages=find_packages(),
    package_data={
        'SPF50': ['attack_data/*'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: Unlicense",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires='>=3.7',
    install_requires=[
        "openai==1.6.1",
        "langchain==0.0.353",
        "langchain-community==0.0.7",
        "langchain-core==0.1.4",
        "argparse==1.4.0",
        "python-dotenv==1.0.0",
        "tqdm==4.66.1",
        "colorama==0.4.6",
        "prettytable==3.10.0",
        "pandas==2.2.2",
        "inquirer==3.2.4",
        "prompt-toolkit==3.0.43",
        "fastparquet==2024.2.0",
        "streamlit==1.26.0",  # Added for the streamlit app
        'ollama',
    ],
    extras_require={
        "dev": ["pytest==7.4.4"]
    },
    entry_points={
        'console_scripts': [
            'spf50-security-fuzzer=SPF50.main:main',  # Updated entry point
        ],
    },
    license="Unlicensed",
)
