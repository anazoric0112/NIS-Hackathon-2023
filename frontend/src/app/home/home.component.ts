import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TaxiService } from '../services/taxi.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService) { }

  toCard() {
    this.router.navigate(["card"]);
  }
  toShare() {
    this.router.navigate(["recommend"]);
  }
}
