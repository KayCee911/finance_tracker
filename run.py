from app import create_app

# Create Flask app using the factory pattern
app = create_app()

# Start development server
if __name__ == "__main__":
    app.run(debug=True)
