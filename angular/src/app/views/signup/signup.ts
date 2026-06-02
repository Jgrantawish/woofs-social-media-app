import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-signup',
  imports: [FormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {
  public username: string = '';
  public email: string = '';
  public password: string = '';

  public signUp() {
    console.log(this.email);
    console.log(this.password);
  }
}
