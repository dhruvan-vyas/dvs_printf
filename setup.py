from setuptools import setup, find_packages

setup(
    name='dvs_printf',
    version='2.2',
    description=
"Animated Visual appearance for console-based applications, with different animation styles",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dhruvan Vyas',
    maintainer='dhruvan_vyas',
    url='https://github.com/dhruvan-vyas/dvs_printf',
    packages=find_packages(),
    python_requires='>=3.10',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
        "Environment :: Console"
    ],
    keywords = ["printf", "animation", "console", "terminal"],
    license='MIT',
    project_urls={
        'Source': 'https://github.com/dhruvan-vyas/dvs_printf',
        "Documentation": "https://github.com/dhruvan-vyas/dvs_printf/blob/main/README.md",
        'Tracker': 'https://github.com/dhruvan-vyas/dvs_printf/issues'
    },

    include_package_data=True,
    zip_safe=False
)
