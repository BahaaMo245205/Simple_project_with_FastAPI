n
# 🛡️ Simple Project with FastAPI, JWT & Frontend

مشروع متكامل ومأمن لإنشاء حسابات المستخدمين وتسجيل الدخول باستخدام **FastAPI** كـ Backend، ونظام الـ **JWT (JSON Web Token)** لحماية المسارات، مع واجهة مستخدم **Frontend (HTML/JS Vanilla)** متوافقة بالكامل، ومقفل للتشغيل السريع باستخدام **Docker Compose**.

---

## 🚀 مميزات المشروع (Features)

* **Backend قوي:** مبني باستخدام FastAPI و Python 3.14 مع تفقد تلقائي للبيانات (Pydantic Validation).
* **أمان احترافي:** تشفير كلمات المرور بـ SHA-256 وحماية الـ Endpoints باستخدام كروت الـ JWT (`Depends` & `HTTPBearer`).
* **واجهة مستخدم نظيفة:** صفحة دخول وإنشاء حساب (Auth) ولوحة تحكم محمية (Dashboard) ترسل التوكن في الـ Headers.
* **قاعدة بيانات منظمة:** ربط وتخزين البيانات باستخدام SQLAlchemy ORM.
* **حاويات مجهزة:** تشغيل فوري للجبهتين بـ أمر واحد عبر Docker Compose وسيرفر Nginx خفيف.

---

## 📂 هيكل المشروع (Project Structure)

```text
Simple_project_with_FastAPI/
├── Backend/
│   ├── Backend_App/
│   │   └── model.py          # جداول قاعدة البيانات (SQLAlchemy Models)
│   ├── Test/
│   │   └── test_is_password_valid.py  # اختبارات الأمان (Pytest)
│   ├── config.py             # إعدادات قاعدة البيانات والبيئة
│   ├── run.py                # نقطة انطلاق السيرفر والـ Endpoints
│   └── Dockerfile            # بناء حاوية الباكيند
├── FrontEnd/
│   ├── auth.html             # صفحة الـ Login / Signup
│   └── dashboard.html        # لوحة التحكم المحمية بالـ JWT
├── docker-compose.yml        # مدير تشغيل الحاويات (Orchestration)
└── requirements.txt          # مكتبات البايثون المطلوبة
```

🛠️ طريقة التشغيل المحلية (Local Setup)
1. تشغيل الـ Backend
تأكد من تثبيت المكتبات وتفعيل البيئة الافتراضية (Virtual Environment)، ثم تشغيل السيرفر من المجلد الرئيسي:

```Bash
python -m uvicorn Backend.run:app --reload --port 8000
```
رابط توثيق الـ API الفوري (Swagger UI): `http://127.0.0.1:8000/docs`

2. تشغيل الـ Testing (Pytest)
لتشغيل اختبارات التحقق من قوة كلمات المرور والتأكد من جودة الكود:

```Bash
python -m pytest
```

3. تشغيل الـ Frontend
يمكنك استخدام إضافة Live Server في VS Code وتشغيل ملف FrontEnd/auth.html ليفتح معك على بورت 5500.

🐋 التشغيل السحابي والفوري باستخدام Docker
المشروع مهيأ ليقوم بالكامل (الباكيند والفرونتيند) بكلمة واحدة ودون الحاجة لتسطيب بايثون على جهازك:

Bash
# بناء وتشغيل الحاويات في شبكة واحدة
docker-compose up --build
رابط الواجهة (Frontend): `http://127.0.0.1:5500/auth.html`

رابط السيرفر (Backend): `http://127.0.0.1:8000`
🔒 حماية البيانات والـ HTTP Headers
Request Headers: الـ Frontend يقوم بحفظ الـ access_token في الـ LocalStorage وإرساله في هيدر الطلب تلقائياً:

HTTP
Authorization: Bearer <your_jwt_token>
CORS Middleware: مدمج في الباكيند لضمان سماح المتصفح بتبادل البيانات والـ Tokens بين البورتات المختلفة بأمان.