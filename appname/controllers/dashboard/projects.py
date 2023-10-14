from flask import Blueprint, render_template, flash, abort, redirect, request, url_for, session
from flask_login import login_required, current_user

from appname.extensions import storage
from appname.models import db
from appname.models.user import User
from appname.models.clip import Clip
from appname.models.project import Project
from appname.forms import SimpleForm
from appname.forms.files import FileForm
from appname.helpers.session import current_membership

blueprint = Blueprint('dashboard_projects', __name__)

@blueprint.before_request
def check_for_membership(*args, **kwargs):
    if not current_user.is_authenticated:
        flash('You currently do not have accesss to appname', 'warning')
        return redirect(url_for("main.home"))

@blueprint.route('/projects')
@login_required
def index():
    form = FileForm()
    return render_template('dashboard/projects.html', form=form, projects=current_user.projects, user=current_user)

@blueprint.route('/projects/<hashid:project_id>')
@login_required
def download_clip(project_id):
    clip = Clip.query.filter_by(id=project_id).one()
    if clip:
        file_object = storage.get(clip.file_object_name)
        # Instead of redirecting, you can use the save to URL
        if file_object:
            return redirect(file_object.download_url())
    return abort(404)

@blueprint.route('/projects/<hashid:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).one()
    if project:
        # Delete all the clips associated with the project
        for clip in project.clips:
            file_object = storage.get(clip.file_object_name)
            db.session.delete(clip)
            if file_object:
                file_object.delete()
        # Delete the project itself
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('.index'))
    return abort(404)
