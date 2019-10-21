




#yeni kullanici olusturma
@mod_auth.route('/signup', methods=['POST'])        
def add_user():
    data = request.json
    email = data['email']
    password = data['password']
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(email, hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


#kayitli kullanicinin giris bilgilerini kontrol etme
@mod_auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = Users.query.filter_by(email=email).first()
    if not user:
        return make_response('User not found', 401)
    if check_password_hash(user.password, password):
        token = jwt.encode({'userid': user.user_id}, app.config['SECRET_KEY'])
        user.user_token = token
        db.session.commit()
        out = jsonify(success=True,token=token.decode('utf-8'))
        return out
    return make_response('Password is incorrect', 401)
