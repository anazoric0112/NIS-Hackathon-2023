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
    let qr = localStorage.getItem("showqr");
    if (qr == "1") {
      this.showQR();
      localStorage.setItem("showqr", "0");
    }
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
        };
        reader.readAsDataURL(blob);
      }
    )

    this.service.getCard(this.card.number).subscribe(
      data => {
        this.card = data;
        console.log(this.card);
      }
    )
  }

  showCard: boolean = false;
  showShare: boolean = false;
  imgSource: string = "";
  card: Card = new Card();

  imgpath: string = "../../assets/icons/";
  pathhome: string = this.imgpath + "home.png";
  pathshare: string = this.imgpath + "share.png";
  pathqr: string = this.imgpath + "qr.png";
  pathq: string = this.imgpath + "q.png";


  showSh() {
    this.router.navigate(['recommend'])
  }
  showInfo() {
    this.router.navigate(['info'])
  }
  showQR(): void {
    this.showCard = true;
  }
  showHome(): void {
    this.showCard = false;
  }

}
