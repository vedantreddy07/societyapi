"""
Script to create or reset admin user
"""
from database import SessionLocal
import models
from auth import get_password_hash, verify_password

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        
        if admin:
            print("Admin user already exists. Do you want to reset the password? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                # Update password
                admin.hashed_password = get_password_hash("admin123")
                db.commit()
                print("✓ Admin password reset to 'admin123'")
            else:
                print("Admin user unchanged")
        else:
            # Create new admin
            print("Creating new admin user...")
            new_password = "admin123"
            hashed = get_password_hash(new_password)
            
            # Verify the hash works
            if verify_password(new_password, hashed):
                print("✓ Password hash verified successfully")
            else:
                print("✗ Warning: Password hash verification failed!")
            
            admin_user = models.User(
                username="admin",
                email="admin@society.com",
                hashed_password=hashed,
                full_name="System Administrator",
                phone_number="1234567890",
                role=models.UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print("\n" + "="*50)
            print("✓ Admin user created successfully!")
            print("="*50)
            print("\nLogin Credentials:")
            print(f"  Username: {admin_user.username}")
            print(f"  Password: admin123")
            print(f"  Email: {admin_user.email}")
            print(f"  Role: {admin_user.role}")
            print("\n⚠️  Please change the password after first login!")
            print("="*50 + "\n")
            
        # Verify we can query the admin
        verify_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if verify_admin:
            print(f"\n✓ Verification: Admin user exists in database")
            print(f"  ID: {verify_admin.id}")
            print(f"  Username: {verify_admin.username}")
            print(f"  Email: {verify_admin.email}")
            print(f"  Active: {verify_admin.is_active}")
            print(f"  Role: {verify_admin.role}")
            
            # Test password verification
            if verify_password("admin123", verify_admin.hashed_password):
                print(f"\n✓ Password verification test: PASSED")
            else:
                print(f"\n✗ Password verification test: FAILED")
        else:
            print("\n✗ Verification failed: Admin user not found!")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("="*50)
    print("Admin User Creation/Reset Script")
    print("="*50 + "\n")
    create_admin()