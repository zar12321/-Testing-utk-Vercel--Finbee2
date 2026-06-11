from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Form

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def login_page():

    return """
    <html>
    <head>
        <title>FinBee Login</title>

        <style>

        body{
            background:#0f172a;
            color:white;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }

        .card{
            width:400px;
            background:#1e293b;
            padding:30px;
            border-radius:20px;
        }

        input{
            width:100%;
            padding:12px;
            margin-top:10px;
            margin-bottom:20px;
            border:none;
            border-radius:10px;
        }

        button{
            width:100%;
            padding:12px;
            border:none;
            border-radius:10px;
            font-weight:bold;
            background:#fbbf24;
        }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>🐝 FinBee Login</h1>

            <form action="/login" method="post">

                <input
                    name="username"
                    placeholder="Username"
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                >

                <button type="submit">
                    Masuk
                </button>

            </form>

        </div>

    </body>
    </html>
    """

@app.post("/login", response_class=HTMLResponse)
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if (
        username == "admin"
        and
        password == "123456"
    ):
        return """
        <h1>
            Login Berhasil 🎉
        </h1>

        <p>
            Selamat datang Admin
        </p>
        """

    return """
    <h1>
        Login Gagal ❌
    </h1>

    <p>
        Username atau Password salah
    </p>

    <a href="/">
        Kembali ke Login
    </a>
    """