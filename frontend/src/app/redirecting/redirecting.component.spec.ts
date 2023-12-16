import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RedirectingComponent } from './redirecting.component';

describe('RedirectingComponent', () => {
  let component: RedirectingComponent;
  let fixture: ComponentFixture<RedirectingComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RedirectingComponent]
    });
    fixture = TestBed.createComponent(RedirectingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
