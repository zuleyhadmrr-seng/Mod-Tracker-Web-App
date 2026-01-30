from website import create_app

app = create_app()

if __name__ == '__main__':
    # starts the web server in debug mode
    app.run(debug=True)