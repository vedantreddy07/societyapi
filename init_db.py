"""
Database initialization script
Run this to create initial database tables and seed data
"""

from database import engine, SessionLocal
import models
from auth import get_password_hash

def init_db():
    # Create all tables
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    
    # Create initial admin user
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            print("\nCreating default admin user...")
            admin_user = models.User(
                username="admin",
                email="admin@society.com",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                phone_number="1234567890",
                role=models.UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✓ Admin user created successfully!")
            print("\nDefault Login Credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\n⚠️  Please change the password after first login!")
        else:
            print("\n✓ Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Society Management System - Database Initialization")
    print("=" * 50)
    init_db()
    print("\n" + "=" * 50)
    print("Initialization Complete!")
    print("=" * 50)
