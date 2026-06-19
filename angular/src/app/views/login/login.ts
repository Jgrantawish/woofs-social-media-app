import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgClass } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, NgClass, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  constructor(private authService: AuthService) {}

  public username: string = "";
  public password: string = "";
  public invalidCredentials: boolean = false;

  logIn() {
    this.authService.logIn(this.username, this.password).subscribe({
      next: () => {
        console.log("yay");
  
      },
      error: (err) => {
        console.error(err);
      }
    });
  }

}


