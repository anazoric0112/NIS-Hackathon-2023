import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RecommendComponent } from './recommend/recommend.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { HomeComponent } from './home/home.component';
import { LogoutComponent } from './logout/logout.component';
import { CommonModule } from '@angular/common';
import { LoginReferralComponent } from './login-referral/login-referral.component';
import { PumpComponent } from './pump/pump.component';
import { InfoComponent } from './info/info.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RecommendComponent,
    HomeComponent,
    LogoutComponent,
    LoginReferralComponent,
    PumpComponent,
    InfoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    CommonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
