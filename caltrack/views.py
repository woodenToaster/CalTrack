from flask import render_template, flash, redirect
from caltrack import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash_fmt = 'Login requested for OpenID="{}", remember_me={}'
        flash(flash_fmt.format(form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])
