import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.css']
})


export class InfoComponent {
  constructor(private router: Router) { }

  imgpath: string = "../../assets/icons/";
  pathhome: string = this.imgpath + "home.png";
  pathshare: string = this.imgpath + "share.png";
  pathqr: string = this.imgpath + "qr.png";
  pathq: string = this.imgpath + "q.png";

  showHome() {
    this.router.navigate(["home"]);
  }

  showQR() {
    localStorage.setItem("showqr", "1");
    this.router.navigate(["home"]);
  }

  showSh() {
    this.router.navigate(['recommend'])
  }

}
