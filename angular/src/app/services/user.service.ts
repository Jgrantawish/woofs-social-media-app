import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface UserData {
    id: number;
    username: string;
    profile_pic_url: string | null;
}

@Injectable({
    providedIn: 'root'
})
export class UserService {
    private apiUrl = environment.apiUrl;


    constructor(private http: HttpClient) { }


    public search(username: string) {
        return this.http.get<UserData[]>(this.apiUrl + '/users/search', {
            params: {
                search_text: username
            }
        });
    }

}