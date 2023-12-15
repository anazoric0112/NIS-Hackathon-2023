import { Component } from '@angular/core';
import { TaxiService } from '../services/taxi.service';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Card } from '../models/card';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService) { }

  phone: string = "";
  licence: string = "";
  msg: string = "";
  msg2: string = "";

  login() {
    let regexPhone = /^\+\d{3} ?\d{8,9}$/;
    let regexLicence = /^\d{5}$/
    if (!regexPhone.test(this.phone)) {
      this.msg = "Telefon nije u ispravnom formatu.";
    }
    if (!regexLicence.test(this.licence)) {
      this.msg2 = "Licenca nije u ispravnom formatu.";
    }
    if (this.msg.length > 0 || this.msg2.length > 0) return;

    this.msg = "";
    this.msg2 = "";
    this.service.login(this.phone, this.licence).subscribe(
      data => {
        if (data == null) return;
        let csrf_token = data.csrftoken;
        localStorage.setItem("csrftoken", JSON.stringify(csrf_token));
        let card = new Card();
        card.balance = data.balance;
        card.discount = data.discount;
        card.number = data.number;
        card.taxiLicence = data.taxiLicence;
        card.points = data.points;
        card.qrcode = data.qrcode;
        localStorage.setItem("card", JSON.stringify(card));
      }
    )
  }
}
