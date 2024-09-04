with open('/run/secrets/ibl_db_password', 'r') as secret_file:
    db_password = secret_file.read().strip()
    print(f"DB password: {db_password}")