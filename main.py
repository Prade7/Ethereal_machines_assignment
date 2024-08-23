from application import app,db

from application.routes import routes as routes_blueprint
app.register_blueprint(routes_blueprint)


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
