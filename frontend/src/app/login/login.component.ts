import { Component, OnInit } from '@angular/core';
import { TaxiService } from '../services/taxi.service';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Card } from '../models/card';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService) { }

  ngOnInit(): void {
    let logged = localStorage.getItem("csrftoken");
    if (logged != null) this.router.navigate(["home"]);
  }

  phone: string = "";
  licence: string = "";
  email: string = "";
  msg: string = "";
  msg2: string = "";
  msg3: string = "";
  msg4: string = "";

  login() {
    let regexPhone = /^[\+]?[(]?[0-9]{3}[)]?[-\ ]?[0-9]{2}[-\ ]?[0-9]{6,7}$/;
    let regexLicence = /^[0-9]{5}$/;
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

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
    else this.msg2 = "";

    if (this.email.length > 0 && !regexEmail.test(this.email)) {
      this.msg3 = "Invalid email format";
    }
    else this.msg3 = "";

    if (this.msg.length > 0 || this.msg2.length > 0 || this.msg3.length > 0) return;

    this.msg4 = "";

    this.service.login(this.phone, this.licence, this.email).subscribe({
      next: data => {
        if (data == null) return;
        let csrf_token = data.csrftoken;
        localStorage.setItem("csrftoken", JSON.stringify(csrf_token));
        let card = new Card();
        card.balance = data.balance;
        card.discount = data.discount;
        card.number = data.number;
        // card.taxiLicence = data.taxiLicence;
        card.taxiLicence = this.licence // changed to this
        card.points = data.points;
        card.qrcode = data.qrcode;
        localStorage.setItem("card", JSON.stringify(card));

        this.router.navigate(['home']);
      },
      error: error => {
        this.msg4 = error.error
      },
    })
  }
}
