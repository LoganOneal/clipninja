from flask import Blueprint, render_template, flash, abort, redirect, request, url_for, session
from flask_login import login_required, current_user

from appname.extensions import storage
from appname.models import db
from appname.models.clip import Clip
from appname.models.project import Project
from appname.forms import SimpleForm
from appname.forms.files import FileForm
from appname.helpers.session import current_membership

blueprint = Blueprint('dashboard_upload', __name__)

@blueprint.before_request
def check_for_membership(*args, **kwargs):
    # Ensure that anyone that attempts to pull up the dashboard is currently belongs to any team on our site
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to appname', 'warning')
        return redirect(url_for("main.home"))

@blueprint.route('/upload')
@login_required
def index():
    form = FileForm()
    return render_template('dashboard/upload.html', form=form)

@blueprint.route('/upload/add_clip', methods=['POST'])
@login_required
def upload_clip():
    form = FileForm()

    if form.validate_on_submit():
        extensions = ['mp4', 'mov', 'avi']
        attachment = storage.upload(form.attachment.data, extensions=extensions)

        project = Project(title=form.title.data,
                          description=form.description.data,
                          user=current_user)
        clip = Clip(file_name=attachment.info['name'],
                    file_object_name=attachment.name, project=project)

        db.session.add(project)
        db.session.add(clip)
        db.session.commit()

        flash("Succesfully Uploaded {}".format(clip.file_name, attachment.url), 'warning')
        return redirect(url_for('.index'))
