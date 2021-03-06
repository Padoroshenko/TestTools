from setuptools import setup
setup(
  name = 'auchanTestTools',
  packages = ['auchanTestTools'],
  version = '0.4',
  license='MIT',
  description = 'Testing tools/ In development',
  author="Pavel Doroshenko",
  author_email="p.doroshenko@auchan.ru",
  install_requires=[
          'pysftp==0.2.8',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)