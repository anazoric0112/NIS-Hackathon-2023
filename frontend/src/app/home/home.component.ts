import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TaxiService } from '../services/taxi.service';
import { Card } from '../models/card';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService) { }

  ngOnInit(): void {
    let logged = localStorage.getItem("csrftoken");
    if (logged == null) this.router.navigate(["login"]);
    this.card = JSON.parse(localStorage.getItem("card")!);

    // this.service.getQR().subscribe{
    //   data=>{

    //   }
    // }

  }

  showCard: boolean = false;
  showShare: boolean = false;
  imgSource: string = "";
  card: Card = new Card();


  toCard() {
    this.showCard = !this.showCard;
  }
  toShare() {
    this.showShare = !this.showShare;
  }

}
