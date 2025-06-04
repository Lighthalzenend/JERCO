import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Category, Product, Cart, CartItem, Order, OrderItem # Import model Anda di sini

# Tentukan konfigurasi berdasarkan FLASK_ENV
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    config_object = 'config.ProductionConfig'
elif config_name == 'testing':
    config_object = 'config.TestingConfig'
else:
    config_object = 'config.DevelopmentConfig'

app = create_app(config_object)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    # Menambahkan objek ke shell Flask agar mudah diakses
    return dict(db=db, User=User, Category=Category, Product=Product, 
                Cart=Cart, CartItem=CartItem, Order=Order, OrderItem=OrderItem)

if __name__ == '__main__':
    app.run(debug=True)