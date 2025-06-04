import os
from app import create_app, db, bcrypt
from app.models import User, Category, Product, Cart # Import model yang Anda butuhkan
from datetime import datetime
import random

# Pastikan Anda mengimpor konfigurasi yang benar
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    config_object = 'config.ProductionConfig'
elif config_name == 'testing':
    config_object = 'config.TestingConfig'
else:
    config_object = 'config.DevelopmentConfig'

app = create_app(config_object)

with app.app_context():
    # Pastikan database sudah terhubung
    db.create_all() # Ini akan membuat tabel jika belum ada, atau melakukan apa-apa jika sudah ada (dari upgrade)

    # Hapus data yang sudah ada (opsional, untuk pengujian)
    print("Clearing existing data (optional)...")
    db.session.query(User).delete()
    db.session.query(Category).delete()
    db.session.query(Product).delete()
    db.session.query(Cart).delete() # CartItems dan OrderItems akan terhapus otomatis jika cascade diatur

    # --- Tambahkan User ---
    print("Adding users...")
    # Password default untuk admin dan user biasa (sesuai frontend mock)
    admin_password = 'adminpass'
    user_password = 'password123'

    admin_user = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin_user.set_password(admin_password)
    db.session.add(admin_user)

    regular_user = User(
        username='user',
        email='user@example.com',
        role='customer'
    )
    regular_user.set_password(user_password)
    db.session.add(regular_user)

    db.session.commit() # Commit users dulu agar ID tersedia

    # --- Tambahkan Categories ---
    print("Adding categories...")
    category1 = Category(name='Football Jerseys', description='Official and replica football jerseys.')
    category2 = Category(name='Training Gear', description='Apparel for football training.')
    category3 = Category(name='Fan Merchandise', description='Accessories and other fan items.')

    db.session.add_all([category1, category2, category3])
    db.session.commit()

    # --- Tambahkan Products ---
    print("Adding products...")
    products_data = [
        {'name': 'Classic Red Home Jersey 23/24', 'description': 'Feel the passion with this classic red home jersey. Official replica.', 'price': 750000.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/seed/jersey1/600/400', 'category': category1},
        {'name': 'Dynamic Blue Away Jersey 23/24', 'description': 'Stand out on the road with this sleek blue away jersey. Lightweight and breathable.', 'price': 720000.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/seed/jersey2/600/400', 'category': category1},
        {'name': 'Champions Gold Edition Jersey', 'description': 'Celebrate victory with this limited edition gold jersey. Premium quality.', 'price': 950000.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/seed/jersey3/600/400', 'category': category1},
        {'name': 'Retro Stripes Heritage Jersey', 'description': 'A throwback to a legendary era. Comfortable cotton blend.', 'price': 680000.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/seed/jersey4/600/400', 'category': category1},
        {'name': 'Kids Starter Jersey Pack', 'description': 'Get your young fan started with this comfortable jersey. Includes shorts.', 'price': 450000.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/seed/jersey5/600/400', 'category': category1},
        {'name': 'Pro Training Jersey - Black', 'description': 'High-performance training jersey for serious athletes. Moisture-wicking.', 'price': 550000.00, 'stock_quantity': 0, 'image_url': 'https://picsum.photos/seed/jersey6/600/400', 'category': category1},
        {'name': 'Goalkeeper Gloves Pro-Series', 'description': 'Professional-grade gloves for ultimate grip and protection.', 'price': 350000.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/seed/gloves/600/400', 'category': category2},
        {'name': 'Football Training Cone Set (10 Pcs)', 'description': 'Durable cones for agility and drill training.', 'price': 120000.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/seed/cones/600/400', 'category': category2},
        {'name': 'Team Scarf - Blue & White', 'description': 'Show your team pride with this warm knitted scarf.', 'price': 80000.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/seed/scarf/600/400', 'category': category3},
    ]

    for p_data in products_data:
        # Karena p_data sudah mengandung objek Category, kita bisa langsung menggunakannya
        product = Product(
            name=p_data['name'],
            description=p_data['description'],
            price=p_data['price'],
            stock_quantity=p_data['stock_quantity'],
            image_url=p_data['image_url'],
            category=p_data['category'] # Langsung assign objek Category
        )
        db.session.add(product)

    db.session.commit()

    # --- Buat cart kosong untuk user regular (opsional, bisa dibuat on-demand juga) ---
    print("Creating initial cart for regular user...")
    # Pastikan user sudah ada dan ID-nya valid
    user_from_db = User.query.filter_by(username='user').first()
    if user_from_db:
        existing_cart = Cart.query.filter_by(user_id=user_from_db.id).first()
        if not existing_cart:
            initial_cart = Cart(user_id=user_from_db.id)
            db.session.add(initial_cart)
            db.session.commit()
            print(f"Cart created for user: {user_from_db.username}")
        else:
            print(f"Cart already exists for user: {user_from_db.username}")
    else:
        print("Regular user not found, skipping cart creation.")


    print("Database seeding completed successfully!")
