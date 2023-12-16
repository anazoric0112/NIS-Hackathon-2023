import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-redirecting',
  templateUrl: './redirecting.component.html',
  styleUrls: ['./redirecting.component.css']
})
export class RedirectingComponent {
  constructor(private router: Router)
  {
    router.navigate(["login"])
  }
}
