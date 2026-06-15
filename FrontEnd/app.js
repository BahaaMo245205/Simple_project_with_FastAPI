const BACKEND_URL = "http://127.0.0.1:8000/v1"; 

// دالة التنقل بين شاشتي الـ Login والـ Signup
function toggleForms() {
    document.getElementById("login-form").classList.toggle("hidden");
    document.getElementById("signup-form").classList.toggle("hidden");
    hideMessages();
}

function showMessage(type, text) {
    hideMessages();
    const box = type === "error" ? document.getElementById("error-box") : document.getElementById("success-box");
    box.innerText = text;
    box.style.display = "block";
}

function hideMessages() {
    document.getElementById("error-box").style.display = "none";
    document.getElementById("success-box").style.display = "none";
}

// ==================== 1. دالة الـ Signup ====================
async function handleSignup() {
    hideMessages();
    
    const username = document.getElementById("signup-username").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value;
    const confirm_password = document.getElementById("signup-confirm-password").value;

    // التحقق المبدئي في الـ Frontend
    if(!username || !email || !password || !confirm_password) {
        showMessage("error", "رجاءً املأ جميع الحقول!");
        return;
    }

    // تجهيز الـ Payload بنفس أسماء المتغيرات في الـ Pydantic Model (UserRegisterSchema)
    const payload = {
        username: username,
        email: email,
        password: password,
        confirm_password: confirm_password
    };

    try {
        const response = await fetch(`${BACKEND_URL}/AddUser`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("success", "تم إنشاء الحساب بنجاح! يمكنك الدخول الآن.");
            // تحويل المستخدم لشاشة اللوجن بعد ثانيتين
            setTimeout(() => toggleForms(), 2000);
        } else {
            // لو الـ Backend رجع خطأ (زي الإيميل متكرر أو الباسورد مش متطابق)
            showMessage("error", data.detail || "حدث خطأ ما أثناء التسجيل.");
        }
    } catch (error) {
        showMessage("error", "مشكلة في الاتصال بالسيرفر، تأكد من تشغيل الـ Backend.");
    }
}

// ==================== 2. دالة الـ Login ====================
async function handleLogin() {
    hideMessages();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    if(!email || !password) {
        showMessage("error", "رجاءً أدخل البريد الإلكتروني وكلمة المرور!");
        return;
    }

    // تجهيز الـ Payload على مقاس الـ UserLoginSchema في البايثون
    const payload = {
        email: email,
        password: password
    };

    try {
        const response = await fetch(`${BACKEND_URL}/login`, {
            method: "POST", // تأكد إن الـ Route في البايثون بقى @app.post
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("success", data.Message); 
            // الخطوة الجاية لما تفعل الـ JWT الحقيقي:
            localStorage.setItem("access_token", data.access_token);
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            },1000);
            
        } else {
            showMessage("error", data.detail || "بيانات الدخول غير صحيحة.");
        }
    } catch (error) {
        showMessage("error", "مشكلة في الاتصال بالسيرفر، تأكد من تشغيل الـ Backend.");
    }
}