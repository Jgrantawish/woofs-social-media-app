import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgClass } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { Subject, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule, NgClass],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  public username: string = "";
  public email: string = "";
  public password: string = "";
  public usernameTaken : boolean = false;
  public emailTaken : boolean = false;
  public emailErrorMessage: string  = "";
  public usernameErrorMessage: string = "";
  public passwordErrors: string[] = [];
  public accountCreated: boolean = false;
  private usernameChange$ = new Subject<string>();
  private emailChange$ = new Subject<string>();


  ngOnInit(){
    // Calls the backend to check that the username is not already in use 
    this.usernameChange$.pipe(
      // Prevent spamming the backend while the user is typing
      debounceTime(300),
      // Avoid duplicate requests for the same value
      distinctUntilChanged(),
      // Cancel previous HTTP requests if a new username is entered and then call the backend 
      switchMap(username =>
        this.authService.checkUsernameAvailable(username)
      )
    )
    .subscribe(result => {
      this.usernameTaken = !result.available;
    });

    // Calls the backend to check that the email address is not already in use 
    this.emailChange$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(username =>
        this.authService.checkEmailAvailable(username)
      )
    )
    .subscribe(result => {
      this.emailTaken = !result.available;
    });


  }
  

  public validateUsername() {
      // Clear error message from previous checks
      this.usernameErrorMessage = "";

      //
      if (this.username.length === 0) {
        this.usernameErrorMessage = "Username is required";
        return;
      }
      
      if (this.username.length < 3 ) {
        this.usernameErrorMessage = "Your username must be 3 or more characters long";
        return;
      }

      if (this.username.length > 20) {
        this.usernameErrorMessage = "Your username must be 20 characters or less";
        return;
      }

      // Check that username doesn't contain spaces 
      if (/\s/.test(this.username)) {
        this.usernameErrorMessage = "Username cannot contain spaces";
        return;
      }

      // Once the username has passed all validation checks, check that the username is not already taken  
      this.usernameChange$.next(this.username);
    }

    public validateEmail() {
      // Clear error message from previous checks
      this.emailErrorMessage = "";

      // Check the user has entered an email
      if (this.email.length === 0) {
        this.emailErrorMessage = "Email address is required";
        return;
      }

      // Check that the email follows the format of something@something.something with no whitespace
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email)) {
        this.emailErrorMessage = "Please enter a valid email";
        return;
      }

      // Once the email has passed all validation checks, check that the email address is not already taken  
      this.emailChange$.next(this.email);
    }

    public validatePassword(){
      // Clear errors from previous checks
      this.passwordErrors = [];

      // Check password is at least 8 characters long
      if (this.password.length < 8) {
          this.passwordErrors.push("Be at least 8 characters long");    
      }

      // Check password contains at least 1 capial letter
      if (!/[A-Z]/.test(this.password)) {
          this.passwordErrors.push("Contain an uppercase letter");
      }

      // Check password contains at least 1 number
      if (!/\d/.test(this.password)) {
          this.passwordErrors.push("Contain a number");
      }
    }

  
  public signUp(){
    this.authService.signUp(this.username, this.email, this.password).subscribe({
      next: () => {
        this.accountCreated = true;
        // Wait 5 seconds before redirecting to the login page
        setTimeout(() => {
          this.router.navigate(['/']);
        }, 5000);
      },
      error: (err) => {
        console.error(err);
      }
    });
  }
}
