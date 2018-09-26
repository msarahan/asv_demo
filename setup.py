from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='asv_demo',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Short description",
    author="Michael Sarahan",
    author_email='msarahan@gmail.com',
    url='https://github.com/msarahan/asv_demo',
    packages=['asv_demo'],
    entry_points={
        'console_scripts': [
            'asv_demo=asv_demo.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='asv_demo',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
