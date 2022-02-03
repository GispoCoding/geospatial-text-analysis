import csv


def import_service_codes(file: str = "data/PATE_active_categories.csv") -> dict:
    categories = {}
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        header = next(reader)
        if (
            not header[0] == "ID"
            or not header[1] == "NAME"
            or not header[2] == "ORGANIZATION"
            or not header[3] == "PARENT_ID"
        ):
            raise AssertionError(
                "The csv file must have fields ID, NAME, ORGANIZATION, PARENT_ID in that order"
            )
        for row in reader:
            categories[row[0]] = {
                "name": row[1],
                "organization": row[2],
                "parent": row[3],
            }
    return categories
