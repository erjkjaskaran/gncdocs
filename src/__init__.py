from datetime import timedelta
import os
import flask_login
from flask import Flask, render_template, request, session, url_for, g
from werkzeug.utils import redirect

from src.common.database import Database
from src.models.User import User
from src.models.useradmin import UserAdmin

app = Flask(__name__)
app.secret_key = "gnc1966"
app.config['UPLOAD_FOLDER'] = "C:\\Users\\erjk\\PycharmProjects\\gncdocs\\src\\static\\files"


@app.route('/login')
def login():
    try:
        if session['name'] is None:
            return render_template('login.html')
        else:
            return render_template("dashboard.html", seskey=session)
    except Exception as e:
        return render_template('exception.html',e)


@app.route('/')
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
        return render_template("dashboard.html", seskey=session)
    else:
        try:
            error = None
            email = request.form['email']
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
        except Exception as e:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    User.logout()
    return redirect(url_for('login'))


@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")


@app.route('/auth/adminlogin', methods=['post'])
def admin_validate():
    if session['name'] is not None:
        return redirect(url_for('admindashboard'))
    else:
        try:
            error = None
            email = request.form['email']
            password = request.form['pass']
            admin = UserAdmin.login_validate(email, password)
            if admin is not None:
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
            return redirect(url_for('adminlogin'))


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
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        dataset113 = Database.find("cri113", {})
        return render_template("criteria1.html", seskey=session, dataset113=dataset113)


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


@app.route('/criteria2')
def criteria2():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria2.html", seskey=session)


@app.route('/criteria3')
def criteria3():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria3.html", seskey=session)


@app.route('/criteria4')
def criteria4():
    if session['name'] is None:
        return redirect(url_for('login'))
    else:
        return render_template("criteria4.html", seskey=session)


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
        if session['name'] is not None:
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
            return render_template("extendedprofile.html", seskey=session, dataset=dataset, dataset1=dataset1, data=data,
                                   data1=data1, dataset2=dataset2, data11=data11, dataset21=dataset21, data21=data21,
                                   data31=data31, dataset31=dataset31, data23=data23, dataset23=dataset23, dataset41=dataset41, dataset41p=dataset41p, data12=data12, dataset42=dataset42, data42=data42, dataset43=dataset43)
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
        f.filename = nc + ".pdf"
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


@app.route('/criterion1')
def criterion1():
    return render_template("criterion1.html", seskey=session)


@app.route('/criterion2')
def criterion2():
    return render_template("criterion2.html", seskey=session)


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
