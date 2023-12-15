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
    // let regexPhone = /^\+\d{3} ?\d{8,9}$/;
    let regexPhone = /^[\+]?[(]?[0-9]{3}[)]?[-\ ]?[0-9]{2}[-\ ]?[0-9]{6,7}$/;
    let regexLicence = /^[0-9]{5}$/
    if (this.phone.length == 0) {
      this.msg = "Field phone missing";
    }
    else if (!regexPhone.test(this.phone)) {
      this.msg = "Invalid phone format";
    }
    else this.msg = "";
    if (this.licence.length == 0) {
      this.msg2 = "Field licence missing";
    }
    else if (!regexLicence.test(this.licence)) {
      this.msg2 = "Invalid licence format";
    }
    else this.msg2 = ""
    if (this.msg.length > 0 || this.msg2.length > 0) return;

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

        this.router.navigate(['home']);
      }
    )
  }
}
