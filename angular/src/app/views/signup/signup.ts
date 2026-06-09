import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  imports: [FormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {
  constructor(private authService:AuthService) {}

  public username: string = '';
  public email: string = '';
  public password: string = '';

  public signUp() {
    this.authService.signUp(this.username, this.email,this.password).subscribe({
      next: () => {
        console.log('User created');
      }
    });
  }
}
