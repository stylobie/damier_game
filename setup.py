from setuptools import setup

setup(name='damier_game',
      version='0.1',
      description='Jeu des dames',
      url='http://github.com/storborg/funniest',
      author='Serban Vascu',
      author_email='spserban@gmail.com',
      license='MIT',
      packages=['damier_game'],
      install_requires=[
          'pillow',
      ],
      console_scripts= ['damier_game=damier_game.command_line:main'],
      scripts=['bin/damier_game'],
      package_data={'damier_game': ['img/*.png']},
      zip_safe=False)