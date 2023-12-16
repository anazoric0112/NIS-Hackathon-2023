import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RecommendComponent } from './recommend/recommend.component';
import { HomeComponent } from './home/home.component';
import { RedirectingComponent } from './redirecting/redirecting.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'recommend', component: RecommendComponent },
  { path: 'home', component: HomeComponent },
  { path: '', component: RedirectingComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
