import csv

from score_display import db
from score_display.models import Gymnast

with open(r"gymnasts.csv","r") as csv_file:
    csv_records = csv.reader(csv_file, delimiter=",")
    for record in csv_records:
        new_rec = Gymnast(
            name=record[0],
            surname=record[1],
            club=record[2],
            age_group=record[3],
            level=record[4],
        )

        db.session.add(new_rec)
db.session.commit()
