from app import create_app, db
from app.models import User, UserRoles, Role

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'UserRoles': UserRoles, 'Role': Role}
