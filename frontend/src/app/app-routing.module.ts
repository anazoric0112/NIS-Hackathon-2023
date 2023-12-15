import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CardComponent } from './card/card.component';
import { LoginComponent } from './login/login.component';
import { RecommendComponent } from './recommend/recommend.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'card', component: CardComponent },
  { path: 'recommend', component: RecommendComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
