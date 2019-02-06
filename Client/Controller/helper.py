import pickle


def dump2file(obj, file):
    with(open(file, 'wb')) as f:
        pickle.dump(obj, f)


def restor_from_file(file):
    rslt = None
    try:
        with(open(file, 'rb')) as f:
            rslt = pickle.load(f)
    except:
        print("No such file")
        pass
    return rslt
