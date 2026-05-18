def parse_par(text):
    vals = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            k, v = parts[0], parts[1]
            try:
                vals[k] = float(v.replace("D", "E"))
            except ValueError:
                vals[k] = v
    return vals