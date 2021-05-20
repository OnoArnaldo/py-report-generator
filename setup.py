from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='reportgen',
    version='1.0.0.2',
    description='Generate pdf report from xml, and using pugjs-based template',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arnaldo Ono',
    author_email='git@onoarnaldo.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='pdf generator, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9, <4',

    install_requires=['reportlab', 'xmljson', 'Jinja2', 'pypugjs'],
    extras_require={
        'test': ['pytest'],
    },
)
