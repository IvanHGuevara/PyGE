from subprocess import call
def compiler():
    call("python mapperSetup.py build_ext --inplace")
    call("python populationSetup.py build_ext --inplace ")
compiler()