from flask import Blueprint, request
import controllers

companies = Blueprint('companies', __name__)


@companies.route('/company', methods=['POST'])
def company_add():
    return controllers.company_add(request)


@companies.route('/companies', methods=['GET'])
def companies_get_all():
    return controllers.companies_get_all(request)


@companies.route('/company/<company_id>', methods=['GET'])
def company_by_id(company_id):
    return controllers.company_by_id(request, company_id)


@companies.route('/company/<company_id>', methods=['PUT'])
def company_update():
    return controllers.company_update(request)
