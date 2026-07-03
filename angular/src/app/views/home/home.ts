import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, SessionData } from '../../services/auth.service';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { CreateNewPost } from '../dialogs/create-new-post/create-new-post';
import { PostService } from '../../services/post.service';

@Component({
  selector: 'app-home',
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  public sessionData$!: Observable<SessionData | null>;
  public posts$!: Observable<any>;
  private apiUrl = environment.apiUrl;
  public profilePicApiUrl = this.apiUrl + "/users/profile-picture/";
  
  constructor(private authService: AuthService,
    private postService: PostService,
    private dialog: MatDialog,
    private router: Router,
  ) { }

  ngOnInit() {
    this.sessionData$ = this.authService.userSessionData$;
    this.posts$ = this.postService.getPosts();
  }

  public createPost() {
    this.dialog.open(CreateNewPost, {
      width: '700px',
    });
  }

}
