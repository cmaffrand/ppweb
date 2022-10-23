from werkzeug.security import generate_password_hash
import csv

INPUT_USERS_PATH = 'users.so'
OUPUT_USERS_PATH = 'users.csv'

# Initialize database Users
with open(INPUT_USERS_PATH) as users_csv:
    users_file = csv.reader(users_csv, delimiter=',')
    email = []
    name = []
    passw = []
    for row in users_file:
        email.append(row[0])
        name.append(row[1])
        passw.append(generate_password_hash(row[2], method='sha256'))
    with open(OUPUT_USERS_PATH, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(email)):
            writer.writerow([email[i], name[i], passw[i]])
