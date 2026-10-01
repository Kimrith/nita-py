import os
from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from model import User, Category, Product, ProductImage
from helper import load_users, save_users


def seed_database():
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        print("Initializing database tables...")

        # Seed Users (Admins and Customers)
        seed_users_data = [
            {
                "fullname": "CHAY NITA",
                "email": "admin@techey.tech",
                "password": "admin123",
                "role": "Admin",
                "status": "Active",
                "image": "/static/uploads/20260824153548_profile.jpg"
            },
            {
                "fullname": "CHANRITH ROUNG",
                "email": "chanrith@techey.tech",
                "password": "admin123",
                "role": "Admin",
                "status": "Active",
                "image": None
            },
            {
                "fullname": "Sokha Chen",
                "email": "sokha@gmail.com",
                "password": "password123",
                "role": "Customer",
                "status": "Active",
                "image": None
            },
            {
                "fullname": "Bopha Vong",
                "email": "bopha@gmail.com",
                "password": "password123",
                "role": "Customer",
                "status": "Active",
                "image": None
            },
            {
                "fullname": "Dara Kim",
                "email": "dara@gmail.com",
                "password": "password123",
                "role": "Customer",
                "status": "Active",
                "image": None
            },
            {
                "fullname": "John Smith",
                "email": "john@gmail.com",
                "password": "password123",
                "role": "Customer",
                "status": "Inactive",
                "image": None
            }
        ]

        added_count = 0
        updated_count = 0
        json_users = load_users()

        for u in seed_users_data:
            email = u["email"]
            existing = User.query.filter_by(email=email).first()
            hashed_pwd = generate_password_hash(u["password"])

            if not existing:
                new_user = User(
                    fullname=u["fullname"],
                    email=email,
                    password=hashed_pwd,
                    role=u["role"],
                    status=u["status"],
                    image=u["image"]
                )
                db.session.add(new_user)
                added_count += 1
                print(f"[+] Created {u['role']}: {u['fullname']} ({email})")
            else:
                # Guarantee admin access by updating existing admin password & role
                if u["role"] == "Admin":
                    existing.password = hashed_pwd
                    existing.role = "Admin"
                    existing.status = "Active"
                    if u["image"] and not existing.image:
                        existing.image = u["image"]
                    updated_count += 1
                    print(f"[~] Refreshed Admin access for: {email}")
                else:
                    print(f"[-] User already exists: {email}")

            # Keep JSON backup synced
            json_users[email] = {
                "name": u["fullname"],
                "email": email,
                "password": hashed_pwd,
                "role": u["role"],
                "status": u["status"]
            }

        # Seed Categories
        categories_data = [
            {"name": "Electronics", "image": "/static/uploads/electronics.jpg", "description": "High-tech gadgets, headphones, and electronics."},
            {"name": "Fashion", "image": "/static/uploads/fashion.jpg", "description": "Trendy clothing and daily wear."},
            {"name": "Accessories", "image": "/static/uploads/accessories.jpg", "description": "Bags, watches, and personal accessories."},
            {"name": "Home & Kitchen", "image": "/static/uploads/home.jpg", "description": "Essential home appliances and kitchenware."}
        ]

        category_map = {}
        for c in categories_data:
            cat = Category.query.filter_by(name=c["name"]).first()
            if not cat:
                cat = Category(name=c["name"], image=c["image"], description=c["description"])
                db.session.add(cat)
                db.session.flush()
                print(f"[+] Created Category: {c['name']}")
            category_map[c["name"]] = cat.id

        db.session.commit()
        save_users(json_users)

        print("\n=======================================================")
        print("  Database Seeding Completed Successfully!")
        print(f"  - New Accounts Created : {added_count}")
        print(f"  - Admins Refreshed     : {updated_count}")
        print("=======================================================")
        print("  Admin Credentials for Dashboard Access:")
        print("  • Email    : admin@techey.tech")
        print("  • Password : admin123")
        print("  • URL      : http://127.0.0.1:5001/admin/login")
        print("=======================================================\n")


if __name__ == "__main__":
    seed_database()
