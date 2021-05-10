from flask import Flask, request, render_template, flash, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, extract
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
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicate records, please try again in a minute.', category='error')
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
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicate records, please try again in a minute.', category='error')
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
                    flash('It hasn\'t been a minute yet for ' + staff.name + '. To avoid duplicate records, please try again in a minute.', category='error')
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

@views.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        idno = request.form.get('idno')
        check = Staff.query.filter_by(staff_id_no=idno).first()
        if check:
            return redirect(url_for('views.generate_report', staff_id=idno))
        else:
            flash('No personnel found with that id #. Try again! This time, type it correctly!', category='error')
            return render_template('generate.html', user=current_user)

    return render_template('generate.html', user=current_user)

@views.route('/generate/<string:staff_id>')
def generate_report(staff_id):
    staff = Staff.query.filter_by(staff_id_no=staff_id).first()
    dt = date.today()
    year_now = dt.year

    record = DailyTimeRecord.query.filter(
        DailyTimeRecord.staff_id == staff.id,
        extract('year', DailyTimeRecord.time_in_am) == year_now
    ).all()

    months = DailyTimeRecord.query.filter(
        DailyTimeRecord.staff_id == staff.id,
        extract('year', DailyTimeRecord.time_in_am) == year_now
    ).group_by(
        extract('month', DailyTimeRecord.time_in_am)
    ).distinct()
    
    return render_template('generate_user_log.html', user=current_user, staff=staff, record=record, months=months)

@views.route('/generate/<string:staff_id>/viewdtr/<int:year>/<int:month>')
def monthly_record(staff_id, year, month):
    staff_id = staff_id
    year = year
    month = month
    return render_template('monthly_record.html', user=current_user, staff_id=staff_id, year=year, month=month)

@views.route('/admin')
@login_required
def admin():
    staff = Staff.query.all()
    return render_template('administration.html', user=current_user, staff=staff)

@views.route('/about')
def about():
    return render_template('masthead.html', user=current_user)

@views.route('/debug')
def debug():
    staff = Staff.query.all()
    return render_template('debug.html', staff=staff, user=current_user)