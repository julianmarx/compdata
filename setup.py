import setuptools

setuptools.setup(
    name="compdata",
    version="0.0.1",
    author="Julian Marx",
    author_email="jhw.marx@gmail.com",
    description='''The compdata package provides access to the
                   financial comparables data provided by Aswath
                   Damodaran via his website.''',
    url="https://github.com/julianmarx/compdata",
    packages=setuptools.find_packages(),
    keywords = ['finance', 'stocks', 'comparables data']
)
