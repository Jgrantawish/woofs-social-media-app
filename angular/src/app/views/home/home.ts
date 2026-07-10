import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { AuthService, SessionData } from '../../services/auth.service';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { CreateNewPost } from '../dialogs/create-new-post/create-new-post';
import { PostService } from '../../services/post.service';
import { Post } from '../post/post';
import { Subject, debounceTime, distinctUntilChanged, switchMap, startWith } from 'rxjs';
import { UserService, UserData } from '../../services/user.service';
import { ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-home',
  imports: [
    CommonModule, 
    Post,     
    FormsModule,
    MatInputModule,
    MatAutocompleteModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  public sessionData$!: Observable<SessionData | null>;
  public posts$!: Observable<any>;
  private apiUrl = environment.apiUrl;
  public profilePicApiUrl = this.apiUrl + "/users/profile-pictures/";
  public searchText = '';
  public usernameSearchText$ = new Subject<string>();
  public users: UserData[] = [];
  public selectedUser?: UserData;

  
  constructor(private authService: AuthService,
    private postService: PostService,
    private userService: UserService,
    private dialog: MatDialog,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.sessionData$ = this.authService.userSessionData$;
    this.getPosts();

    // Calls the backend to search for users 
    this.usernameSearchText$.pipe(
      // Get all users on initialisation
      startWith(''),
      // Prevent spamming the backend while the user is typing
      debounceTime(500),
      // Avoid duplicate requests for the same value
      distinctUntilChanged(),
      // Cancel previous HTTP requests if a new username is entered and then call the backend 
      switchMap(username => this.userService.search(username))
      )
      .subscribe(users => {
        this.users = users;
        this.cdr.detectChanges();
      }
    );
  }

  public onSearch(searchText: string): void {
    // Ignore the ngModel change caused by selecting a user
    if (this.selectedUser && (searchText === this.selectedUser.username)) {
      return;
    }

    this.usernameSearchText$.next(searchText);

    // If text is removed, clear all userdata and get all posts again 
    if (!searchText.trim()) {
      this.clearUserSearch();
    }
  }

  public onUserSelected(user: UserData): void {
    this.selectedUser = user;

    // Clear the dropdown
    this.users = [];

    // get posts for just that user
    this.getPosts(user.id);
  }

  public clearUserSearch() {
    this.selectedUser = undefined;
    this.searchText = '';
    this.users = [];
    this.getPosts();
  }


  public getPosts(userId?: number){
    this.posts$ = this.postService.getPosts(userId);
  }

  public createPost() {

    const createPostDialogRef = this.dialog.open(CreateNewPost, {
      width: '700px',
    });

    createPostDialogRef.afterClosed().subscribe((result) => {
    // Only re fetch posts if a new post was actually created
      if (result) {
            this.getPosts();
      }
    });
    
  }


  public logOut() {
    this.authService.logOut().subscribe({
      next: () => {
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error(err);
      }
    });

  }

}
