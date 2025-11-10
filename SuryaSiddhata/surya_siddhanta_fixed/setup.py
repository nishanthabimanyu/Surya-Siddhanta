from setuptools import setup, find_packages

setup(
    name='surya_siddhanta',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pytest>=6.0.0',
    ],
    author='Surya Siddhanta Project',
    author_email='surya-siddhanta@example.com',
    description='A rigorously validated Python implementation of the ancient Indian astronomical text Surya Siddhanta.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/surya_siddhanta_fixed', # Placeholder
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)