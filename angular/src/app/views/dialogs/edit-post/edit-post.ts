import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

import { PostService } from '../../../services/post.service';
import { environment } from '../../../../environments/environment';


@Component({
  selector: 'app-edit-post',
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
  templateUrl: './edit-post.html',
  styleUrl: './edit-post.css',
})
export class EditPost {
  public postImageApiUrl =  environment.apiUrl + "/posts/images/";
  public content: string = "";
  public selectedFile: File | null = null;
  public imagePreview: string | null = null;
  public imageError: string = "";
  public maxCharacters = 280;
  private maxSizeMB = 5;
  private maxSizeBytes = this.maxSizeMB * 1024 * 1024;
  private postId!: number;
  private originalImage: string | null = null;
  private removeOriginalImage = false;


  constructor(
    private dialogRef: MatDialogRef<EditPost>,
    private postService: PostService,
    @Inject(MAT_DIALOG_DATA) public data: { id: number, image: string, content: string}
  ) {
    this.postId = data.id;
    this.originalImage = data.image;
    this.content = data.content;

    // If the post orginally contained an image, load it into the preview
    if (this.originalImage) {
      this.imagePreview = this.postImageApiUrl + this.originalImage;
    }
  }

  ngOnDestroy() {
    // If the current preview is a temporary blob URL release it to avoid leaking browser memory
    // (Don't revoke normal server URLs)
    if (this.imagePreview?.startsWith("blob:")){
      URL.revokeObjectURL(this.imagePreview);
    }
  }

  public removeImage(){

    this.selectedFile = null;
    this.imagePreview = null;

    if (this.originalImage) {
        this.removeOriginalImage = true;
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

    // If there is a previous URL blob preview, remove it
    if (this.imagePreview?.startsWith("blob:")) {
      URL.revokeObjectURL(this.imagePreview);
    }

    this.selectedFile = file;
    this.imagePreview = URL.createObjectURL(file);
  }

  public isOverCharacterLimit() {
    return (this.content?.length || 0) > this.maxCharacters;
  }

  public cancel(){
    this.dialogRef.close(false);
  }

  public update(){

    this.postService.updatePost(this.postId, this.removeOriginalImage, this.selectedFile, this.content)
    .subscribe({
    next: () => this.dialogRef.close(true),
    error: (err) => {
        console.error(err);
      }
    });
  }
}
