#!/usr/bin/env python3
"""
Startup validation script for Chronicle AI deployment.
Run this to check for configuration issues before deploying.
"""

import os
import sys
from pathlib import Path

# Load .env file first
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"📄 Loaded environment from {env_path}\n")
    else:
        print(f"⚠️  .env file not found at {env_path}\n")
except ImportError:
    print("⚠️  python-dotenv not installed, trying to continue anyway...\n")

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required. Current version:", sys.version)
        return False
    print("✓ Python version OK:", sys.version.split()[0])
    return True


def check_required_packages():
    """Check if all required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "supabase",
        "openai",
    ]
    
    print("\nChecking required packages:")
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} NOT FOUND")
            all_good = False
    
    return all_good


def check_environment_variables():
    """Check for required environment variables"""
    required_vars = {
        "DATABASE_URL": "PostgreSQL/Supabase database connection",
        "SUPABASE_URL": "Supabase project URL",
        "SUPABASE_SERVICE_KEY": "Supabase service role key",
        "OPENROUTER_API_KEY": "OpenRouter API key for LLM",
    }
    
    optional_vars = {
        "CORS_ORIGINS": "CORS allowed origins",
        "OPENROUTER_MODEL": "LLM model selection",
    }
    
    print("\n📋 Environment Variables Check:")
    
    missing_required = []
    for var, desc in required_vars.items():
        if os.getenv(var):
            print(f"  ✓ {var}: configured")
        else:
            print(f"  ❌ {var}: MISSING - {desc}")
            missing_required.append(var)
    
    print("\nOptional variables:")
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        status = "✓ set" if value else "⚠️  not set (will use default)"
        print(f"  {status}: {var}")
    
    if missing_required:
        print(f"\n❌ Missing {len(missing_required)} required variables:")
        for var in missing_required:
            print(f"   - {var}")
        return False
    
    return True


def check_app_imports():
    """Try importing the main app to catch import errors"""
    print("\n🔍 Testing app imports:")
    try:
        from app.main import app
        print("  ✓ app.main imported successfully")
        
        # Check if routers are loaded
        routes = [route.path for route in app.routes]
        print(f"  ✓ App initialized with {len(routes)} routes")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to import app: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation checks"""
    print("=" * 60)
    print("🚀 Chronicle AI Startup Validation")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Environment Variables", check_environment_variables),
        ("App Imports", check_app_imports),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Validation Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All validations passed! Ready for deployment.")
        return 0
    else:
        print(f"\n❌ {total - passed} validation(s) failed. Fix issues before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
