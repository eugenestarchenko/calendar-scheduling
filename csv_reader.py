import csv
import pprint

oncalls = "./csv_files/Oncalls.csv"
teams = "./csv_files/Teams.csv"
leaders = "./csv_files/Leaders.csv"

available_teamnames = ["Avengers", "Rebels", "Empire", "Fellowship"]

available_rotations = ["Filecoin", "Go", "JavaScript"]


def extract_engineers_info(oncalls):
    print("Extracting data from CSV file for Oncalls")

    try:
        csvReader = csv.DictReader(open(oncalls, mode="r", encoding="utf-8-sig"))

        nestedDict = {}

        for rotation in available_rotations:
            nestedDict[rotation] = {}

        for counter, row in enumerate(csvReader):
            counter = len(nestedDict[dict(row)["rotation"]])
            nestedDict[dict(row)["rotation"]][counter] = dict(row)

    except:
        print("Unable to get data for Oncalls")
        raise
    return nestedDict


rotations = extract_engineers_info(oncalls)


def extract_team_info(teams):
    print("Extracting data from CSV file for Teams")

    try:
        csvReader = csv.DictReader(open(teams, mode="r", encoding="utf-8-sig"))

        nestedDict = {}

        for name in available_teamnames:
            nestedDict[name] = []

        for row in csvReader:
            nestedDict[dict(row)["name"]] = dict(row)

    except:
        print("Unable to get data for Teams")
        raise
    return nestedDict


team_details = extract_team_info(teams)


def extract_leaders_info(leaders):
    print("Extracting data from CSV file for Leaders")

    try:
        csvReader = csv.DictReader(open(leaders, mode="r", encoding="utf-8-sig"))

        Dict = {}

        for row in csvReader:
            Dict[dict(row)["name"]] = dict(row)
    except:
        print("Unable to get data for Leaders")
        raise
    return Dict


emails = extract_leaders_info(leaders)

data = rotations | team_details | emails

if __name__ == "__main__":
    # pprint.pprint(rotations)
    # pprint.pprint(teams)
    # pprint.pprint(emails)
    print(data)
