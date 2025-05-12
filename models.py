from flask_sqlalchemy import SQLAlchemy

# Инициализация SQLAlchemy

db = SQLAlchemy()

class PartnerType(db.Model):
    __tablename__ = 'partner_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    partners = db.relationship('Partner', backref='type', lazy=True)

class Partner(db.Model):
    __tablename__ = 'partner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('partner_type.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255))
    director_name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    sales = db.relationship('SalesHistory', backref='partner', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    param1 = db.Column(db.Numeric, nullable=False)
    param2 = db.Column(db.Numeric, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    sales = db.relationship('SalesHistory', backref='product', lazy=True)
    product_materials = db.relationship('ProductMaterial', backref='product', lazy=True)

class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product_materials = db.relationship('ProductMaterial', backref='material', lazy=True)

class SalesHistory(db.Model):
    __tablename__ = 'sales_history'
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)

class ProductMaterial(db.Model):
    __tablename__ = 'product_material'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    product_coefficient = db.Column(db.Numeric, nullable=False)
    defect_percent = db.Column(db.Numeric, nullable=False) 