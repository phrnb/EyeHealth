import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import AuthPage from './AuthPage';
import ChartPage from './ChartPage';
import EditProfile from './EditProfile';
import ImgAnalysis from './ImgAnalysis';
import PatientPage from './PatientPage';
import PatientProfile from './PatientProfile';
import RegisterPatient from './RegisterPatient';
import UploadPage from './UploadPage';
import UserProfile from './UserProfile';
import UserRegister from './UserRegister';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/auth" component={AuthPage} />
        <Route path="/chart" component={ChartPage} />
        <Route path="/edit-profile" component={EditProfile} />
        <Route path="/img-analysis" component={ImgAnalysis} />
        <Route path="/patient" component={PatientPage} />
        <Route path="/patient-profile" component={PatientProfile} />
        <Route path="/register-patient" component={RegisterPatient} />
        <Route path="/upload" component={UploadPage} />
        <Route path="/user-profile" component={UserProfile} />
        <Route path="/user-register" component={UserRegister} />
        
        {/* Главная страница или редирект, если маршрут не найден */}
        <Route exact path="/" render={() => <h1>Добро пожаловать на главную страницу!</h1>} />
      </Switch>
    </Router>
  );
};

export default App;
