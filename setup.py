from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='flask_prometheus',
    py_modules=['flask_prometheus'],
    version='0.0.2',
    description='Prometheus metrics exporter for Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Ometria',
    author_email='devs@ometria.com',
    url='https://github.com/Ometria/flask-prometheus',
    download_url='https://github.com/Ometria/flask-prometheus/archive/0.0.1.tar.gz',
    keywords=['prometheus', 'flask', 'monitoring', 'exporter'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=['prometheus_client', 'flask'],
)
