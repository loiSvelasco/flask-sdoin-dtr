from flask import Flask, request, render_template, flash, Blueprint, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from .models import Staff, DailyTimeRecord
from . import db
from datetime import datetime, date

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_no = request.form.get('idno')
        staff = Staff.query.filter_by(staff_id_no=id_no).first()

        dt = datetime.now()
        today_dt = date.today()

        dtr_log = DailyTimeRecord.query.filter(
            func.date(DailyTimeRecord.time_in_am)==today_dt, 
            DailyTimeRecord.staff_id==staff.id
        ).first()

        if dtr_log:
            if dtr_log.time_out_am == None:
                a, b = dtr_log.time_in_am, dt
                c = b-a
                mins = c.seconds / 60
                if mins < 1:
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicated records, please try again in a minute.', category='error')
                    return render_template('index.html', user=current_user)
                else:
                    dtr_log.time_out_am = dt
                    db.session.commit()
                    flash('Timed out @ ' + dt.strftime('%I:%M %p') + ' in the morning.', category='success')
                    return render_template('index.html', user=current_user)
            elif dtr_log.time_in_pm == None:
                a, b = dtr_log.time_out_am, dt
                c = b-a
                mins = c.seconds / 60
                if mins < 1:
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicated records, please try again in a minute.', category='error')
                    return render_template('index.html', user=current_user)
                else:
                    dtr_log.time_in_pm = dt
                    db.session.commit()
                    flash('Timed in @ ' + dt.strftime('%I:%M %p') + ' in the afternoon.', category='success')
                    return render_template('index.html', user=current_user)
            elif dtr_log.time_out_pm == None:
                a, b = dtr_log.time_in_pm, dt
                c = b-a
                mins = c.seconds / 60
                if mins < 1:
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicated records, please try again in a minute.', category='error')
                    return render_template('index.html', user=current_user)
                else:
                    dtr_log.time_out_pm = dt
                    db.session.commit()
                    flash('Timed out @ ' + dt.strftime('%I:%M %p') + ' in the afternoon.', category='success')
                    return render_template('index.html', user=current_user)
            else:
                flash('Your in and out for the morning and afternoon already exists! Please do not spam this application.', category='error')
                return render_template('index.html', user=current_user)
        else:
            new_dtr_log = DailyTimeRecord(time_in_am=dt, time_out_am=None, time_in_pm=None, time_out_pm=None, staff_id=staff.id)
            db.session.add(new_dtr_log)
            db.session.commit()
            flash('Timed in @ ' + dt.strftime('%I:%M %p') + ' in the morning.', category='success')
            return render_template('index.html', user=current_user)
    return render_template('index.html', user=current_user)

@views.route('/logs')
def logs():
    today_dt = date.today()
    allStaff = Staff.query.all()
    allDtr = DailyTimeRecord.query.filter(func.date(DailyTimeRecord.time_in_am)==today_dt).all()
    return render_template('logs.html', user=current_user, allDtr=allDtr, allStaff=allStaff)

@views.route('/generate')
def generate():
    return render_template('generate.html', user=current_user)

@views.route('/admin')
@login_required
def admin():
    return render_template('administration.html', user=current_user)

@views.route('/about')
def about():
    return render_template('masthead.html', user=current_user)

@views.route('/debug')
def debug():
    staff = Staff.query.all()
    return render_template('debug.html', staff=staff, user=current_user)