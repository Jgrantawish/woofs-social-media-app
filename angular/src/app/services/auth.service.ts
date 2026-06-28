import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { BehaviorSubject, tap } from 'rxjs';

export interface SessionData {
  user_id: number;
  username: string;
  profile_pic_url: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
    
    constructor(private http: HttpClient) {}

    private apiUrl = environment.apiUrl;
    private userSessionSubject = new BehaviorSubject<SessionData | null>(null);

    public userSessionData$ = this.userSessionSubject.asObservable();

    private setSessionData(sessionData: SessionData) {
      this.userSessionSubject.next(sessionData);
    }

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

    public checkSession(){
      return this.http.get<SessionData>(this.apiUrl + '/auth/check-session');
    }

    public loadSession() {
      return this.checkSession().pipe(
        tap(sessionData => this.setSessionData(sessionData))
      );
    }

    public logOut(){
      return this.http.post(this.apiUrl + '/auth/logout', {});
    }
}


