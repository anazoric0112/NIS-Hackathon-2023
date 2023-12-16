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

  ngOnInit() {
    let card: Card = JSON.parse(localStorage.getItem('card')!)
    let licence_b64 = btoa(card.taxiLicence)
    this.WAhref = "https://api.whatsapp.com/send?text=" + this.baseUrl + "/login/" + licence_b64
    this.Viberhref = 'viber://forward?text=' + this.baseUrl + "/login/" + licence_b64
  }

  phone: string = "";
  email: string = "";
  baseUrl = "http://localhost:4200"
  msg: string = "";
  msg2: string = "";
  WAhref: string = ""
  Viberhref: string = ""
  referralLink: string = "123"
  imgpath: string = "../../assets/icons/";
  pathsms: string = this.imgpath + "sms.png";
  pathmail: string = this.imgpath + "mail.png";
  pathwa: string = this.imgpath + "wa.png";
  pathviber: string = this.imgpath + "viber.png";
  pathhome: string = this.imgpath + "home.png";
  pathshare: string = this.imgpath + "share.png";
  pathqr: string = this.imgpath + "qr.png";
  pathq: string = this.imgpath + "q.png";

  check_phone(): boolean {
    this.msg = ""
    this.msg2 = ""

    let regexPhone = /^[\+]?[(]?[0-9]{3}[)]?[-\ ]?[0-9]{2}[-\ ]?[0-9]{6,7}$/;
    if (this.phone.length == 0) {
      this.msg = "Field phone missing";
    }
    else if (!regexPhone.test(this.phone)) {
      this.msg = "Invalid phone format";
    }
    else this.msg = "";
    return this.msg == "";
  }

  sendSMS() {

    if (!this.check_phone()) return;
    if (this.msg.length != 0) return;

    let card: Card = JSON.parse(localStorage.getItem('card')!)
    let licence_b64 = btoa(card.taxiLicence)

    this.service.sendSMS(`${this.baseUrl}/login/${licence_b64}`).subscribe(
      data => {
        this.msg = data;
      }
    );
  }

  sendWA() {
    this.msg = "";
    this.msg2 = "";
    window.location.href = this.WAhref;
  }

  sendViber() {
    this.msg = "";
    this.msg2 = "";
    window.location.href = this.Viberhref;
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

    this.service.sendEmail(this.email, "NISTaxi Invitation", `${this.baseUrl}/login/${licence_b64}`).subscribe(
      data => {
        this.msg2 = data;
      }
    )
  }
  back() {
    this.router.navigate(["home"]);
  }

  showHome() {
    this.router.navigate(["home"]);
  }

  showQR() {
    localStorage.setItem("showqr", "1");
    this.router.navigate(["home"]);
  }
  showInfo() {
    this.router.navigate(['info'])
  }

}
