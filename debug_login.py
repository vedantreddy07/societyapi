"""
Debug login issues
"""
from database import SessionLocal
import models
from auth import verify_password, get_password_hash

def debug_login():
    db = SessionLocal()
    
    print("\n" + "="*60)
    print("LOGIN DEBUG SCRIPT")
    print("="*60 + "\n")
    
    # Check all users
    print("1. Checking all users in database...")
    users = db.query(models.User).all()
    print(f"   Total users found: {len(users)}\n")
    
    for user in users:
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Active: {user.is_active}")
        print(f"   Hash: {user.hashed_password[:50]}...")
        print()
    
    # Try to find admin
    print("2. Looking for 'admin' user...")
    admin = db.query(models.User).filter(models.User.username == "admin").first()
    
    if not admin:
        print("   ✗ Admin user NOT FOUND!")
        print("   Run: python create_admin.py")
        db.close()
        return
    
    print(f"   ✓ Admin user found!")
    print(f"   ID: {admin.id}")
    print(f"   Active: {admin.is_active}")
    
    # Test password verification
    print("\n3. Testing password verification...")
    test_passwords = ["admin123", "admin", "password", ""]
    
    for pwd in test_passwords:
        result = verify_password(pwd, admin.hashed_password)
        status = "✓ MATCH" if result else "✗ No match"
        print(f"   Password '{pwd}': {status}")
    
    # Generate new hash and compare
    print("\n4. Testing hash generation...")
    new_hash = get_password_hash("admin123")
    print(f"   New hash generated: {new_hash[:50]}...")
    print(f"   Verification of new hash: {verify_password('admin123', new_hash)}")
    
    # Check if bcrypt is working
    print("\n5. Checking bcrypt library...")
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        test_hash = pwd_context.hash("test123")
        test_verify = pwd_context.verify("test123", test_hash)
        print(f"   Bcrypt test: {'✓ Working' if test_verify else '✗ Failed'}")
    except Exception as e:
        print(f"   ✗ Bcrypt error: {e}")
    
    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60 + "\n")
    
    db.close()

if __name__ == "__main__":
    debug_login()