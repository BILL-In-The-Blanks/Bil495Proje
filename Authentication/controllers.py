





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
