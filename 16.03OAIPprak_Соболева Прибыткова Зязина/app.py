from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

app.secret_key = 'super_secret_key_11111' 

materials = [
    {
        "id": 1,
        "title": "Flask для чайников",
        "category": "Книга",
        "author": "Соболева А.Д.",
        "description": "введение во фласк для чайников."
    },
    {
        "id": 2,
        "title": "Python Web-разработка",
        "category": "Видеокурс",
        "author": "Зязина Е.А.",
        "description": "Поверхностное погружение в веб-разработку."
    },
    {
        "id": 3,
        "title": "Jinja2",
        "category": "Статья",
        "author": "Прибыткова Н.П.",
        "description": "циклы и условия в работе."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materials')
def materials_list():
    return render_template('materials.html', materials=materials)

@app.route('/materials/<int:material_id>')
def material_detail(material_id):
    found_material = None
    
    for item in materials:
        if item["id"] == material_id:
            found_material = item
            break
    
    if found_material:
        return render_template('material_detail.html', material=found_material)
    else:
        return "<h1>Материальчик с таким ID не найден</h1><a href='/materials'>Вернуться к спискочку</a>"

@app.route('/add', methods=['GET', 'POST'])
def add_material():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        author = request.form.get('author')
        description = request.form.get('description')

        new_id = materials[-1]['id'] + 1 if materials else 1
        new_material = {
            "id": new_id,
            "title": title,
            "category": category,
            "author": author,
            "description": description
        }
        
        materials.append(new_material)
        
        return redirect(url_for('materials_list'))

    return render_template('add_material.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == '11111':
            session['logged_in'] = True
            session['user'] = username
            
            return redirect(url_for('add_material'))
        else:
            error = 'неверный логин или пароль'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)