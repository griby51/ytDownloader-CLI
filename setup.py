from setuptools import setup, find_packages

setup(name='ytDownloader_cli',
      version='0.1.0',
      description='A simple Youtube Downloader',
      author='Griby51',
      author_email='gritrepailgri@gmail.com',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['dlyt = ytDownloader_cli.cli:main'],
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      intall_requires=['pytubefix']
)