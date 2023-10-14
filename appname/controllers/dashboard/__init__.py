from .home import blueprint as home_blueprint
from .team import blueprint as team_blueprint
from .files import blueprint as files_blueprint
from .projects import blueprint as projects_blueprint
from .upload import blueprint as upload_blueprint
dashboard_blueprints = [
    home_blueprint,
    team_blueprint,
    files_blueprint,
    projects_blueprint,
    upload_blueprint,
]
