import nose

try:
    basestring
except NameError:
    basestring = str


def run(argv=None):
    argv_list = ['--logging-clear-handlers', '--nologcapture']
    if argv is not None:
        if isinstance(argv, basestring):
            argv = argv,
        argv_list.extend(argv)
        nose.run(argv=list(set(argv_list)))
    else:
        nose.run(argv=argv_list)

             
