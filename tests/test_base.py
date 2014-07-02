def test_base(app):
    assert app.extensions['fliki'] is not None


def test_has_index(client):
    r = client.get('/test/', follow_redirects=True)
    assert b"Title: index\nSummary: base page for wiki" not in r.data
    assert b"Welcome to your flask-wiki" in r.data


def test_new_page(client):
    r = client.get('/test/test_page/', follow_redirects=True)
    assert b"Edit Page Content" in r.data


def test_edit_page(client):
    r = client.post('/test/save',
                    data=dict(pagekey='test_page', edit_content='a test_page'),
                    follow_redirects=True)
    assert b"a test_page" in r.data


def test_display_page(client):
    r = client.get('/test/random_page/', follow_redirects=True)
    assert b"A random page" in r.data


def test_move_page(client):
    r1 = client.post('/test/move',
                     data=dict(oldkey='random_page', newkey='new/random_page'),
                     follow_redirects=True)
    r2 = client.get('/test/new/random_page/', follow_redirects=True)
    r3 = client.get('/test/random_page/', follow_redirects=True)
    assert b"A random page" in r1.data
    assert r1.data == r2.data
    assert b"A random page" not in r3.data


def test_delete_page(client):
    r = client.post('/test/delete',
                    data=dict(delete='random_page'),
                    follow_redirects=True)
    assert b"index" in r.data
