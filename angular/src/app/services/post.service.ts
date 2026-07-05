import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

export interface PostData {
    id: number;
    picture_url: string | null;
    content: string | null;
    created_date: Date;
    last_updated: Date | null;
    owner_username: string;
    owner_profile_pic_url: string | null;
    like_count: number
    has_liked: boolean
    comment_count: number
}

@Injectable({
  providedIn: 'root'
})
export class PostService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  public getPosts(): Observable<any>{
    return this.http.get(this.apiUrl + '/posts/');
  }

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

  public addComment(postId: number, content: string){
    return this.http.post(this.apiUrl + '/posts/add-comment', {
      post_id: postId,
      content: content
    });
  }
}