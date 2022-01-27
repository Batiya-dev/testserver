from bottle_sqlite import SQLitePlugin
from bottle import run, route, template, install, static_file, post, request, redirect, TEMPLATES


install(SQLitePlugin(dbfile=r'C:\projects\teleg_b\example.db'))


@route('/')
def main():
    return template("starter.html")


@route('/products')
def main(db):
    data = []
    dict_ = {}
    rows = db.execute(f"SELECT name, number, price, id FROM products").fetchall()

    for row in rows:
        dict_['name'] = row[0]
        dict_['nums'] = row[1]
        dict_['price'] = row[2]
        dict_['id'] = row[3]
        data.append(dict_)
        dict_ = {}

    return template("index.html", products=data)


@route('/static/css/<filename>')
def send_static(filename):
    return static_file(filename, root=r'C:\projects\teleg_b\server\static\css')


@post('/send_data')
def add_to_db(db):
    name = request.forms.name
    nums = request.POST.nums
    price = request.POST.price

    try:
        db.execute("INSERT INTO products (name, number, price) VALUES (?, ?, ?)", (name, int(nums), float(price)))
    except:
        return "<p>Ошибка! Ожидалась числовое значение в количестве и сумме.</p>"
    return redirect('/products')


@post('/delete')
def delete_from_db(db):
    id = request.forms.id
    print(id)
    try:
        db.execute("DELETE FROM products where id=?", (id,))
    except Exception as e:
        print(e)
        return "Что-то пошло не так"
    return redirect('/products')


run(host="192.168.1.102", port="80", debug=True)
