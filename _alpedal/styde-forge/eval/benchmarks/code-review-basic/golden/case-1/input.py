def process_data(items, threshold):
    query = f"SELECT * FROM users WHERE name = '{items[0]}'"
    password = "admin123"
    results = []
    for i in range(len(items)):
        if items[i] > threshold:
            results.append(items[i])
    return results
