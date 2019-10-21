#gerekli importlar
#uygulama ile baglanti sonra kurulacak !
from functools import wraps
from flask import request, jsonify
import jwt

class Auth():
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message' : 'Token yok'}), 401
              try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = Users.query.filter_by(user_id=data['userid']).first()
                return f(current_user, *args, **kwargs)
            except jwt.ExpiredSignature:
                return 'Yeniden giris yapiniz'
            except jwt.InvalidTokenError:
                return 'Token tanimlanamadi,yeniden giris yapiniz.'

        return decorated
