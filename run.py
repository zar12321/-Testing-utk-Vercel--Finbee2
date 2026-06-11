from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <!DOCTYPE html>
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
                padding:30px;
                border-radius:20px;
                background:#1e293b;
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
                background:linear-gradient(
                    90deg,
                    #f59e0b,
                    #fbbf24
                );
                font-weight:bold;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <h1>🐝 FinBee</h1>

            <input
                placeholder="Email atau Username"
            >

            <input
                type="password"
                placeholder="Password"
            >

            <button>
                Masuk
            </button>

        </div>

    </body>
    </html>
    """