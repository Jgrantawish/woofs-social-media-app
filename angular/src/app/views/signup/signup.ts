import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgClass } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule, NgClass],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {
  constructor(private authService:AuthService) {}

  public username: string = "";
  public email: string = "";
  public password: string = "";
  public usernameTaken : boolean = false;
  public emailTaken : boolean = false;
  public emailErrorMessage: string  = "";
  public usernameErrorMessage: string = "";
  public passwordErrors: string[] = [];
  
  

public validateUsername() {
    // Clear error message from previous checks
    this.usernameErrorMessage = "";

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
  }

  public validateEmail() {
    // Clear error message from previous checks
    this.emailErrorMessage = "";

    // check the user has entered an email
    if (this.email.length === 0) {
      this.emailErrorMessage = "Email address is required";
      return;
    }

    // Check that the email follows the format of something@something.something with no whitespace
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email)) {
      this.emailErrorMessage = "Please enter a valid email";
      return;
    }

    if (this.emailTaken) {
      this.emailErrorMessage = "This email address is already in use. Please enter a different email.";
      return;
    }
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
        console.log('User created');
      }
    });
  }
}
