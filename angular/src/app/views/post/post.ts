import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PostService, PostData, CommentData } from '../../services/post.service';
import { environment } from '../../../environments/environment';
import { ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-post',
  imports: [CommonModule, FormsModule],
  templateUrl: './post.html',
  styleUrl: './post.css',
})
export class Post {

  constructor(
    private postService: PostService,
    private cdr: ChangeDetectorRef
  ) {}

  @Input({ required: true }) post!: PostData;

  // UI state (local to each post instance)
  public showComments: boolean = false;
  public comments: CommentData[] = [];
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
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error(err);
      }
      });
    }
  }

  public toggleShowComments() {
    this.showComments = !this.showComments;

    if (this.showComments && !this.commentsLoaded) {
      this.loadComments();
    }
  }


  private loadComments() {
    this.postService.getComments(this.post.id).subscribe({
      next: (comments) => {
        this.comments = comments;
        this.commentsLoaded = true;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.log(err);
      }
    });
  }
}
