import os

def main():
    """Entry point for the application."""
    print("Starting Streamlit UI...")
    os.system("streamlit run src/ui/app.py")

if __name__ == "__main__":
    main()
