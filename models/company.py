import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


from db import db


class Companies(db.Model):
    __tablename__ = 'Companies'

    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.String(), nullable=False, unique=True)

    products = db.relationship('Products', foreign_keys='[Products.company_id]', back_populates='company', cascade='all,delete')

    def __init__(self, company_name):
        self.company_name = company_name


class CompaniesSchema(ma.Schema):
    class Meta:
        fields = ['company_id', 'company_name', 'products']
    products = ma.fields.Nested("ProductsSchema", many=True, exclude=['company'])


company_schema = CompaniesSchema()
companies_Schema = CompaniesSchema(many=True)


class CompanyNameIDSchema(ma.Schema):
    class Meta:
        fields = ['company_id', 'company_name']


company_name_id_schema = CompanyNameIDSchema()
companyies_name_id_schema = CompanyNameIDSchema(many=True)
