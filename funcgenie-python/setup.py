from setuptools import setup, find_packages

setup(
    name='funcgenie',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'run-funcgenie-server=funcgenie.run_genie:run_genie',
        ],
    },
    author='Shivam Pachchigar',
    author_email='shpachchigar@proton.me',
    description='funcgenie Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/funcgenie',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)
