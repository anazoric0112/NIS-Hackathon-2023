import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RecommendComponent } from './recommend/recommend.component';
import { HomeComponent } from './home/home.component';
import { LogoutComponent } from './logout/logout.component';
import { LoginReferralComponent } from './login-referral/login-referral.component'; import { PumpComponent } from './pump/pump.component';
import { InfoComponent } from './info/info.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'login', component: LoginComponent },
  { path: 'login/:ref_code', component: LoginReferralComponent },
  { path: 'recommend', component: RecommendComponent },
  { path: 'home', component: HomeComponent },
  { path: 'logout', component: LogoutComponent },
  { path: 'pump', component: PumpComponent },
  { path: 'info', component: InfoComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
