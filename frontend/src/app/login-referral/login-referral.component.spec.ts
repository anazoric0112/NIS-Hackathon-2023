import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginReferralComponent } from './login-referral.component';

describe('LoginReferralComponent', () => {
  let component: LoginReferralComponent;
  let fixture: ComponentFixture<LoginReferralComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LoginReferralComponent]
    });
    fixture = TestBed.createComponent(LoginReferralComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
