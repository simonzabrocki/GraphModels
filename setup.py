from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()
    required = [r.split('==')[0] for r in required]

setup(
    name='ggmodel_dev',
    version='0.0.13',
    description='A Python package for creating graphical models',
    url='https://github.com/Global-Green-Growth-Institute/GraphModels',
    author='Simon Zabrocki',
    author_email='simon.zabrocki@gmail.com',
    license='BSD 2-clause',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['ggmodel_dev'],
    package_dir={'ggmodel_dev': 'ggmodel/'},
    install_requires=required,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
    ],
)

