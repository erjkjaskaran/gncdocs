from datetime import timedelta
import uuid
import os
import flask_login
from flask import Flask, render_template, request, session, url_for, g
from werkzeug.utils import redirect
from gnc.common.database import Database
from gnc.models.User import User
from gnc.models.useradmin import UserAdmin

app = Flask(__name__)
app.secret_key = "gnc1966"
app.config['UPLOAD_FOLDER'] = "/Users/jaskaran/PycharmProjects/gncdocs/gnc/static/files"


@app.route('/login')
def login():
    try:
        if session.get('name') is not None:
            return render_template("dashboard.html", seskey=session)
        else:
            return render_template('login.html')
    except Exception as e:
        return render_template('exception.html', e=e)


@app.route('/')
def root():
    return redirect(url_for('main'))


@app.route('/naac')
def main():
    return render_template("main.html")


@app.route('/extendprofile')
def extendprofile():
    data11 = Database.find("ext11f", {})
    data12 = Database.find("ext12f", {})
    data = Database.find("ext22", {})
    dataset = Database.find("ext22", {})
    data1 = Database.find("ext32", {})
    dataset1 = Database.find("ext32", {})
    dataset2 = Database.find("ext11", {})
    data21 = Database.find("ext21", {})
    data31 = Database.find("ext31", {})
    data23 = Database.find("ext23", {})
    dataset21 = Database.find("ext21", {})
    dataset23 = Database.find("ext23", {})
    dataset31 = Database.find("ext31", {})
    dataset41 = Database.find("ext41", {})
    dataset41p = Database.find("ext41p", {})
    dataset42 = Database.find("ext42", {})
    data42 = Database.find("ext42", {})
    dataset43 = Database.find("ext43", {})
    return render_template("extendprofile.html", seskey=session, dataset=dataset, dataset1=dataset1, data=data,
                           data1=data1, dataset2=dataset2, data11=data11, dataset21=dataset21, data21=data21,
                           data31=data31, dataset31=dataset31, data23=data23, dataset23=dataset23, dataset41=dataset41,
                           dataset41p=dataset41p, data12=data12, dataset42=dataset42, data42=data42,
                           dataset43=dataset43)


@app.route('/auth/register', methods=['post'])
def faculty_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    if User.register(name, email, password):
        return render_template("login.html")
    else:
        return render_template("adminpage.html")


@app.route('/main', methods=['post', 'get'])
def login_validate():
    if session.get('name') is not None:
        print("ABC")
        return render_template("dashboard.html", seskey=session)
    else:
        try:
            email = request.form['email']
            if email is not None:
                password = request.form['pass']
                session['name'] = User.login_validate(email, password)

                if session['name'] is not None:
                    User.login(email)
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(minutes=10)
                    session.modified = True
                    g.user = flask_login.current_user
                    return render_template("dashboard.html", seskey=session)
                else:
                    session['email'] = None
                    session['name'] = None
                    error = 'Invalid Password'
                    return render_template('login.html', error=error)
            else:
                return render_template('login.html')
        except Exception as e:
            session['name'] = None
            return render_template("login.html", e=e)


@app.route('/logout')
def logout():
    User.logout()
    return redirect(url_for('login'))


@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")


@app.route('/auth/adminlogin', methods=['post'])
def admin_validate():
    if session.get('name') is not None:
        return redirect(url_for('admindashboard'))
    else:
        try:
            email = request.form['email']
            password = request.form['pass']
            print(password)
            admin = UserAdmin.login_validate(email, password)
            if admin is not None:
                print("abc")
                UserAdmin.login(admin)
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=10)
                session.modified = True
                g.user = flask_login.current_user
                return redirect(url_for('admindashboard'))
            else:
                session['name'] = None
                session['type'] = None
                error = 'Invalid Password'
                return render_template('/adminlogin', error=error)
        except Exception as e:
            return render_template("exception.html", e=e)


