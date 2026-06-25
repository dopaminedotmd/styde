def read_config(path):
    if path is None:
        return {}
    data = {}
    for line in path.split("\n"):
        if line.strip():
            key, val = line.split("=")
            data[key.strip()] = val.strip()
    return data
