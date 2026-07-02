import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateNewPost } from './create-new-post';

describe('CreateNewPost', () => {
  let component: CreateNewPost;
  let fixture: ComponentFixture<CreateNewPost>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateNewPost],
    }).compileComponents();

    fixture = TestBed.createComponent(CreateNewPost);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
