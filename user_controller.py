
from course_center_db import User, Permission # استيراد الجداول من Peewee
from peewee import DoesNotExist
import bcrypt

class UserManager:
    def __init__(self):
        self.logged_user = None  # المستخدم الحالي بعد تسجيل الدخول

    def verify_password(self, user, password):
        try:
            return bcrypt.checkpw(password.encode(), user.password.encode())
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    
    def login(self, username, password):
        try:
            user = User.get(User.username == username)
            if self.verify_password(user, password):  # استخدام الدالة المخصصة للتحقق
                self.logged_user = user
                return True, user
            else:
                return False, "كلمة المرور غير صحيحة"
        except User.DoesNotExist:
            return False, "المستخدم غير موجود"
        except Exception as e:
            return False, f"حدث خطأ: {str(e)}"   
    
    def get_logged_user_id(self):
        if self.logged_user:
            return self.logged_user.id
        return None

    
    def get_permissions(self):
        if not self.logged_user:
            return []
        return list(Permission.select().where(Permission.user_id == self.logged_user))

    
    @staticmethod
    def create_user(fullname, username, password, job, phone, is_admin=False):
        try:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.create(
                fullname=fullname,
                username=username,
                password=hashed_password,
                job=job,
                phone=phone,
                is_admin=is_admin
            )
            return True, "تم حفظ بيانات المستخدم بنجاح"        
        except Exception as e:
            return False, "خطأ تكرار بيانات"

    @staticmethod
    def get_all_users():
        return list(User.select())
    
    def update_user(self, user_id, fullname, job, username, password, phone, is_admin):
        try:
            user = User.get_by_id(user_id)
            if password:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user.password = hashed_password
            user.fullname = fullname
            user.job = job
            user.username = username
            user.phone = phone
            user.is_admin = is_admin    
            user.save()
            return True, "تم تحديث بيانات المستخدم بنجاح"
        except User.DoesNotExist:
            return False, "المستخدم غير موجود"
        except Exception as e:
            return False, f"حدث خطأ أثناء التحديث: {str(e)}"

    def delete_user(self, user_id):
        try:
            user = User.get_by_id(user_id)
            user.delete_instance()
            return True, "تم حذف المستخدم بنجاح"
        except User.DoesNotExist:
            return False, "المستخدم غير موجود"
        except Exception as e:
            return False, "لا يمكن حذف المستخدم لارتباطه بسجلات أخرى"
        
