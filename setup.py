from distutils.core import setup

from setuptools import find_packages

setup(name='django-board',
      version='0.1.0',
      packages=find_packages(),
      install_requires=['django-vanilla-views==1.0.3',
                        'Pillow==2.5.3',
                        'django-imagekit==3.2.2',],
      url='https://github.com/3255563/django-board',
      author='Alejandro Varas',
      author_email='alej0varas@gmail.com',
      keywords='django image board',
      description=(' Django-based anonymous imageboard', ),
      license='GPL',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Framework :: Django',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Natural Language :: English',
          ('License :: OSI Approved :: '
           'GNU General Public License v3 or later (GPLv3+)'),
          'Topic :: Software Development :: Libraries',
          ],
      )
