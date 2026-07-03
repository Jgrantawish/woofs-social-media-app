import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PostService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  public createPost(image?: File | null, content?: string): Observable<any> {

    // Use FormData to send image file 
    const formData = new FormData();

    if (image) {
      formData.append('image', image);
    }

    // If no content, then don't add it to the formData
    if (content?.trim()) {
        formData.append('content', content);
    }

    return this.http.post(this.apiUrl + '/posts/new', formData);
  }
}