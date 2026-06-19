import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
    
    constructor(private http: HttpClient) {}

    private apiUrl = environment.apiUrl;

    public signUp(username: string, email: string, password: string){
      return this.http.post(this.apiUrl + '/auth/signup', {
        username: username,
        email: email,
        password :password
      });
    }

    public checkUsernameAvailable(username: string) {
      return this.http.get<{available: boolean}>(this.apiUrl + '/auth/users/check-username', {
        params: {
          username
        }
      });
    }

    public checkEmailAvailable(email: string) {
      return this.http.get<{available: boolean}>(this.apiUrl + '/auth/users/check-email', {
        params: {
          email
        }
      });
    }

    public logIn(username: string, password: string){
      return this.http.post(this.apiUrl + '/auth/login', {
        username: username,
        password :password
      });
    }



}


