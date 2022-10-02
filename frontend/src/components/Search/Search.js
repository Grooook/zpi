import React from "react";
import { useTranslation } from "react-i18next";
import "locale/i18n";
import "static/css/search.css";

const Search = () => {
    const { t } = useTranslation();

  return (
    <form method="POST" >
      <div className="container mb-5">
       <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder={t("Start typing application name...")}/>
        <div class="input-group-append">
            <button class="btn btn-primary" type="button">{t("Search")}</button>
        </div>
        </div>
      </div>
    </form>
  );
};

export default Search;
