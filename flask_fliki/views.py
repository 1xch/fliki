from flask import (current_app, redirect, request, render_template,
    Blueprint, url_for)
from .util import config_value, _wiki, flash_next
from .forms import EditorForm, MoveForm, DeleteForm


def index():
    page = _wiki.get('index')
    return render_template(_wiki.display_view, page=page)

def display(url):
    page = _wiki.get(url)
    if page:
        return render_template(_wiki.display_view, page=page)
    return redirect(url_for('.wiki_edit', url=url))

def preview(url):
    page = _wiki.get(url)
    if page:
        return page.html

def edit(url):
    page = _wiki.get(url)
    if page:
        first = False
        forms = {'edit_form': EditorForm(url=url, edit_content=page.raw),
                 'move_form': MoveForm(old=url),
                 'delete_form': DeleteForm(delete=url)}
    else:
        first=True
        forms={'edit_form': EditorForm(url=url)}
    return render_template(_wiki.edit_view, first=first, forms=forms, page=page)

def save():
    r = request.form
    form = EditorForm(url=r['pagekey'], edit_content=r['edit_content'])
    page = form.pagekey.data
    if form.validate_on_submit():
        if _wiki.put(page, form.edit_content.data):
            flash_next('EDIT_PAGE_SUCCESS', page=page)
        else:
            flash_next('EDIT_PAGE_FAIL', page=page)
    return redirect(url_for('.wiki_display', url=page))

def move():
    r = request.form
    form = MoveForm(old=r['oldkey'], new=r['newkey'])
    old = form.oldkey.data
    new = form.newkey.data
    if form.validate_on_submit():
        if _wiki.move(old, new):
            flash_next('MOVE_PAGE_SUCCESS', old_page=old, new_page=new)
            return redirect(url_for('.wiki_display', url=new))
    flash_next('MOVE_PAGE_FAIL', old_page=old)
    return redirect(url_for('.wiki_display', url=old))

def delete():
    r = request.form
    form = DeleteForm(delete=r['delete'])
    page = form.delete.data
    if form.validate_on_submit():
        if _wiki.delete(page):
            url='index'
            flash_next('DELETE_PAGE_SUCCESS', page=page)
        else:
            url = form.delete.data
            flash_next('DELETE_PAGE_FAIL', page=page)
    return redirect(url_for('.wiki_display', url=url))

def create_blueprint(wiki, import_name):
    bp = Blueprint(wiki.blueprint_name,
                   import_name,
                   url_prefix=wiki.url_prefix,
                   subdomain=wiki.subdomain,
                   template_folder='templates')

    bp.route('/',
             endpoint='wiki_index',
             methods=['GET'])(index)

    bp.route('/<path:url>/',
             endpoint='wiki_display',
             methods=['GET'])(display)

    if wiki.editable:
        bp.route('/<path:url>/preview',
                 endpoint='wiki_preview',
                 methods=['GET'])(preview)

        bp.route('/<path:url>/edit',
                 endpoint='wiki_edit',
                 methods=['GET'])(edit)

        bp.route('/move',
                 endpoint='wiki_move',
                 methods=['POST'])(move)

        bp.route('/save',
                 endpoint='wiki_save',
                 methods=['POST'])(save)

        bp.route('/delete',
                 endpoint='wiki_delete',
                 methods=['POST'])(delete)

    return bp
