from extensions import db
from sqlalchemy.orm import synonym


class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id = db.Column(db.Integer, primary_key=True)
    ProductId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    # Synonym for lowercase attribute access
    product_id = synonym('ProductId')

    def __repr__(self):
        return f"<ProductImage {self.name}>"