@app.route('/admindashboard')
def admindashboard():
    if session['name'] is None:
        return redirect(url_for('adminlogin'))
    else:
        return render_template("admindashboard.html", seskey=session)


@app.route('/adminpage')
def adminpage():
    return render_template("adminpage.html", seskey=session)


@app.route('/criteria1')
def criteria1():
    if session.get('name') is not None:
        dataset113 = Database.find("cri113", {})
        dataset132 = Database.find("cri132", {})
        dataset133 = Database.find("cri133", {})
        return render_template("criteria1.html", seskey=session, dataset113=dataset113, dataset132=dataset132,
                               dataset133=dataset133)
    else:
        return redirect(url_for('login'))


@app.route('/cri1.1.3', methods=['POST', 'GET'])
def cri113():
    try:
        y = request.form.get('year')
        nt = request.form.get('nameofteacher')
        nb = request.form.get('nameofbody')
        f = request.files["document"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri113', f.filename))
        Database.insert("cri113",
                        {"id": session['name'], "year": y, "nameofteacher": nt, "nameofbody": nb, "file": f.filename})
        return redirect(url_for('criteria1'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/cri1.3.2', methods=['POST', 'GET'])
def cri132():
    try:
        y = request.form.get('year132')
        pc = request.form.get('programcode')
        nc = request.form.get('namecourse')
        cc = request.form.get('coursecode')
        ns = request.form.get('namestudent')
        f = request.files["document"]
        f.filename = y + "_" + cc + "_" + ns + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri132', f.filename))
        Database.insert("cri132",
                        {"id": session['name'], "year": y, "programcode": pc, "nameofcourse": nc, "coursecode": cc,
                         "nameofstudent": ns, "file": f.filename})
        return redirect(url_for('criteria1'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/cri1.3.3', methods=['POST', 'GET'])
def cri133():
    try:
        pn = request.form.get('programname133')
        pc = request.form.get('programcode133')
        f = request.files["liststudent"]
        f.filename = pn + "_" + "_" + pc + "_studentlist.pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri133', f.filename))
        f1 = request.files["document133"]
        f1.filename = pn + "_" + "_" + pc + "_doc.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri133', f1.filename))
        Database.insert("cri133",
                        {"id": session['name'], "nameofprogram": pn, "programcode": pc, "liststudent": f.filename,
                         "file": f1.filename})
        return redirect(url_for('criteria1'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/criteria2')
def criteria2():
    if session.get('name') is not None:
        dataset211 = Database.find('cri211', {})
        dataset212a = Database.find('cri212a', {})
        dataset212b = Database.find('cri212b', {})
        data212b = Database.find('cri212b', {})
        dataset222 = Database.find('cri222', {})
        dataset233 = Database.find('cri233', {})
        dataset233b = Database.find('cri233b', {})
        dataset241 = Database.find('cri241', {})
        dataset242 = Database.find('cri242', {})
        dataset243 = Database.find('cri243', {})
        dataset263 = Database.find('cri263', {})
        return render_template("criteria2.html", seskey=session, dataset211=dataset211, dataset212a=dataset212a,
                               dataset212b=dataset212b, data212b=data212b, dataset222=dataset222, dataset233=dataset233,
                               dataset233b=dataset233b, dataset241=dataset241, dataset242=dataset242, dataset243=dataset243, dataset263=dataset263)
    else:
        return redirect(url_for('login'))


@app.route('/cri2.1.1', methods=['POST', 'GET'])
def cri211():
    try:
        y = request.form.get('year211')
        pn = request.form.get('programname')
        pc = request.form.get('programcode')
        ss = request.form.get('nosanctionedseat')
        sa = request.form.get('noadmittedstudent')
        f = request.files["documentsanction"]
        f.filename = pn + "_sanctionedseat.pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri211', f.filename))
        f1 = request.files["documentadmitted"]
        f1.filename = pn + "_" + y + "_studentadmitted.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri211', f1.filename))
        Database.insert("cri211",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": y, "programname": pn,
                         "programcode": pc, "seatsanctioned": ss, "studentadmitted": sa, "sanction": f.filename,
                         "admitted": f1.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri211/<string:id>', methods=['POST', 'GET'])
def deletecri211(id=None):
    Database.delete_one("cri211", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.1.2a', methods=['POST', 'GET'])
def cri212a():
    try:
        f1 = request.files["stategovt"]
        f1.filename = "stategovt.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri212a', f1.filename))
        Database.insert("cri212a",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "stategovt": f1.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri212a/<string:id>', methods=['POST', 'GET'])
def deletecri212a(id=None):
    Database.delete_one("cri212a", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.1.2b', methods=['POST', 'GET'])
def cri212b():
    try:
        y = request.form.get('year212b')
        ns = request.form.get('noseats')
        f1 = request.files["admissionlist"]
        f1.filename = "admissionlist_" + y + ".pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri212b', f1.filename))
        f2 = request.files["admissionextract"]
        f2.filename = "admissionextract_" + y + ".pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri212b', f2.filename))
        Database.insert("cri212b",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": y, "noseat": ns,
                         "admissionlist": f1.filename, "admissionextract": f2.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri212b/<string:id>', methods=['POST', 'GET'])
def deletecri212b(id=None):
    Database.delete_one("cri212b", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.2.2', methods=['POST', 'GET'])
def cri222():
    try:
        f1 = request.files["listteacher"]
        f1.filename = "listteacher.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri222', f1.filename))
        Database.insert("cri222",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "listteacher": f1.filename})

        f2 = request.files["liststudent"]
        f2.filename = "liststudent.pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri222', f2.filename))
        Database.insert("cri222",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "liststudent": f2.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri222/<string:id>', methods=['POST', 'GET'])
def deletecri222(id=None):
    Database.delete_one("cri222", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.3.3', methods=['POST', 'GET'])
def cri233():
    try:
        f1 = request.files["mentormentee"]
        f1.filename = "mentormentee.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri233', f1.filename))
        Database.insert("cri233",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "mentormentee": f1.filename})

        f2 = request.files["listmentor"]
        f2.filename = "listmentor.pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri233', f2.filename))
        Database.insert("cri233",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "listmentor": f2.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri233/<string:id>', methods=['POST', 'GET'])
def deletecri233(id=None):
    Database.delete_one("cri233", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.3.3b', methods=['POST', 'GET'])
def cri233b():
    try:
        mn = request.form.get('mentor')
        f2 = request.files["issue"]
        f2.filename = mn + "_issue.pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri233b', f2.filename))
        Database.insert("cri233b",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "mentor": mn, "issue": f2.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri233b/<string:id>', methods=['POST', 'GET'])
def deletecri233b(id=None):
    Database.delete_one("cri233b", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.4.1', methods=['POST', 'GET'])
def cri241():
    try:
        f1 = request.files["sanctionpost"]
        f1.filename = "sanctionedpost.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri241', f1.filename))
        Database.insert("cri241",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "sanctionpost": f1.filename})

        f2 = request.files["listfulltime"]
        f2.filename = "listfulltime.pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri241', f2.filename))
        Database.insert("cri241",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "listfulltime": f2.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri241/<string:id>', methods=['POST', 'GET'])
def deletecri241(id=None):
    Database.delete_one("cri241", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.4.2', methods=['POST', 'GET'])
def cri242():
    try:
        s = request.form.get('session')
        fn = request.form.get('facultyname')
        q = request.form.get('qualification')
        ya = request.form.get('yearaward')
        f1 = request.files["document242"]
        f1.filename = fn + "_" + q + ".pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri242', f1.filename))
        Database.insert("cri242",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "session": s, "facultyname": fn, "qualification": q, "yearaward": ya,
                         "document": f1.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri242/<string:id>', methods=['POST', 'GET'])
def deletecri242(id=None):
    Database.delete_one("cri242", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.4.3', methods=['POST', 'GET'])
def cri243():
    try:
        fn = request.form.get('facultyname243')
        da = request.form.get('dateofappointment')
        e = request.form.get('experience')
        f1 = request.files["document243"]
        f1.filename = fn + "_experience.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri243', f1.filename))
        Database.insert("cri243",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "facultyname": fn, "dateofappointment": da, "experience": e,
                         "document": f1.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri243/<string:id>', methods=['POST', 'GET'])
def deletecri243(id=None):
    Database.delete_one("cri243", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/cri2.6.3', methods=['POST', 'GET'])
def cri263():
    try:
        y = request.form.get('year263')
        pn = request.form.get('programname263')
        f1 = request.files["result"]
        f1.filename = "result" + y + ".pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri263', f1.filename))
        Database.insert("cri263",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": y, "programname": pn,
                         "result": f1.filename})
        return redirect(url_for('criteria2'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri263/<string:id>', methods=['POST', 'GET'])
def deletecri263(id=None):
    Database.delete_one("cri263", {'_id': id})
    return redirect(url_for('criteria2'))


@app.route('/criteria3')
def criteria3():
    if session.get('name') is not None:
        return render_template("criteria3.html", seskey=session)
    else:
        return redirect(url_for('login'))


@app.route('/criteria4')
def criteria4():
    if session.get('name') is not None:
        dataset413 = Database.find('ext41p', {})
        dataset414 = Database.find('cri414', {})
        dataset422 = Database.find('cri422', {})
        dataset423 = Database.find('cri423', {})
        dataset424 = Database.find('cri424', {})
        dataset432 = Database.find('cri432', {})
        return render_template("criteria4.html", seskey=session, dataset413=dataset413, dataset414=dataset414, dataset422=dataset422, dataset423=dataset423, dataset424=dataset424, dataset432=dataset432)
    else:
        return redirect(url_for('login'))


@app.route('/cri4.1.3', methods=['POST', 'GET'])
def cri413():
    try:
        nc = request.form.get('classno')
        f = request.files["doc413"]
        f.filename = nc + ".jpeg"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext41', f.filename))
        Database.insert("ext41p", {"id": session['name'], "classno": nc, "pic": f.filename})
        return redirect(url_for('criteria4'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri413/<string:id>')
def deletecri413(id=None):
    Database.delete_one("ext41p", {'classno': id})
    return redirect(url_for('criteria4'))


@app.route('/cri4.1.4', methods=['POST', 'GET'])
def cri414():
    try:
        nc = request.form.get('year414')
        f = request.files["doc414"]
        f.filename = nc + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri414', f.filename))
        Database.insert("cri414", {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": nc, "document": f.filename})
        return redirect(url_for('criteria4'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri414/<string:id>')
def deletecri414(id=None):
    Database.delete_one("cri414", {'_id': id})
    return redirect(url_for('criteria4'))


@app.route('/cri4.2.2', methods=['POST', 'GET'])
def cri422():
    try:
        nc = request.form.get('year422')
        f = request.files["doc422"]
        f.filename = nc + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri422', f.filename))
        Database.insert("cri422", {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": nc, "document": f.filename})
        return redirect(url_for('criteria4'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri422/<string:id>')
def deletecri422(id=None):
    Database.delete_one("cri422", {'_id': id})
    return redirect(url_for('criteria4'))


@app.route('/cri4.2.4', methods=['POST', 'GET'])
def cri424():
    try:
        f1 = request.files["ledger"]
        f1.filename = "ledger.pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri424', f1.filename))
        Database.insert("cri424",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "ledger": f1.filename})

        f2 = request.files["screenshot"]
        f2.filename = "screenshot.pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri424', f2.filename))
        Database.insert("cri424",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "screenshot": f2.filename})
        return redirect(url_for('criteria4'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri424/<string:id>', methods=['POST', 'GET'])
def deletecri424(id=None):
    Database.delete_one("cri424", {'_id': id})
    return redirect(url_for('criteria4'))


@app.route('/cri4.3.2', methods=['POST', 'GET'])
def cri432():
    try:
        y = request.form.get('year432')
        ns = request.form.get('noseats')
        f1 = request.files["admissionlist"]
        f1.filename = "admissionlist_" + y + ".pdf"
        f1.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri432', f1.filename))
        f2 = request.files["admissionextract"]
        f2.filename = "admissionextract_" + y + ".pdf"
        f2.save(os.path.join(app.config["UPLOAD_FOLDER"], 'cri432', f2.filename))
        Database.insert("cri432",
                        {"_id": "" + uuid.uuid4().hex, "id": session['name'], "year": y, "noseat": ns,
                         "admissionlist": f1.filename, "admissionextract": f2.filename})
        return redirect(url_for('criteria4'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delcri432/<string:id>', methods=['POST', 'GET'])
def deletecri432(id=None):
    Database.delete_one("cri432", {'_id': id})
    return redirect(url_for('criteria4'))


@app.route('/criteria5')
def criteria5():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria5.html", seskey=session)


@app.route('/criteria6')
def criteria6():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria6.html", seskey=session)


@app.route('/criteria7')
def criteria7():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria7.html", seskey=session)


@app.route('/extendedprofile')
def extprof():
    try:
        if session.get('name') is not None:
            data11 = Database.find("ext11f", {})
            data12 = Database.find("ext12f", {})
            data = Database.find("ext22", {})
            dataset = Database.find("ext22", {"id": session['name']})
            data1 = Database.find("ext32", {})
            dataset1 = Database.find("ext32", {"id": session['name']})
            dataset2 = Database.find("ext11", {"id": session['name']})
            data21 = Database.find("ext21", {})
            data31 = Database.find("ext31", {})
            data23 = Database.find("ext23", {})
            dataset21 = Database.find("ext21", {"id": session['name']})
            dataset23 = Database.find("ext23", {"id": session['name']})
            dataset31 = Database.find("ext31", {"id": session['name']})
            dataset41 = Database.find("ext41", {"id": session['name']})
            dataset41p = Database.find("ext41p", {"id": session['name']})
            dataset42 = Database.find("ext42", {"id": session['name']})
            data42 = Database.find("ext42", {})
            dataset43 = Database.find("ext43", {"id": session['name']})
            return render_template("extendedprofile.html", seskey=session, dataset=dataset, dataset1=dataset1,
                                   data=data,
                                   data1=data1, dataset2=dataset2, data11=data11, dataset21=dataset21, data21=data21,
                                   data31=data31, dataset31=dataset31, data23=data23, dataset23=dataset23,
                                   dataset41=dataset41, dataset41p=dataset41p, data12=data12, dataset42=dataset42,
                                   data42=data42, dataset43=dataset43)
        else:
            return redirect(url_for('main'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/adminextendedprofile')
def adminextprof():
    if session['name'] is not None:
        data = Database.find("ext22", {})
        dataset = Database.find("ext22", {})
        data1 = Database.find("ext32", {})
        dataset1 = Database.find("ext32", {})
        dataset2 = Database.find("ext11", {})
        return render_template("adminextendedprofile.html", seskey=session, dataset=dataset, dataset1=dataset1,
                               data=data,
                               data1=data1, dataset2=dataset2)
    else:
        return redirect(url_for('adminlogin'))


@app.route('/ext1.1', methods=['POST', 'GET'])
def ext11():
    pc = request.form.get('programcode')
    pn = request.form.get('programname')
    cc = request.form.get('coursecode')
    cn = request.form.get('coursename')
    y = request.form.get('yearofintroduction')
    Database.insert("ext11", {"pcode": pc, "pname": pn, "ccode": cc, "cname": cn, "yoi": y, "id": session['name']})
    return redirect(url_for('extprof'))


@app.route('/ext1.1f', methods=['POST', 'GET'])
def ext11f():
    print('abc')
    f = request.files['doc11']
    f.filename = "criteria1.1.pdf"
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext11', f.filename))
    Database.insert("ext11f", {"id": session['name'], "file": f.filename})
    return redirect(url_for('extprof'))


@app.route('/ext1.2f', methods=['POST', 'GET'])
def ext12f():
    print('abc')
    f = request.files['doc12']
    f.filename = "criteria1.2.pdf"
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext12', f.filename))
    Database.insert("ext12f", {"id": session['name'], "file": f.filename})
    return redirect(url_for('extprof'))


@app.route('/delext11/<string:id>')
def deleteext11(id=None):
    Database.delete_one("ext11", {'ccode': id})
    return redirect(url_for('extprof'))


@app.route('/delext11f/<string:id>')
def deleteext11f(id=None):
    Database.delete_one("ext11f", {'file': id})
    return redirect(url_for('extprof'))


@app.route('/delext12f/<string:id>')
def deleteext12f(id=None):
    Database.delete_one("ext12f", {'file': id})
    return redirect(url_for('extprof'))


@app.route('/ext2.2', methods=['POST', 'GET'])
def ext22():
    try:

        y = request.form.get('year')
        n = request.form['numberseat']
        f = request.files["document"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext22', f.filename))
        Database.insert("ext22", {"id": session['name'], "year": y, "numberseat": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/ext2.3', methods=['POST', 'GET'])
def ext23():
    try:

        y = request.form.get('year23')
        n = request.form['numberstudent23']
        f = request.files["document23"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext23', f.filename))
        Database.insert("ext23", {"id": session['name'], "year": y, "numberseat": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/ext2.1', methods=['POST', 'GET'])
def ext21():
    try:

        y = request.form.get('year21')
        n = request.form['numberstudent']
        f = request.files["document21"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext21', f.filename))
        Database.insert("ext21", {"id": session['name'], "year": y, "numberstudent": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delext21/<string:id>')
def deleteext21(id=None):
    Database.delete_one("ext21", {'year': id})
    return redirect(url_for('extprof'))


@app.route('/delext22/<string:id>')
def deleteext22(id=None):
    Database.delete_one("ext22", {'year': id})
    return redirect(url_for('extprof'))


@app.route('/delext23/<string:id>')
def deleteext23(id=None):
    Database.delete_one("ext23", {'year': id})
    return redirect(url_for('extprof'))


@app.route('/ext3.1', methods=['POST', 'GET'])
def ext31():
    try:

        y = request.form.get('year')
        n = request.form['numberpost']
        f = request.files["document"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext31', f.filename))
        Database.insert("ext31", {"id": session['name'], "year": y, "numberpost": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/ext3.2', methods=['POST', 'GET'])
def ext32():
    try:

        y = request.form.get('year')
        n = request.form['numberpost']
        f = request.files["document"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext32', f.filename))
        Database.insert("ext32", {"id": session['name'], "year": y, "numberpost": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/ext4.1', methods=['POST', 'GET'])
def ext41():
    try:
        nc = request.form.get('noclass')
        ns = request.form['noseminar']
        f = request.files["doc41"]
        f.filename = "4.1.pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext41', f.filename))
        Database.insert("ext41", {"id": session['name'], "noclass": nc, "noseminar": ns, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/ext4.1p', methods=['POST', 'GET'])
def ext41p():
    try:
        nc = request.form.get('classno')
        f = request.files["doc41p"]
        f.filename = nc + ".jpeg"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext41', f.filename))
        Database.insert("ext41p", {"id": session['name'], "classno": nc, "pic": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delext41/<string:id>')
def deleteext41(id=None):
    Database.delete_one("ext41", {'id': id})
    return redirect(url_for('extprof'))


@app.route('/delext41p/<string:id>')
def deleteext41p(id=None):
    Database.delete_one("ext41p", {'classno': id})
    return redirect(url_for('extprof'))


@app.route('/ext4.2', methods=['POST', 'GET'])
def ext42():
    try:
        y = request.form.get('year42')
        n = request.form['expenditure']
        f = request.files["document42"]
        f.filename = y + ".pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext42', f.filename))
        Database.insert("ext42", {"id": session['name'], "year": y, "expenditure": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delext42/<string:id>')
def deleteext42(id=None):
    Database.delete_one("ext42", {'year': id})
    return redirect(url_for('extprof'))


@app.route('/ext4.3', methods=['POST', 'GET'])
def ext43():
    try:
        n = request.form['nocomputer']
        f = request.files["document43"]
        f.filename = "computer.pdf"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], 'ext43', f.filename))
        Database.insert("ext43", {"id": session['name'], "nocomputer": n, "file": f.filename})
        return redirect(url_for('extprof'))
    except Exception as e:
        return render_template("exception.html", e=e)


@app.route('/delext43/<string:id>')
def deleteext43(id=None):
    Database.delete_one("ext43", {'id': id})
    return redirect(url_for('extprof'))


@app.route('/delext32/<string:id>')
def deleteext32(id=None):
    Database.delete_one("ext32", {'year': id})
    return redirect(url_for('extprof'))


@app.route('/delcri113/<string:yy>,<string:nt>', methods=['POST', 'GET'])
def deletecri113(yy=None, nt=None):
    Database.delete_one("cri113", {'year': yy, 'nameofteacher': nt})
    return redirect(url_for('criteria1'))


@app.route('/delcri132/<string:cc>,<string:ns>', methods=['POST', 'GET'])
def deletecri132(cc=None, ns=None):
    Database.delete_one("cri132", {'coursecode': cc, 'nameofstudent': ns})
    return redirect(url_for('criteria1'))


@app.route('/delcri133/<string:pc>', methods=['POST', 'GET'])
def deletecri133(pc=None):
    Database.delete_one("cri133", {'programcode': pc})
    return redirect(url_for('criteria1'))


@app.route('/criterion1')
def criterion1():
    dataset113 = Database.find("cri113", {})
    dataset132 = Database.find("cri132", {})
    dataset133 = Database.find("cri133", {})
    return render_template("criterion1.html", seskey=session, dataset113=dataset113, dataset132=dataset132,
                           dataset133=dataset133)


@app.route('/criterion2')
def criterion2():
    dataset211 = Database.find('cri211', {})
    dataset212a = Database.find('cri212a', {})
    dataset212b = Database.find('cri212b', {})
    data212b = Database.find('cri212b', {})
    dataset222 = Database.find('cri222', {})
    dataset233 = Database.find('cri233', {})
    dataset233b = Database.find('cri233b', {})
    dataset241 = Database.find('cri241', {})
    dataset242 = Database.find('cri242', {})
    dataset243 = Database.find('cri243', {})
    dataset263 = Database.find('cri263', {})
    return render_template("criterion2.html", dataset211=dataset211, dataset212a=dataset212a,
                           dataset212b=dataset212b, data212b=data212b, dataset222=dataset222, dataset233=dataset233,
                           dataset233b=dataset233b, dataset241=dataset241, dataset242=dataset242, dataset243=dataset243,
                           dataset263=dataset263)


@app.route('/criterion3')
def criterion3():
    return render_template("criterion3.html", seskey=session)


@app.route('/criterion4')
def criterion4():
    return render_template("criterion4.html", seskey=session)


@app.route('/criterion5')
def criterion5():
    return render_template("criterion5.html", seskey=session)


@app.route('/criterion6')
def criterion6():
    return render_template("criterion6.html", seskey=session)


@app.route('/criterion7')
def criterion7():
    return render_template("criterion7.html", seskey=session)


@app.before_first_request
def init_db():
    Database.initialize()
    session['email'] = None
    session['name'] = None


if __name__ == '__main__':
    app.run(port=5555)
