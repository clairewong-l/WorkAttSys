from App import app, api

if __name__ == '__main__':
    print(app.config["SQLALCHEMY_POOL_RECYCLE"])
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 800
    print(app.config["SQLALCHEMY_POOL_RECYCLE"])
    app.run()
