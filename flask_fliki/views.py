from flask import current_app, redirect, request, render_template, jsonify, \
    after_this_request, Blueprint

from werkzeug.local import LocalProxy
#from .decorators import conditionally
from .util import config_value

# Convenient references
_wiki = LocalProxy(lambda: current_app.extensions['fliki'])

#@conditionally(config_value(_wiki.secure)) decorator to conditionally apply a decorator
def index():
    page = _wiki.get('index')
    return render_template(_wiki.display_view, page=page)

def display(url):
    page = _wiki.get(url)
    return render_template(_wiki.display_view, page=page)

def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for('edit', url=form.clean_url(form.url.data)))
    return render_template(_wiki.create_view, form=form)

#def preview():
#    a = request.form
#    data = {}
#    processed = _wiki.default_processor(a['body'])
#    data['html'], data['body'], data['meta'] = processed.out()
#    return data['html']

#def move(url):
#    page = _wiki.get_or_404(url)
#    form = URLForm(obj=page)
#    if form.validate_on_submit():
#        newurl = form.url.data
#        wiki.move(url, newurl)
#        return redirect(url_for('.display', url=newurl))
#    return render_template(_wiki.move_view, form=form, page=page)

#def delete(url):
#    page = _wiki.get_or_404(url)
#    _wiki.delete(url)
#    flash("Page {} was deleted.".format(page.title), 'success')
#    return redirect(url_for('index'))

#def edit(url):
#    page = _wiki.get(url)
#    form = EditorForm(obj=page)
#    if form.validate_on_submit():
#        if not page:
#            page = _wiki.get_bare(url)
#        form.populate_obj(page)
#        page.save()
#        flash("{} was saved.".format(page.title), 'success')
#        return redirect(url_for('display', url=url))
#    return render_template(_wiki.edit_view, form=form, page=page)

#@app.route('/tags/')
#@protect
#def tags():
#    tags = wiki.get_tags()
#    return render_template('tags.html', tags=tags)

#@app.route('/tag/<string:name>/')
#@protect
#def tag(name):
#    tagged = wiki.index_by_tag(name)
#    return render_template('tag.html', pages=tagged, tag=name)

#@app.route('/search/', methods=['GET', 'POST'])
#@protect
#def search():
#    form = SearchForm()
#    if form.validate_on_submit():
#        results = wiki.search(form.term.data)
#        return render_template('search.html', form=form,
#                               results=results, search=form.term.data)
#    return render_template('search.html', form=form, search=None)

def create_blueprint(wiki, import_name):
    bp = Blueprint(wiki.blueprint_name,
                   import_name,
                   url_prefix=wiki.url_prefix,
                   subdomain=wiki.subdomain,
                   template_folder='templates')

    bp.route(wiki.index_url,
             endpoint='wiki_index',
             methods=['GET'])(index)

    bp.route(wiki.index_url+'/<path:url>/',
             endpoint='wiki_display',
             methods=['GET'])(display)

    if wiki.editable:
        bp.route(wiki.index_url+'/create/',
                 endpoint='wiki_create',
                 methods=['GET', 'POST'])(create)

        #bp.route(wiki.index_url+'/preview/',
        #         endpoint='wiki_preview',
        #         methods=['POST'])(preview)

        #bp.route(wiki.index_url+'/<path:url>/move',
        #         endpoint='wiki_move',
        #         methods=['GET', 'POST'])(move)

        #bp.route(wiki.index_url+'/<path:url>/edit',
        #         endpoint='wiki_edit',
        #         methods=['GET', 'POST'])(edit)

        #bp.route(wiki.index_url+'/<path:url>/delete',
        #         endpoint='wiki_delete',
        #         methods=['GET'])(delete)

    return bp
