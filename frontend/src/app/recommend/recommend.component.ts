import { Component } from '@angular/core';
import { TaxiService } from '../services/taxi.service';
import { Card } from '../models/card';
import { Router } from '@angular/router';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent {
  constructor(private service: TaxiService, private router: Router) { }

  phone: string = "";
  email: string = "";
  baseUrl = "http://localhost:4200/taxi"
  msg: string = "";
  msg2: string = "";
  // msg3: string = "";
  // msg4: string = "";

  sendSMS() {
    let regexPhone = /^[\+]?[(]?[0-9]{3}[)]?[-\ ]?[0-9]{2}[-\ ]?[0-9]{6,7}$/;
    this.msg = ""
    this.msg2 = ""

    if (this.phone.length == 0) {
      this.msg = "Field phone missing";
    }
    else if (!regexPhone.test(this.phone)) {
      this.msg = "Invalid phone format";
    }
    else this.msg = "";

    if (this.msg.length > 0) return;

    let card: Card = JSON.parse(localStorage.getItem('card')!)
    let licence_b64 = btoa(card.taxiLicence)

    this.service.sendSMS(`${this.baseUrl}/login/${licence_b64}`).subscribe();
  }

  sendEmail() {
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    this.msg = ""
    this.msg2 = ""

    if (this.email.length == 0) {
      this.msg2 = "Field email missing"
    }
    else if (!regexEmail.test(this.email)) {
      this.msg2 = "Invalid email format";
    }
    else this.msg2 = "";

    if (this.msg2.length > 0) return;

    let card: Card = JSON.parse(localStorage.getItem('card')!)
    let licence_b64 = btoa(card.taxiLicence)

    this.service.sendEmail(this.email, "NISTaxi Invitation", `${this.baseUrl}/login/${licence_b64}`).subscribe()
  }
  back() {
    this.router.navigate(["home"]);
  }
}
