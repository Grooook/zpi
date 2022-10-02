import React from "react";
import { Route, BrowserRouter, Routes } from 'react-router-dom';
import { isUserAuthenticated } from "utils/auth";
import Navbar from "components/Navbar/Navbar";
import Login from "components/Login/Login";
import Search from "components/Search/Search";
import MainLayoutRoutes from "./MainRoutes";

function App () {
  const isAuthenticated = isUserAuthenticated();
    return (
      <div className="app">
        <BrowserRouter exact path="/">
          <Routes>
            <Route exact path="/login" element={<Login />} />
            <Route path="*" element={<MainLayoutRoutes />} />
          </Routes>
        </BrowserRouter>
        </div>
    );
};


export default App;