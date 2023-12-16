import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RecommendComponent } from './recommend/recommend.component';
import { HomeComponent } from './home/home.component';
import { RedirectingComponent } from './redirecting/redirecting.component';
import { LogoutComponent } from './logout/logout.component';
import { LoginReferralComponent } from './login-referral/login-referral.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'login/:ref_code', component: LoginReferralComponent },
  { path: 'recommend', component: RecommendComponent },
  { path: 'home', component: HomeComponent },
  { path: '', component: RedirectingComponent },
  { path: 'logout', component: LogoutComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
