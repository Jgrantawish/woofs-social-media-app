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
    is_owner: boolean;
    like_count: number;
    has_liked: boolean;
    comment_count: number;
}

export interface CommentData {
    id: number;
    content: string;
    created_date: Date;
    last_updated: Date | null;
    owner_username: string;
    owner_profile_pic_url: string | null;
    is_owner: boolean;
}

@Injectable({
    providedIn: 'root'
})
export class PostService {

    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    public getPosts(): Observable<PostData[]> {
        return this.http.get<PostData[]>(this.apiUrl + '/posts/');
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

    public updatePost(postId: number, removeOriginalImage: boolean, image?: File | null, content?: string): Observable<any> {

        // Use FormData to send image file 
        const formData = new FormData();

        // convert to strings so that it can be sent as part of the FormData
        formData.append("post_id", postId.toString());
        formData.append("remove_original_image", removeOriginalImage.toString());

        if (image) {
            formData.append('image', image);
        }

        // If no content, then don't add it to the formData
        if (content?.trim()) {
            formData.append('content', content);
        }

        return this.http.put(this.apiUrl + '/posts/edit', formData);
    }

    public deletePost(postId: number){
        return this.http.delete(this.apiUrl + '/posts/delete', {body:postId});
    }

    public addLike(postId: number) {
        return this.http.post(this.apiUrl + '/posts/add-like', {post_id: postId});
    }

    public removeLike(postId: number) {
        return this.http.delete(this.apiUrl + '/posts/remove-like', {body:postId});
    }

    public getComments(postId: number): Observable<CommentData[]>{
        return this.http.get<CommentData[]>(this.apiUrl + '/comments/'+ postId);
    }

    public addComment(postId: number, content: string) {
        return this.http.post(this.apiUrl + '/comments/new', {
            post_id: postId,
            content: content
        });
    }
}