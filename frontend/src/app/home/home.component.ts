import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
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

  constructor(private route: ActivatedRoute, private router: Router, private service: TaxiService, private changeDetectorRef: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.cardbuttontext = "Show my card";
    let logged = localStorage.getItem("csrftoken");
    if (logged == null) this.router.navigate(["login"]);
    this.card = JSON.parse(localStorage.getItem("card")!);

    this.service.getQR().subscribe(
      data => {
        const blob = new Blob([data.body!], { type: 'image/png' });
        const reader = new FileReader();
        reader.onload = () => {
          const dataURL = reader.result;
          this.imgSource = dataURL as string;
          // this.changeDetectorRef.detectChanges();
        };
        reader.readAsDataURL(blob);
      }
    )
  }

  showCard: boolean = false;
  showShare: boolean = false;
  imgSource: string = "";
  card: Card = new Card();
  cardbuttontext: string = "";


  toCard() {
    if (this.showCard == true) {
      this.cardbuttontext = "Show my card";
      this.showCard = false;
    } else {
      this.cardbuttontext = "Hide my card";
      console.log(1);
      this.showCard = true;
    }

  }

  toShare() {
    this.router.navigate(['recommend'])
  }

  showQR(): void {
    this.showCard = !this.showCard;
  }

}
