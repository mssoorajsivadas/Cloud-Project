from datetime import datetime,timezone, timedelta

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User

from app.validators.password import is_valid_password
from app.validators.username import is_valid_username

from app.utils.session import create_session, get_current_session,check_session_security, SECURITY_CHECK_INTERVAL, SESSION_IDLE_DAYS



auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

'''
#============================#

    Register Page

#============================#
'''
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username", "").strip()
    first_name = data.get("first_name", "").strip()
    second_name = data.get("second_name", "").strip()
    password = data.get("password", "")

    if not username or not first_name or not second_name or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    if not is_valid_password(password):
        return jsonify({
            "message": "Password must be at least 8 characters"
        }), 400

    if not is_valid_username(username):
        return jsonify({
            "message": "Username must be 3-30 characters and contain only letters, numbers, and underscores"
        }), 400

    existing_username = User.query.filter_by(username=username).first()

    if existing_username:
        return jsonify({
            "message": "Username already taken. Please choose another username"
        }), 409

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        first_name=first_name,
        second_name=second_name,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully."
    }), 201


'''
#============================#

   Login Page

#============================#
'''
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        return jsonify({
            "message": "username and password are required"
        }), 400

    user = User.query.filter_by(username=login.lower()).first()

    if not user:
        return jsonify({
            "message": "Invalid username or password"
        }), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "message": "Invalid username or password"
        }), 401

    session_token = create_session(user)

    response = jsonify({
        "message": "Login successful"
    })

    response.set_cookie(
        "session_token",
        session_token,
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return response, 200

'''
#============================#

   User Info Page

#============================#
'''
@auth_bp.route("/me", methods=["GET"])
def me():

    current_session = get_current_session()

    if not current_session:
        return jsonify({
            "message": "Not logged in"
        })
    
        response.delete_cookie("session_token")

        return response, 401

    user = db.session.get(User, current_session.user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        })
    
        response.delete_cookie("session_token")

        return response, 401

    now = datetime.now(
        timezone.utc
    ).replace(tzinfo=None)

    seconds_since_security_check = (
        now - current_session.last_security_check_at
    ).total_seconds()

    if (
        seconds_since_security_check
        >= SECURITY_CHECK_INTERVAL
    ):

        security_check = check_session_security(
            current_session
        )

        print(
            "SECURITY CHECK:",
            security_check
        )

        current_session.last_security_check_at = now

        if security_check["reauth_required"]:

            db.session.commit()

            return jsonify({
                "message": "Re-authentication required",
                "reauth_required": True
            }), 401

            response.delete_cookie("session_token") 
            return response, 401
        db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200

'''
#============================#

   Logout Page

#============================#
'''
@auth_bp.route("/logout", methods=["POST"])
def logout():

    current_session = get_current_session()

    if current_session:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        current_session.revoked = True
        current_session.revoked_at = now

        db.session.commit()

    response = jsonify({
        "message": "Logged out successfully"
    })

    response.delete_cookie("session_token")

    return response, 200

'''
#============================#

    Acitivity Chick
    
#============================#
'''
@auth_bp.route("/activity", methods=["POST"])
def activity():

    current_session = get_current_session()

    if not current_session:
        return jsonify({
            "message": "Not logged in"
        }), 401

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    current_session.last_seen_at = now

    current_session.idle_expires_at = (
        now + timedelta(days=SESSION_IDLE_DAYS)
    )

    db.session.commit()

    return jsonify({
        "message": "Activity updated"
    }), 200
