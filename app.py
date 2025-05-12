from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Partner, PartnerType, SalesHistory, Product
import os
from datetime import datetime

app = Flask(__name__)

# Настройка подключения к PostgreSQL с явным указанием кодировки
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres@localhost:5432/partners_db?client_encoding=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Удаляем декоратор before_first_request
# Инициализация таблиц будет в блоке if __name__ == '__main__'

@app.route('/')
def index():
    partners = Partner.query.all()
    return render_template('partners.html', partners=partners)

@app.route('/partner/add', methods=['GET', 'POST'])
def add_partner():
    types = PartnerType.query.all()
    if request.method == 'POST':
        partner = Partner(
            name=request.form['name'],
            type_id=request.form['type_id'],
            rating=request.form['rating'],
            address=request.form['address'],
            director_name=request.form['director_name'],
            phone=request.form['phone'],
            email=request.form['email']
        )
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('partner_form.html', types=types, partner=None)

@app.route('/partner/edit/<int:partner_id>', methods=['GET', 'POST'])
def edit_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    types = PartnerType.query.all()
    if request.method == 'POST':
        partner.name = request.form['name']
        partner.type_id = request.form['type_id']
        partner.rating = request.form['rating']
        partner.address = request.form['address']
        partner.director_name = request.form['director_name']
        partner.phone = request.form['phone']
        partner.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('partner_form.html', types=types, partner=partner)

# Функция для расчета скидки на основе общей суммы продаж
def calculate_discount(partner_id):
    # Получаем все продажи партнера
    sales = SalesHistory.query.filter_by(partner_id=partner_id).all()
    
    # Суммируем общую стоимость продаж
    total_sales_amount = sum(float(sale.total_price) for sale in sales)
    
    # Определяем скидку в соответствии с правилами по общей сумме продаж
    if total_sales_amount < 10000:
        discount = 0
    elif 10000 <= total_sales_amount < 50000:
        discount = 5
    elif 50000 <= total_sales_amount < 300000:
        discount = 10
    else:  # total_sales_amount >= 300000
        discount = 15
        
    return discount, total_sales_amount

@app.route('/partner/<int:partner_id>/history')
def partner_history(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    sales = SalesHistory.query.filter_by(partner_id=partner_id).all()
    
    # Рассчитываем текущую скидку и общую сумму продаж
    discount, total_amount = calculate_discount(partner_id)
    
    return render_template('sales_history.html', partner=partner, sales=sales, 
                          discount=discount, total_amount=total_amount)

@app.route('/partner/<int:partner_id>/add_sale', methods=['GET', 'POST'])
def add_sale(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    products = Product.query.all()
    
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            product_id = request.form['product_id']
            product = Product.query.get_or_404(product_id)
            quantity = int(request.form['quantity'])
            
            # Проверка на допустимое значение quantity
            if quantity <= 0 or quantity > 2147483647:
                return "Ошибка: Количество должно быть положительным числом и не превышать 2147483647"
                
            sale_date = datetime.strptime(request.form['sale_date'], '%Y-%m-%d').date()
            
            # Рассчитываем общую стоимость
            total_price = float(product.price) * quantity
            
            # Создаем новую запись о продаже
            sale = SalesHistory(
                partner_id=partner_id,
                product_id=product_id,
                quantity=quantity,
                sale_date=sale_date,
                total_price=total_price
            )
            
            db.session.add(sale)
            db.session.commit()
            # Пересчитываем скидку
            discount, _ = calculate_discount(partner_id)
            return redirect(url_for('partner_history', partner_id=partner_id))
        except ValueError as e:
            return "Ошибка: Некорректное значение - " + str(e)
        except Exception as e:
            db.session.rollback()
            return "Ошибка при добавлении продажи: " + str(e)
    
    # Передаем текущую дату для поля даты        
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_sale.html', partner=partner, products=products, today_date=today_date)

@app.route('/types')
def types_list():
    types = PartnerType.query.all()
    return render_template('types.html', types=types)

@app.route('/type/add', methods=['GET', 'POST'])
def add_type():
    if request.method == 'POST':
        t = PartnerType(name=request.form['name'])
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('types_list'))
    return render_template('type_form.html', type_obj=None)

@app.route('/type/edit/<int:type_id>', methods=['GET', 'POST'])
def edit_type(type_id):
    t = PartnerType.query.get_or_404(type_id)
    if request.method == 'POST':
        t.name = request.form['name']
        db.session.commit()
        return redirect(url_for('types_list'))
    return render_template('type_form.html', type_obj=t)

if __name__ == '__main__':
    # Создаем таблицы в контексте приложения (если они еще не существуют)
    with app.app_context():
        # Проверяем наличие таблиц и создаем их, если их нет
        db.create_all()
        
        # Проверяем, есть ли типы партнеров, и добавляем если их нет
        if PartnerType.query.count() == 0:
            # Добавляем несколько типов партнеров
            types = [
                PartnerType(name="Дистрибьютор"),
                PartnerType(name="Розничный магазин"),
                PartnerType(name="Оптовый покупатель"),
                PartnerType(name="Поставщик")
            ]
            db.session.add_all(types)
            db.session.commit()
            print("Добавлены типы партнеров")
        
        # Проверяем, есть ли продукты, и добавляем если их нет
        if Product.query.count() == 0:
            # Добавляем несколько продуктов с ценами
            products = [
                Product(name="Товар А", param1=10.5, param2=5.2, price=100.50),
                Product(name="Товар Б", param1=20.0, param2=8.1, price=250.75),
                Product(name="Товар В", param1=15.3, param2=3.7, price=75.25),
                Product(name="Товар Г", param1=30.8, param2=12.4, price=350.00)
            ]
            db.session.add_all(products)
            db.session.commit()
            print("Добавлены тестовые продукты")
            
    app.run(debug=True) 