import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, SessionData } from '../../services/auth.service';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { CreateNewPost } from '../dialogs/create-new-post/create-new-post';

@Component({
  selector: 'app-home',
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  public sessionData$!: Observable<SessionData | null>;
  private apiUrl = environment.apiUrl;
  public profilePicApiUrl = this.apiUrl + "/uploads/profile-picture/";
  
  constructor(private authService: AuthService,
    private dialog: MatDialog,
    private router: Router,
  ) { }

  ngOnInit() {
    this.sessionData$ = this.authService.userSessionData$;
  }

  createPost() {
    this.dialog.open(CreateNewPost, {
      width: '700px',
    });
  }

}
