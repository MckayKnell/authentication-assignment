from flask import jsonify, request

from db import db
from lib.authenticate import auth, auth_admin
from models.products import Products, product_schema, products_schema
from models.categories import Categories
from util.reflection import populate_object


@auth_admin
def product_add(request):
    post_data = request.form if request.form else request.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "product created", "results": product_schema.dump(new_product)}), 200


@auth_admin
def product_add_category(request):
    post_data = request.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()
    return jsonify({'message': 'category assigned to product', 'results': product_schema.dump(product_query)})


@auth_admin
def product_remove_category(request):
    post_data = request.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.remove(category_query)
    db.session.commit()
    return jsonify({'message': 'category removed from product'})


@auth
def products_get_all(req):
    query = db.session.query(Products).all()

    return jsonify({"message": "products found", "results": products_schema.dump(query)}), 200


@auth
def products_active(req):
    query = db.session.query(Products).filter(Products.active == True).all()

    if not query:
        return jsonify({"message": f'product could not be found'}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(query)}), 200


@auth
def product_by_id(req, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).all()

    if not query:
        return jsonify({"message": f'product could not be found'}), 404

    return jsonify({"message": "product found", "results": product_schema.dump(query)}), 200


@auth_admin
def product_update(request, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    post_data = request.form if request.form else request.get_json()
    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'product updated', 'results': product_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400


@auth_admin
def product_delete(req, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": 'product could not be found'}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete product"})

    return jsonify({'message': 'record has been deleted'})
