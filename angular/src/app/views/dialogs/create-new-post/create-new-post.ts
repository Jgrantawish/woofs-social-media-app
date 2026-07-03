import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

import { PostService } from '../../../services/post.service';


@Component({
  selector: 'app-create-new-post',
  standalone: true,
  imports: [CommonModule,
    FormsModule,

    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatDatepickerModule,
    MatNativeDateModule],
  templateUrl: './create-new-post.html',
  styleUrl: './create-new-post.css',
})
export class CreateNewPost {
  public content: string = "";
  public selectedFile: File | null = null;
  public imagePreview: string | null = null;
  public imageError: string = "";
  public maxCharacters = 280;
  private maxSizeMB = 5;
  private maxSizeBytes = this.maxSizeMB * 1024 * 1024;


  constructor(
    private dialogRef: MatDialogRef<CreateNewPost>,
    private postService: PostService
  ) {}

  ngOnDestroy() {
    if (this.imagePreview) {
      URL.revokeObjectURL(this.imagePreview);
    }
  }

  public onImageSelected(event: Event): void {
    // Clear error message from any previous attempts
    this.imageError = "";

    const input = event.target as HTMLInputElement;
    
    // Check that a file was actually uploaded
    if (!input.files || input.files.length === 0) {
      return;
    }

    // Get the first selected file
    const file = input.files[0];

    // Check the file type to ensure that only an image file was uploaded 
    if (!file.type.startsWith('image/')) {
      this.imageError = "Please select a valid image file";
      return;
    }

    // Check that the file is of a reasonable size
    if (file.size > this.maxSizeBytes) {
      this.imageError = "Image file is too large";
      return;
    }

    this.selectedFile = file;
    this.imagePreview = URL.createObjectURL(file);
  }

  public isOverCharacterLimit() {
    return (this.content?.length || 0) > this.maxCharacters;
  }

  public cancel(){
    this.dialogRef.close();
  }

  public post(){
    this.postService.createPost(this.selectedFile, this.content
    )
    .subscribe({
      next: (res) => {
        console.log('Post created:', res);
        },
      error: (err) => {
        console.error(err);
      }
    });

   this.dialogRef.close(); 

  }
}
