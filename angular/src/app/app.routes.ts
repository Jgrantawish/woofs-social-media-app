import { Routes } from '@angular/router';

import { Login } from './views/login/login';
import { Signup } from './views/signup/signup';

export const routes: Routes = [
  {
    path: '',
    component: Login
  },
  {
    path: 'signup',
    component: Signup
  },
];
