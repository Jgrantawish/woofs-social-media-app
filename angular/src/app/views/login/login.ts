import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgClass } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, NgClass, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  public username: string = "";
  public password: string = "";
  public invalidCredentials: boolean = false;

  constructor(private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) { }

  logIn() {
    this.authService.logIn(this.username, this.password).subscribe({
      next: () => {
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.invalidCredentials = true;
        // Force UI update immediately (and display error message)
        this.cdr.detectChanges();
      }
    });
  }

}


