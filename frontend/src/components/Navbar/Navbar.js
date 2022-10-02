import React from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import "locale/i18n";
import login from "utils/auth";
import pl from "static/img/pl_flag.svg";
import en from "static/img/en_flag.svg";
import "static/css/flag.css";
import { authlogoutUser, isUserAuthenticated } from "utils/auth";

const Navbar = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem("language", lang);
  };

  const languageButton = () => {
    if (i18n.language === "pl") {
      return <img src={pl} onClick={() => changeLanguage("en")} alt="en" />;
    } else {
      return <img src={en} onClick={() => changeLanguage("pl")} alt="pl" />;
    }
  };

  const logout = () => {
    authlogoutUser();
  };

  return (
    <nav className="navbar navbar-light bg-light">
      <div className="d-flex justify-content-between mx-5 w-100">
        <div>
          <a className="navbar-brand" href="/">
            SZW
          </a>
        </div>
        <div className="d-flex">
          {(() => {
            if (isUserAuthenticated()) {
              return (
                <div className="d-flex">
                  <a className="nav-link active" aria-current="page" href="#">
                    {t("All applications")}
                  </a>
                  <a className="nav-link active" aria-current="page" href="#">
                    {t("My applications")}
                  </a>
                  <a
                    href="#"
                    onClick={logout}
                    className="nav-link active"
                    aria-current="page"
                  >
                    {t("Logout")}
                  </a>
                </div>
              );
            } else {
              return (
                <div>
                  <a
                    className="nav-link active"
                    aria-current="page"
                    href="/login"
                  >
                    {t("Login")}
                  </a>
                </div>
              );
            }
          })()}
          <div className="flag" alt="contacts">
            {languageButton()}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
