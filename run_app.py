"""
Startup script for the Crypto Trading Simulator
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'websocket-client',
        'requests',
        'pandas',
        'numpy',
        'plotly',
        'python-dotenv',
        'ccxt'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Crypto Trading Simulator...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        print("Make sure you're in the correct directory.")
        sys.exit(1)
    
    print("🌐 Launching Streamlit app...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
