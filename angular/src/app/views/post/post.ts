import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PostService, PostData } from '../../services/post.service';
import { environment } from '../../../environments/environment';


@Component({
  selector: 'app-post',
  imports: [CommonModule, FormsModule],
  templateUrl: './post.html',
  styleUrl: './post.css',
})
export class Post {

  constructor(private postService: PostService) {}

  @Input({ required: true }) post!: PostData;

  // UI state (local to each post instance)
  public showComments: boolean = false;
  public comments: any[] = [];
  public commentsLoaded: boolean = false;
  public newCommentContent: string = "";


  private apiUrl = environment.apiUrl;
  public profilePicApiUrl = this.apiUrl + "/users/profile-pictures/";
  public postImageApiUrl = this.apiUrl + "/posts/images/";


  public postComment() {
    if (this.newCommentContent?.trim()){
      this.postService.addComment(this.post.id, this.newCommentContent).subscribe({
      next: () => {
        // Clear comment input box ready for another comment
        this.newCommentContent = "";      
      },
      error: (err) => {
        console.error(err);
      }
      });
    }
  }

}
