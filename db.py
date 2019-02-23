from db_models import UserInfo


def insert_user_info(db, dialog_id, name, mobile):
    info = UserInfo(dialog_id, name, mobile)
    db.session.add(info)
