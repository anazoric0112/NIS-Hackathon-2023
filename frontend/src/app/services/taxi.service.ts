import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { CardCsrf } from '../models/card_csrf';
import { Card } from '../models/card';

@Injectable({
  providedIn: 'root'
})
export class TaxiService {

  constructor(private http: HttpClient) { }

  baseUrl = "http://localhost:8000/taxi"

  login(phone: string, licence: string) {
    let data = {
      phone: phone,
      taxilicence: licence
    }
    return this.http.post<CardCsrf>(`${this.baseUrl}/login`, data);
  }
  getQR() {
    let card : Card = JSON.parse(localStorage.getItem("card")!)
    return this.http.post(`${this.baseUrl}/get_qr_code`, { taxilicence : card.taxiLicence }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': localStorage.getItem("csrftoken")!
      },
      observe: 'response', // Setting observe to 'response'
      responseType: 'blob' // Set responseType to 'text'
    });
  }

  sendSMS(phone: string) {

  }
  
  sendEmail(email: string) {

  }

}
