from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.companies import Companies, company_schema, companies_Schema
from util.reflection import populate_object


@auth_admin
def company_add(req):
    post_data = req.form if req.form else req.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({'message': f'(field) is required'}), 400

        values[field] = field_data

    new_company = Companies(values['company_name'])
    try:
        db.session.add(new_company)
        db.session.commit()
        query = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()
        values['company_id'] = query.company_id
        return jsonify({'message': 'company created', 'result': values}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create record'}), 400


@auth
def companies_get_all(req):
    query = db.session.query(Companies).all()

    return jsonify({"message": "company found", "results": companies_Schema.dump(query)}), 200


@auth
def company_by_id(req, company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).all()

    if not query:
        return jsonify({"message": f'company could not be found'}), 404

    return jsonify({"message": "company found", "results": company_schema.dump(query)}), 200


@auth_admin
def company_update(req, company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    post_data = req.form if req.form else req.get_json()

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'company updated', 'results': {
            'company_id': query.company_id,
            'company_name': query.company_name
        }}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
