import os
import io

from setuptools import find_packages, setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


version = __import__('janyson').__version__

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()
try:
    import pypandoc
    long_description = pypandoc.convert(long_description, 'rst', 'md')
    long_description = long_description.replace('\r', '')
    with io.open('README.rst', mode='w', encoding='utf-8') as f:
        f.write(long_description)
except (ImportError, OSError):
    print("!!! Can't convert README.md - install pandoc and/or pypandoc.")


with io.open('requirements.txt', encoding='utf8') as f:
    install_requires = [l.strip() for l in f.readlines() if
                        l.strip() and not l.startswith('#')]


setup(
    name='django-janyson',
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    license='BSD License',
    description='Virtual model fields that are transparently '
                'mapped to Postgres jsonb',
    long_description=long_description,
    url='https://github.com/un-def/django-janyson',
    author='un.def',
    author_email='un.def@ya.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
