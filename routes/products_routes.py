from flask import Blueprint, request
import controllers

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def product_add():
    return controllers.product_add(request)


@products.route('/product/category', methods=['POST'])
def product_add_category():
    return controllers.product_add_category(request)


@products.route('/products', methods=['GET'])
def products_get_all():
    return controllers.products_get_all(request)


@products.route('/products/active', methods=['GET'])
def products_active():
    return controllers.products_active(request)


@products.route('/product/<product_id>', methods=['GET'])
def product_by_id(product_id):
    return controllers.product_by_id(request, product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def product_update():
    return controllers.product_update(request)


@products.route('/product/category', methods=['DELETE'])
def product_remove_category():
    return controllers.product_remove_category(request)


@products.route('/product/delete/<product_id>', methods=['DELETE'])
def product_delete(product_id):
    return controllers.product_delete(request, product_id)
