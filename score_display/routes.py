import json

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from score_display import app, db

from score_display.models import Gymnast, GymnastScores, ActiveSet, Apparatus

gmnst_app_lvl = {
    "Level 8": ["FX", "Rope", "Ball"],
    "Level 9": ["Hoop", "Ball", "Clubs"],
    "Level 10": ["Hoop", "Ball", "Clubs", "Ribbon"],
    "Pre-Junior": ["Rope", "Ball", "Clubs", "Ribbon"],
    "Junior": ["Rope", "Ball", "Clubs", "Ribbon"],
    "Senior": ["Hoop", "Ball", "Clubs", "Ribbon"],
    "HP 1": ["FX", "Rope", "Ball", "Clubs"],
    "HP 2": ["FX", "Hoop", "Clubs", "Ribbon"]
}

@app.route("/", methods=("GET", "POST"))
def index():
    active_set = ActiveSet.query.all()

    gymnasts = []
    gym_details = Gymnast.query.all()
    for g in gym_details:
        gymnasts.append(" ".join([g.name, g.surname]))

    for_display = []

    if request.method == "POST":
        form_result = request.form.to_dict()
        for result in form_result:
            #Firs, get which set(s) are active
            if "active_" in result:
                for_display.append(result[result.index("_") +1:])

        #now we've got all the active sets... clear what was set first
        for row in ActiveSet.query.all():
            row.is_active = False
            db.session.add(row)
        db.session.commit()

        #Set wat is active now
        for display in for_display:
            row = ActiveSet.query.filter_by(level=display).first()
            row.is_active = True
            db.session.add(row)
        db.session.commit()

        #now, let's update the gymnast score
        #get the gymnast to update
        #Some surnames have spaces and split wont work too well, 
        tmp_gymnst = form_result.get("gymnast_list").split()

        gymnst = Gymnast.query.filter_by(
            name=tmp_gymnst.pop(0),
            surname=" ".join(tmp_gymnst)
            ).first()
        apparatus = Apparatus.query.filter_by(name=form_result.get("gymnast_app")).first()

        if not gymnst or not apparatus:
            flash("couldn't find the gymnast or the appartus", "danger")
            return redirect(url_for("index"))

        if form_result.get("gymnast_score") is not "":
            #do nothing
            score = GymnastScores(gymnast_id=gymnst.id, apparatus_id=apparatus.id, final_score=form_result.get("gymnast_score"))

            db.session.add(score)
            try:
                db.session.commit()
                flash(f"Added {form_result.get('gymnast_list')}: {form_result.get('gymnast_app')} > {form_result.get('gymnast_score')}", "success")
            except IntegrityError:
                db.session.rollback()
                flash("Oops... {} already had a {} score".format(form_result["gymnast_list"], form_result["gymnast_app"]), "danger")
        else:
            print("not updating gymnast", "info")

    return render_template("index.html", title="Competition", active_set=active_set, gymnast_detail=json.dumps(gymnasts), gymnasts=gymnasts)

@app.route("/display_scores")
def display_scores():
    
    #Get the active set to display
    active = ActiveSet.query.filter_by(is_active=True).all()
    active_level = []
    for activ in active:
        active_level.append(activ.level)

    gymnasts = Gymnast.query.filter(Gymnast.level.in_(active_level)).all()

    gymnast={}
    x = 0
    for g in gymnasts:
        gymnast[x] = {"name": f"{g.name} {g.surname}"}
        gymnast[x].update({"level":g.level})
        gymnast[x].update({"age":g.age_group})
        gymnast[x].update({"club":g.club})
        for s in g.scores:
            gymnast[x].update({s.apparatus.name : s.final_score})
        x += 1

    return render_template("display_scores.html", gymnasts=gymnasts, active_level=active_level, gym_dict=gymnast)