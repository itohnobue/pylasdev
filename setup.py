from setuptools import *
setup(
    name = "pyLASDev",
    version = "0.8.1",
    #scripts = ['geo.py'],
        include_package_data = True,
        #package_dir = {'': 'package'},
        packages = ['pylasdev'],
        package_data = {'pylasdev': ['*.py']},

    # metadata for upload to PyPI
    author = "Artur Muharlyamov",
    author_email = "muharlyamovar@ufanipi.ru",
    description = "Python Log ASCII Standart & Deviation files reader/writer",
    license = "BSD",
    keywords = ["geo, wells, las, dev, well, logs, log"]
    #url = "---",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
