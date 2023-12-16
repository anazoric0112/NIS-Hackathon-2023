import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TaxiService } from '../services/taxi.service';
import { Card } from '../models/card';
import { Buffer } from 'buffer';
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

    this.service.getQR().subscribe(
      data => {
        const blob = new Blob([data.body!], { type: 'image/png' }); 
        const reader = new FileReader();
        reader.onload = () => { 
          const dataURL = reader.result;
          this.imgSource = dataURL as string
        };
        console.log(this.imgSource)
        reader.readAsDataURL(blob);
      }
    )
  }

  showCard: boolean = false;
  imgSource: string = "";
  card: Card = new Card();


  toCard() {
    this.showCard = !this.showCard;
  }
  
  toShare() {
    this.showCard = false;
    this.router.navigate(["recommend"]);
  }

  hexToBase64(hexString: string): string {
    console.log(hexString.slice(2).slice(0, -1))
    return Buffer.from(hexString.slice(2).slice(0, -1), 'hex').toString('base64');
  }

  showQR(): void {
    this.showCard = !this.showCard;
  }

}
