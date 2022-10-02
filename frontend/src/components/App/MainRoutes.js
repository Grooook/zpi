import React from "react";
import { Route, BrowserRouter, Routes } from "react-router-dom";
import Navbar from "components/Navbar/Navbar";
import Search from "components/Search/Search";

function MainLayoutRoutes() {
  return (
    <React.Fragment>
      <Navbar />
      <Routes>
        <Route index element={<Search />} />
      </Routes>
    </React.Fragment>
  );
}

export default MainLayoutRoutes;
