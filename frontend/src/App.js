import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import Game from "./pages/gamesRoom";
import LoginPage from "./pages/loginPage";
import Register from "./pages/registerPage";
import Home from "./pages/homePage";

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen overflow-hidden">
        <AuthProvider>
          <Switch>
            <Route component={LoginPage} path="/login" />
            <Route component={Register} path="/register" />
            <PrivateRoute component={Home} path="/" exact />
            <PrivateRoute component={Game} path="/game_room" exact />
          </Switch>
        </AuthProvider>
      </div>
    </Router>
  );
}

export default App;