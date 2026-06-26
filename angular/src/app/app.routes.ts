import { Routes } from '@angular/router';
import { authGuard } from './auth-guard';
import { Login } from './views/login/login';
import { Signup } from './views/signup/signup';
import { Home } from './views/home/home';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: Login
  },
  {
    path: 'signup',
    component: Signup
  },
  {
    path: 'home',
    component: Home,
    canActivate: [authGuard]
  }
];
