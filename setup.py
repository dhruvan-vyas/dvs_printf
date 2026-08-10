from setuptools import setup, find_packages

setup(
    name="dvs_printf",
    version="3.1.0",
    description="Animated Visual appearance for console-based applications, with different animation styles",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",

    author="Dhruvan Vyas",
    author_email="dhruvan_vyas@github.com", 
    maintainer="Dhruvan Vyas",
    url="https://github.com/dhruvan-vyas/dvs_printf",

    license="Apache 2.0",
    keywords=[
        "printf",
        "animation",
        "console",
        "terminal",
        "spinner",
        "loader",
        "progressbar",
        "progress-bar",
        "gradient",
        "gradient-text",
        "colors",
        "ansi",
        "ansi-colors",
        "ansi-styles",
        "text-animation",
        "typing-effect",
        "console-effects",
        "ascii-art",
        "cli",
        "command-line",
        "visuals",
    ],

    packages=find_packages(),
    python_requires=">=3.10",
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Environment :: Console",
    ],

    project_urls={
        "Source": "https://github.com/dhruvan-vyas/dvs_printf",
        "Documentation": "https://github.com/dhruvan-vyas/dvs_printf/blob/main/README.md",
        "Tracker": "https://github.com/dhruvan-vyas/dvs_printf/issues",
    },
)


