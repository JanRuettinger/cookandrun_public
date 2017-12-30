from ..factory import db
from ..models import Organizer, Team, Event, Participant, Group
from ..equal_groups import EqualGroupsKMeans
from flask import current_app


def delete_groups(event):
    groups = Group.query.filter_by(event_id=event.id).all()

    for g in groups:
        # current_app.logger.info("Team Members: ")
        # current_app.logger.info(t.members)
        # current_app.logger.info(t.members[0].email)
        db.session.delete(g)
        #db.session.delete(t.members[1])
        #db.session.delete(t)

    db.session.commit()
    current_app.logger.info("All Groups deleted.")


def draw_teams(event):
    teams = Team.query.filter_by(event_id=event.id).all()
    number_of_groups = int(len(teams)/9)
    current_app.logger.info("Number of Groups im Event {}".format(number_of_groups))
    current_app.logger.info("Number of Teams im Event {}".format(len(teams)))

    X = [[t.x_cord, t.y_cord] for t in teams]

    clf = EqualGroupsKMeans(n_clusters=number_of_groups)
    clf.fit(X)
    result = clf.predict(X)
    current_app.logger.info(result)
    current_app.logger.info(type(result))
    print(result)
    print(type(result))

    groups = []
    for i in range(number_of_groups):
        g = Group(event_id=event.id)
        db.session.add(g)
        db.session.commit()
        groups.append(g)

    result = list(result)
    for index, t in enumerate(teams):
        t.group_id = groups[result[index]].id

    db.session.commit()

    groups = Group.query.filter_by(event_id=event.id).all()
    for g in groups:
        sort_teams_in_group(g.id)

def sort_teams_in_group(group_id):
    current_app.logger.info("STARTE ORDER_GROUP()")
    group = Group.query.filter_by(id = group_id).first()
    teams = Team.query.filter_by(group_id = group.id).all()
    # current_app.logger.info("Number of Teams: {}".format(len(teams)))
    # current_app.logger.info("ID von Group: {}".format(group.id))
    # current_app.logger.info("0. Team group-id: {}".format(teams[0].group_id))
    # current_app.logger.info("Gruppe Starter-Host(vor) : {}".format(group.starter_1_host))


    # Starter1    Starter2   Starter3
    # 0,1,2       3,4,5     6,7,8

    # Main1       Main2     Main3
    # 1,3,6       4,2,8     7,0,5

    # Dessert1    Dessert2  Dessert3
    # 2,3,7       4,0,6     8,1,5

    group.starter_1_host = teams[0].id
    group.starter_1_guest_1 = teams[1].id
    group.starter_1_guest_2 = teams[2].id
    teams[0].host_1_id = teams[0].id
    teams[1].host_1_id = teams[0].id
    teams[2].host_1_id = teams[0].id

    group.starter_2_host = teams[3].id
    group.starter_2_guest_1 = teams[4].id
    group.starter_2_guest_2 = teams[5].id
    teams[3].host_1_id = teams[3].id
    teams[4].host_1_id = teams[3].id
    teams[5].host_1_id = teams[3].id

    group.starter_3_host = teams[6].id
    group.starter_3_guest_1 = teams[7].id
    group.starter_3_guest_2 = teams[8].id
    teams[6].host_1_id = teams[6].id
    teams[7].host_1_id = teams[6].id
    teams[8].host_1_id = teams[6].id

    group.main_1_host = teams[1].id
    group.main_1_guest_1 = teams[3].id
    group.main_1_guest_2 = teams[6].id
    teams[1].host_2_id = teams[1].id
    teams[3].host_2_id = teams[1].id
    teams[6].host_2_id = teams[1].id

    group.main_2_host = teams[4].id
    group.main_2_guest_1 = teams[2].id
    group.main_2_guest_2 = teams[8].id
    teams[4].host_2_id = teams[2].id
    teams[2].host_2_id = teams[2].id
    teams[8].host_2_id = teams[2].id

    group.main_3_host = teams[7].id
    group.main_3_guest_1 = teams[0].id
    group.main_3_guest_2 = teams[5].id
    teams[7].host_2_id = teams[7].id
    teams[0].host_2_id = teams[7].id
    teams[5].host_2_id = teams[7].id

    group.dessert_1_host = teams[2].id
    group.dessert_1_guest_1 = teams[3].id
    group.dessert_1_guest_2 = teams[7].id
    teams[2].host_3_id = teams[2].id
    teams[3].host_3_id = teams[2].id
    teams[7].host_3_id = teams[2].id

    group.dessert_2_host = teams[4].id
    group.dessert_2_guest_1 = teams[0].id
    group.dessert_2_guest_2 = teams[6].id
    teams[4].host_3_id = teams[4].id
    teams[0].host_3_id = teams[4].id
    teams[6].host_3_id = teams[4].id

    group.dessert_3_host = teams[8].id
    group.dessert_3_guest_1 = teams[1].id
    group.dessert_3_guest_2 = teams[5].id
    teams[8].host_3_id = teams[8].id
    teams[1].host_3_id = teams[8].id
    teams[5].host_3_id = teams[8].id

    db.session.commit()


def change_event_status(event, status):
    # 0: draft_start, 1: draft_finished, 2: registration_open,
    # 3: registration_closed, 4: ready_for_draw, 5: draw_finished,
    # 6: event_started
    try:
        event.status = status
        db.session.add(event)
        db.session.commit()
    except:
        current_app.logger.info("Error: change_event_status")
