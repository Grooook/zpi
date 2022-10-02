import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { authLoginUser } from "utils/auth";
import swal from 'sweetalert';
import "locale/i18n";
import "static/css/login.css";
import { API_URL } from "constants/index";


const Login = () => {
  const { t } = useTranslation();
  const [index, setIndex] = useState();
  const [password, setPassword] = useState();

  async function loginUser(credentials) {
    return fetch('http://localhost:8000/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
   }
  
  const handleSubmit = async e => {
    e.preventDefault();
    const response = await loginUser({
      index,
      password
    });
    if ('accessToken' in response) {
      swal(t(response.message), {
        icon: "success",
        buttons: false,
        timer: 2000,
      })
      .then((value) => {
        authLoginUser(response['accessToken'], response['user']);
        window.location.href = "/";
      });
    } else {
      swal(t(response.message), {
        icon:"error"
      });
    }
  }

  return (
    <form method="POST" onSubmit={handleSubmit}>
      <div className="container">
        <div className="row d-flex justify-content-center">
            <div className="card px-5 py-5">
              <div className="form-data">
                <div className="forms-inputs mb-4">
                  <span>{t("Student ID")}</span>
                  <input name="index" className="w-100" type="text" onChange={e => setIndex(e.target.value)}/>
                </div>
                <div className="forms-inputs mb-4">
                  <span>{t("Password")}</span>
                  <input
                    name="password"
                    className="w-100"
                    autoComplete="off"
                    type="password"
                    onChange={e => setPassword(e.target.value)}
                  />
                </div>
                <div className="mb-3">
                  <button className="btn btn-success w-100">
                    {t("Login")}
                  </button>
                </div>
              </div>
          </div>
        </div>
      </div>
    </form>
  );
};

export default Login;
