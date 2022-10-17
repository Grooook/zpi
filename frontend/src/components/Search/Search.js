import React from "react";
import { useTranslation } from "react-i18next";
import { getSearchHelp } from "utils/api";
import "locale/i18n";
import "static/css/search.css";

const Search = () => {
  const { t } = useTranslation();

  const searchHelpHandler = async () => {
    const responseData = await getSearchHelp();
    let datalist = document.querySelector('datalist');
    let innerHTML = "";
    responseData.forEach(element => {
      innerHTML += '<option value="' + element + '">';
    });
    datalist.innerHTML = innerHTML;
  }
  searchHelpHandler()

  return (
    <form method="POST">
      <div className="container mb-5">
        <div className="input-group mb-3">
          <input
            type="text"
            className="form-control"
            list="applications"
            placeholder={t("Start typing application name...")}
          />
          <datalist id="applications">
           
          </datalist>
          <div className="input-group-append">
            <button className="btn btn-primary" type="button">
              {t("Search")}
            </button>
          </div>
        </div>
      </div>
    </form>
  );
};

export default Search;
