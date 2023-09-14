import ckan.plugins.toolkit as tk

import ckan.model as model
from ckan.logic import validate

import ckanext.mailcraft.model as mc_model
from ckanext.mailcraft.logic import schema


@tk.side_effect_free
@validate(schema.mail_list_schema)
def mc_mail_list(context, data_dict):
    """Return a list of mails from database"""
    tk.check_access("mc_mail_list", context, data_dict)

    query = model.Session.query(mc_model.Email)

    if data_dict.get("state"):
        query = query.filter(mc_model.Email.state == data_dict["state"])

    query = query.order_by(mc_model.Email.timestamp.desc())

    return [mail.dictize(context) for mail in query.all()]


@tk.side_effect_free
@validate(schema.mail_show_schema)
def mc_mail_show(context, data_dict):
    """Return a data for a specific mail"""
    tk.check_access("mc_mail_show", context, data_dict)

    return mc_model.Email.get(data_dict["id"]).dictize(context)  # type: ignore
