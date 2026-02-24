import csv

contacts = [
    ["name", "email", "attachment"],
    ["John", "John@example.com",
        r"attachment1 path"],
    ["Mosh", "Mosh@example.com",
        r"attachment2 path"],
    ["Brian", "Brian@example.com",
        r"attachment3 path"]

]

with open("contacts_example.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(contacts)

print("Csv written")
