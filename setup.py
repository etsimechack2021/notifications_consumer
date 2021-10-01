from setuptools import setup, find_packages

setup(name='notifications',
      version='1.0',
      license='Apache 2.0',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=[
          'Flask',
          'flask-restful',
          'requests',
          'simplejson',
          'gevent',
          'werkzeug',
          'Flask-SocketIO',
          'Flask-MQTT'
      ],
      zip_safe=False,
      )
