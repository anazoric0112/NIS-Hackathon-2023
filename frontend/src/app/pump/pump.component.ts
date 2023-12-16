import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TaxiService } from '../services/taxi.service';
import { Payment } from '../models/payment';

@Component({
  selector: 'app-pump',
  templateUrl: './pump.component.html',
  styleUrls: ['./pump.component.css']
})
export class PumpComponent {
  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService,) { }

  balance: number = 0;
  card: string = "";
  msg1: string = "";
  msg2: string = "";
  msg_request: string = "";
  payment: Payment = new Payment();

  check(): boolean {
    let regexcard = /^\d{16}$/;
    if (this.card.length == 0) {
      this.msg1 = "Field card number missing";
    } else if (!regexcard.test(this.card)) {
      this.msg1 = "Card number in wrong format";
    }
    else this.msg1 = "";
    if (this.balance <= 0) {
      this.msg2 = "Field cash amount missing";
    }
    else this.msg2 = "";
    if (this.msg1.length > 0 || this.msg2.length > 0) return false;
    return true;

  }

  pay() {
    if (!this.check()) return;
    this.service.payment(this.card, this.balance).subscribe(
      data => {
        this.payment = data;
        this.msg_request = this.payment.msg;
      }
    )
  }

  add_to_card() {
    if (!this.check()) return;
    this.payment = new Payment();
    this.service.pay_to_card(this.card, this.balance).subscribe(
      data => {
        this.msg_request = data;
        this.payment.disc = false;
        this.payment.points = false;
        this.payment.balance = -1;
      }
    )
  }
}
