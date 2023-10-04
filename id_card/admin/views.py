from . import admin
from .forms import EditStudent
from ..models import User
from .. import db
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    flash
)
from flask_login import (
    login_required,
    current_user
)



@admin.route('/dash')
@login_required
def index():
    students = User.query.filter_by(role='STUDENT')
    # set of all departments
    deps = {user.department for user in students}
    counts = {}
    for dep in deps:
        counts.setdefault(dep, User.query.filter_by(department=dep).count())
    return render_template('admin/dash.html', deps=deps, counts=counts)


@admin.route('/admin/students')
@login_required
def students():
    students = User.query.filter_by(role='STUDENT')
    deps = {user.department for user in students}
    return render_template('admin/students.html', students=students, deps=deps)


@admin.route('/admin/students/<dep>')
@login_required
def filtered_students(dep):
    all = User.query.filter_by(role='STUDENT')
    deps = {user.department for user in all}
    students = User.query.filter_by(department=dep).order_by(User.user_id)
    return render_template('admin/students_by_dep.html', students=students, deps=deps)


@admin.route('/admin/refresh')
@login_required
def refresh():
    """Refreshes the students page to update ID card ready statuses and other fields I choose to refresh.
    
    Return: Redirect to the students view.
    """
    users = User.query.filter_by(role='STUDENT')
    for user in users:
        response = user.check_id_status()
        if response.get('status') is True:
            user.id_ready = True
    db.session.commit()
    return redirect(url_for('.students'))


@admin.route('/admin/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    user = User.query.get(id)
    form = EditStudent(obj=user)
    if form.is_submitted():
        # try:
        # personal info update
        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.user_id = form.user_id.data
        user.email = form.email.data
        user.number = form.number.data
        user.dob = form.dob.data
        user.state_of_origin = form.state_of_origin.data
        user.address = form.address.data
        # user active or rusticated
        user.is_active = form.is_active.data
        user.rusticated = form.rusticated.data
        db.session.commit()
        flash('Changes applied', 'success')
        return redirect(url_for('.students'))
        # except:
        #     flash('Error. Check inputs and try again.', 'warning')
        #     return redirect(url_for('.edit_student', id=id))
    return render_template('admin/edit_student.html', form=form, user=user)
